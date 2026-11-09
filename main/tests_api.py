import uuid
import base64
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

from django.contrib.auth.models import Group, Permission, User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Award, Experience, Project


class EditorSetupAPITest(APITestCase):
    def test_setup_creates_editor_with_only_section_edit_permissions(self):
        call_command("setup_editor", stdout=StringIO())
        group = Group.objects.get(name="Editor")
        self.assertEqual(set(group.permissions.values_list("codename", flat=True)), {
            "change_award", "change_experience",
        })
        self.assertFalse(group.user_set.exists())

    def test_setup_can_be_repeated_without_removing_existing_permissions_or_members(self):
        group = Group.objects.create(name="Editor")
        group.permissions.add(Permission.objects.get(codename="change_project"))
        user = User.objects.create_user("existing-editor", password="test-password")
        user.groups.add(group)
        for _ in range(2):
            call_command("setup_editor", stdout=StringIO())
        self.assertEqual(set(group.permissions.values_list("codename", flat=True)), {
            "change_project", "change_award", "change_experience",
        })
        self.assertEqual(list(group.user_set.all()), [user])

    def test_configured_editor_can_edit_both_sections_but_cannot_create_or_delete(self):
        user = User.objects.create_user("configured-editor", password="test-password")
        group = Group.objects.create(name="Editor")
        user.groups.add(group)
        award = Award.objects.create(title="Original Award", issuer="UI", year=2026)
        experience = Experience.objects.create(title="Original Experience", description="Work")
        call_command("setup_editor", stdout=StringIO())
        self.client.force_authenticate(user=user)
        for section, obj in [("award", award), ("experience", experience)]:
            with self.subTest(section=section):
                detail = reverse(f"api:{section}-detail", args=[obj.pk])
                self.assertEqual(self.client.patch(detail, {"title": "Edited"}, format="json").status_code, 200)
                self.assertEqual(self.client.post(reverse(f"api:{section}-list"), {}, format="json").status_code, 403)
                self.assertEqual(self.client.delete(detail).status_code, 403)
                obj.refresh_from_db()
                self.assertEqual(obj.title, "Edited")
                self.assertEqual(type(obj).objects.count(), 1)


class ProjectAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.project = Project.objects.create(
            title="Portfolio", description="My website", tech_stack="Django",
        )
        self.list_url = reverse("api:project-list")
        self.detail_url = reverse("api:project-detail", args=[self.project.id])
        self.star_url = reverse("api:project-star", args=[self.project.id])
        self.payload = {
            "title": "New project", "description": "A useful app", "tech_stack": "Python",
            "project_url": "https://example.com/", "project_image_url": "",
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.project.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"title": "PORT"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"title": "not-found"})
        self.assertEqual(response.data, [])

    def test_missing_project(self):
        url = reverse("api:project-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Project.objects.count(), 1)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Portfolio")

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Project.objects.filter(pk=response.data["id"]).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"project_url": "javascript:alert(1)"}, "project_url"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
        self.assertEqual(Project.objects.count(), 1)

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.description, "My website")
        response = self.client.put(self.detail_url, {"title": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_staff_and_editor_cannot_manage_tutorial_projects(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.visitor.groups.add(Group.objects.create(name="Editor"))
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Project.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        # The Browsable API form renders a real CSRF token into the response.
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AwardAPITest(APITestCase):
    """Tugas 6: kontrak API Awards, empat peran, validasi, Like, dan CSRF."""

    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_superuser(
            username="award-owner", password="test-password", email="owner@example.com",
        )
        cls.visitor = User.objects.create_user(username="award-user", password="test-password")
        cls.editor = User.objects.create_user(username="award-editor", password="test-password")
        editor_group = Group.objects.create(name="Editor")
        editor_group.permissions.add(Permission.objects.get(
            content_type__app_label="main", codename="change_award",
        ))
        cls.editor.groups.add(editor_group)
        cls.award = Award.objects.create(title="Web Prize", issuer="UI", year=2026)
        cls.payload = {
            "title": "New Prize", "issuer": "University", "year": 2025,
            "thumbnail": "https://example.com/award.jpg", "certificate_url": "",
        }
        cls.list_url = reverse("api:award-list")
        cls.detail_url = reverse("api:award-detail", args=[cls.award.id])
        cls.star_url = reverse("api:award-star", args=[cls.award.id])

    def test_public_list_detail_and_private_account_fields(self):
        self.award.liked_by.add(self.visitor)
        for user in (None, self.visitor, self.editor, self.owner):
            with self.subTest(user=user):
                self.client.force_authenticate(user=user)
                response = self.client.get(self.list_url)
                self.assertEqual(response.status_code, 200)
                data = response.data[0]
                self.assertEqual(set(data), {
                    "id", "title", "issuer", "year", "thumbnail", "certificate_url",
                    "like_count", "is_liked",
                })
                self.assertEqual(data["id"], str(self.award.id))
                self.assertEqual(data["like_count"], 1)
                self.assertEqual(data["is_liked"], user == self.visitor)
                self.assertEqual(self.client.get(self.detail_url).data, data)

    def test_guest_and_regular_user_cannot_manage_data(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            for method, url in [
                ("post", self.list_url), ("put", self.detail_url),
                ("patch", self.detail_url), ("delete", self.detail_url),
            ]:
                with self.subTest(user=user, method=method):
                    response = getattr(self.client, method)(url, self.payload, format="json")
                    self.assertEqual(response.status_code, 403)
                    self.assertEqual(Award.objects.count(), 1)
                    self.award.refresh_from_db()
                    self.assertEqual((self.award.title, self.award.issuer, self.award.year), ("Web Prize", "UI", 2026))
                    self.assertEqual(self.award.liked_by.count(), 0)

    def test_editor_can_patch_and_put_but_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(self.detail_url, {"title": "Edited Prize"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.award.refresh_from_db()
        self.assertEqual(self.award.title, "Edited Prize")
        self.assertEqual(self.award.issuer, "UI")
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, 200)
        self.award.refresh_from_db()
        self.assertEqual(self.award.issuer, self.payload["issuer"])
        for method, url in [("post", self.list_url), ("delete", self.detail_url)]:
            response = getattr(self.client, method)(url, self.payload, format="json")
            self.assertEqual(response.status_code, 403)
            self.assertEqual(Award.objects.count(), 1)
            self.award.refresh_from_db()
            self.assertEqual(self.award.title, self.payload["title"])

    def test_editor_group_without_model_permission_and_staff_are_denied(self):
        # Nama grup saja tidak cukup: aturan harus sama dengan update_award lama.
        Group.objects.get(name="Editor").permissions.clear()
        self.visitor.is_staff = True
        self.visitor.save()
        for user in (self.editor, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Forbidden"}, format="json").status_code, 403)
            self.award.refresh_from_db()
            self.assertEqual(self.award.title, "Web Prize")

    def test_owner_can_create_update_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, 201)
        created_url = reverse("api:award-detail", args=[response.data["id"]])
        created = Award.objects.get(pk=response.data["id"])
        self.assertEqual(created.title, self.payload["title"])
        self.assertEqual(self.client.patch(created_url, {"title": "Updated"}, format="json").status_code, 200)
        created.refresh_from_db()
        self.assertEqual(created.title, "Updated")
        self.assertEqual(self.client.delete(created_url).status_code, 204)
        self.assertFalse(Award.objects.filter(pk=created.id).exists())
        self.assertEqual(self.client.get(created_url).status_code, 404)

    def test_put_requires_required_fields_and_patch_preserves_other_fields(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.put(self.detail_url, {"title": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("issuer", response.data)
        self.assertIn("year", response.data)
        self.award.refresh_from_db()
        self.assertEqual(self.award.title, "Web Prize")
        self.assertEqual(self.client.patch(self.detail_url, {"year": 2024}, format="json").status_code, 200)
        self.award.refresh_from_db()
        self.assertEqual((self.award.title, self.award.issuer, self.award.year), ("Web Prize", "UI", 2024))

    def test_invalid_input_is_rejected_without_creating_data(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"issuer": "<br>"}, "issuer"),
            ({"year": -1}, "year"),
            ({"year": "invalid"}, "year"),
            ({"thumbnail": "javascript:alert(1)"}, "thumbnail"),
            ({"certificate_url": "ftp://example.com/award.pdf"}, "certificate_url"),
        ]:
            with self.subTest(field=field, changes=changes):
                response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
                self.assertEqual(response.status_code, 400)
                self.assertIn(field, response.data)
                self.assertEqual(Award.objects.count(), 1)

    def test_invalid_patch_preserves_existing_data(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(self.detail_url, {"title": "<br>", "year": 2024}, format="json")
        self.assertEqual(response.status_code, 400)
        self.award.refresh_from_db()
        self.assertEqual((self.award.title, self.award.year), ("Web Prize", 2026))

    def test_text_is_cleaned_and_optional_urls_may_be_empty(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "title": " <b>Prize</b> ", "issuer": "<i>UI</i>",
            "thumbnail": None, "certificate_url": "",
        }, format="json")
        self.assertEqual(response.status_code, 201)
        award = Award.objects.get(pk=response.data["id"])
        self.assertEqual((award.title, award.issuer), ("Prize", "UI"))

    def test_calculated_fields_and_like_relation_cannot_be_forged(self):
        self.client.force_authenticate(user=self.owner)
        forged_id = str(uuid.uuid4())
        response = self.client.post(self.list_url, {
            **self.payload, "id": forged_id, "liked_by": [self.visitor.id],
            "like_count": 99, "is_liked": True,
        }, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(response.data["id"], forged_id)
        self.assertEqual(response.data["like_count"], 0)
        self.assertFalse(response.data["is_liked"])
        self.assertEqual(Award.objects.get(pk=response.data["id"]).liked_by.count(), 0)

    def test_star_requires_login_and_uses_request_user(self):
        self.assertEqual(self.client.post(self.star_url).status_code, 403)
        self.assertEqual(self.award.liked_by.count(), 0)
        for user in (self.visitor, self.editor, self.owner):
            with self.subTest(user=user):
                self.client.force_authenticate(user=user)
                response = self.client.post(self.star_url, {"user_id": self.owner.id}, format="json")
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.data["is_liked"])
                self.assertEqual(response.data["like_count"], 1)
                self.assertEqual(list(self.award.liked_by.values_list("id", flat=True)), [user.id])
                response = self.client.post(self.star_url)
                self.assertFalse(response.data["is_liked"])
                self.assertEqual(response.data["like_count"], 0)
                self.assertEqual(self.award.liked_by.count(), 0)

    def test_search_year_and_ordering_work_together(self):
        Award.objects.create(title="Alpha Prize", issuer="UI", year=2024)
        Award.objects.create(title="Zeta Prize", issuer="UI", year=2026)
        response = self.client.get(self.list_url, {"q": "PRIZE", "year": 2026, "ordering": "title"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["title"] for item in response.data], ["Web Prize", "Zeta Prize"])
        response = self.client.get(self.list_url, {"ordering": "year"})
        self.assertEqual([item["year"] for item in response.data], [2024, 2026, 2026])
        self.assertEqual(self.client.get(self.list_url).data[0]["year"], 2026)
        self.assertEqual(self.client.get(self.list_url, {"q": "not-found"}).data, [])

    def test_invalid_query_returns_field_errors(self):
        for query, field in [
            ({"year": "invalid"}, "year"), ({"year": -1}, "year"),
            ({"ordering": "liked_by__password"}, "ordering"),
        ]:
            response = self.client.get(self.list_url, query)
            self.assertEqual(response.status_code, 400)
            self.assertIn(field, response.data)

    def test_missing_awards_and_wrong_methods(self):
        self.client.force_authenticate(user=self.owner)
        missing_id = uuid.uuid4()
        self.assertEqual(self.client.get(reverse("api:award-detail", args=[missing_id])).status_code, 404)
        self.assertEqual(self.client.post(reverse("api:award-star", args=[missing_id])).status_code, 404)
        self.assertEqual(self.client.delete(self.list_url).status_code, 405)
        self.assertEqual(self.client.get(self.star_url).status_code, 405)
        self.assertEqual(self.client.head(self.list_url).status_code, 200)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")

    def test_list_uses_two_queries_even_with_many_likes(self):
        # Satu query Awards dan satu prefetch Like, bukan query tambahan per kartu.
        for n in range(8):
            award = Award.objects.create(title=f"Prize {n}", issuer="UI", year=2026)
            award.liked_by.add(self.visitor, self.editor)
        self.client.force_authenticate(user=self.visitor)
        with self.assertNumQueries(2):
            response = self.client.get(self.list_url)
        self.assertEqual(len(response.data), 9)
        self.assertEqual(response.data[0]["like_count"], 2)
        self.assertTrue(response.data[0]["is_liked"])

    def test_real_session_without_csrf_cannot_write(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="award-owner", password="test-password"))
        for method, url, data in [
            ("post", self.list_url, self.payload),
            ("patch", self.detail_url, {"title": "Forbidden"}),
            ("delete", self.detail_url, {}), ("post", self.star_url, {}),
        ]:
            response = getattr(client, method)(url, data, format="json")
            self.assertEqual(response.status_code, 403)
            self.assertIn("CSRF", str(response.data))
            self.assertEqual(Award.objects.count(), 1)
            self.award.refresh_from_db()
            self.assertEqual(self.award.title, "Web Prize")
            self.assertEqual(self.award.liked_by.count(), 0)

    def test_real_sessions_with_csrf_allow_each_role(self):
        # Token berasal dari halaman Awards, termasuk bagi user tanpa modal tambah.
        for username, method, url, payload, expected in [
            ("award-user", "post", self.star_url, {}, 200),
            ("award-editor", "patch", self.detail_url, {"title": "Edited"}, 200),
            ("award-owner", "post", self.list_url, self.payload, 201),
        ]:
            client = APIClient(enforce_csrf_checks=True)
            self.assertTrue(client.login(username=username, password="test-password"))
            page = client.get(reverse("main:show_awards"))
            self.assertEqual(page.status_code, 200)
            token = client.cookies["csrftoken"].value
            response = getattr(client, method)(url, payload, format="json", HTTP_X_CSRFTOKEN=token)
            self.assertEqual(response.status_code, expected)
        self.award.refresh_from_db()
        self.assertEqual(self.award.title, "Edited")
        self.assertTrue(self.award.liked_by.filter(pk=self.visitor.pk).exists())
        self.assertEqual(Award.objects.count(), 2)

    def test_browsable_api_and_awards_page_use_new_endpoints(self):
        self.assertEqual(self.client.get(self.list_url, HTTP_ACCEPT="text/html").status_code, 200)
        for user, can_edit, can_create in [
            (self.visitor, False, False), (self.editor, True, False), (self.owner, True, True),
        ]:
            self.client.force_login(user)
            page = self.client.get(reverse("main:show_awards"))
            self.assertContains(page, self.list_url)
            self.assertNotContains(page, reverse("main:create_award_ajax"))
            self.assertEqual('id="award-form"' in page.content.decode(), can_edit)
            self.assertEqual('id="add-award-button"' in page.content.decode(), can_create)

    def test_certificate_gallery_is_available_for_every_role(self):
        # Galeri merupakan fitur baca publik, terpisah dari modal pengelolaan data.
        for user in (None, self.visitor, self.editor, self.owner):
            with self.subTest(user=user):
                self.client.logout()
                if user is not None:
                    self.client.force_login(user)
                page = self.client.get(reverse("main:show_awards"))
                self.assertEqual(page.status_code, 200)
                self.assertTemplateUsed(page, "components/award_gallery_modal.html")
                self.assertContains(page, '<dialog id="award-gallery"')
                self.assertContains(page, 'id="award-gallery-previous"')
                self.assertContains(page, 'id="award-gallery-next"')
                self.assertContains(page, 'type="application/pdf"')
                self.assertContains(page, 'rel="noopener noreferrer"')
                self.assertNotContains(page, 'id="share-awards"')


class ExperienceAPITest(APITestCase):
    """CRUD, Star, upload, dan empat peran Experience tanpa galeri sertifikat."""

    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_superuser("experience-owner", "owner@example.com", "test-password")
        cls.visitor = User.objects.create_user("experience-user", password="test-password")
        cls.editor = User.objects.create_user("experience-editor", password="test-password")
        group = Group.objects.create(name="Editor")
        group.permissions.add(Permission.objects.get(content_type__app_label="main", codename="change_experience"))
        cls.editor.groups.add(group)
        cls.experience = Experience.objects.create(title="Research Position", description="Research work", category="research")
        cls.list_url = reverse("api:experience-list")
        cls.detail_url = reverse("api:experience-detail", args=[cls.experience.id])
        cls.star_url = reverse("api:experience-star", args=[cls.experience.id])
        cls.payload = {"title": "New Experience", "description": "New work", "category": "volunteer", "thumbnail": ""}
        cls.png = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aR7UAAAAASUVORK5CYII=")

    def assert_original_unchanged(self):
        self.assertEqual(Experience.objects.count(), 1)
        self.experience.refresh_from_db()
        self.assertEqual((self.experience.title, self.experience.description, self.experience.category),
                         ("Research Position", "Research work", "research"))
        self.assertEqual(self.experience.starred_by.count(), 0)

    def test_public_read_and_star_representation_for_all_roles(self):
        self.experience.starred_by.add(self.visitor)
        for user in (None, self.visitor, self.editor, self.owner):
            self.client.force_authenticate(user=user)
            response = self.client.get(self.list_url)
            self.assertEqual(response.status_code, 200)
            data = response.data[0]
            self.assertEqual(set(data), {
                "id", "title", "description", "category", "category_display", "thumbnail",
                "started_at", "ended_at", "is_ongoing", "star_count", "is_starred",
            })
            self.assertEqual(data["category"], "research")
            self.assertEqual(data["category_display"], "Research")
            self.assertTrue(data["is_ongoing"])
            self.assertEqual(data["star_count"], 1)
            self.assertEqual(data["is_starred"], user == self.visitor)
            self.assertEqual(self.client.get(self.detail_url).data, data)

    def test_guest_and_regular_user_cannot_manage_data(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            for method, url in [("post", self.list_url), ("put", self.detail_url), ("patch", self.detail_url), ("delete", self.detail_url)]:
                with self.subTest(user=user, method=method):
                    self.assertEqual(getattr(self.client, method)(url, self.payload, format="json").status_code, 403)
                    self.assert_original_unchanged()

    def test_editor_can_patch_put_but_cannot_create_delete(self):
        self.client.force_authenticate(user=self.editor)
        self.assertEqual(self.client.patch(self.detail_url, {"title": "Edited"}, format="json").status_code, 200)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Edited")
        self.assertEqual(self.experience.description, "Research work")
        self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, 200)
        for method, url in [("post", self.list_url), ("delete", self.detail_url)]:
            self.assertEqual(getattr(self.client, method)(url, self.payload, format="json").status_code, 403)
            self.assertEqual(Experience.objects.count(), 1)
            self.experience.refresh_from_db()
            self.assertEqual(self.experience.title, self.payload["title"])

    def test_model_permissions_do_not_leak_between_awards_and_experience(self):
        self.visitor.user_permissions.add(Permission.objects.get(content_type__app_label="main", codename="change_award"))
        self.client.force_authenticate(user=self.visitor)
        self.assertEqual(self.client.patch(self.detail_url, {"title": "Forbidden"}, format="json").status_code, 403)
        self.assert_original_unchanged()
        award = Award.objects.create(title="Prize", issuer="UI", year=2026)
        self.client.force_authenticate(user=self.editor)
        self.assertEqual(self.client.patch(reverse("api:award-detail", args=[award.id]), {"title": "Forbidden"}, format="json").status_code, 403)
        award.refresh_from_db()
        self.assertEqual(award.title, "Prize")

    def test_editor_group_without_permission_and_staff_cannot_edit(self):
        Group.objects.get(name="Editor").permissions.clear()
        self.visitor.is_staff = True
        self.visitor.save()
        for user in (self.editor, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Forbidden"}, format="json").status_code, 403)
            self.assert_original_unchanged()

    def test_owner_can_create_and_delete_with_empty_204_body(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, 201)
        created = Experience.objects.get(pk=response.data["id"])
        self.assertEqual(created.title, self.payload["title"])
        response = self.client.delete(reverse("api:experience-detail", args=[created.id]))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")
        self.assertFalse(Experience.objects.filter(pk=created.id).exists())

    def test_put_requires_fields_and_invalid_patch_does_not_write(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.put(self.detail_url, {"title": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("description", response.data)
        self.assert_original_unchanged()
        response = self.client.patch(self.detail_url, {"title": "<br>", "category": "volunteer"}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assert_original_unchanged()

    def test_validation_rejects_bad_text_categories_urls_and_dates(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"), ({"title": '<img src=x onerror="alert(1)">'}, "title"),
            ({"description": "<br>"}, "description"), ({"category": "invalid"}, "category"),
            ({"thumbnail": "javascript:alert(1)"}, "thumbnail"), ({"thumbnail": "ftp://example.com/image.png"}, "thumbnail"),
            ({"thumbnail": "/static/img/experience-forged.png"}, "thumbnail"), ({"ended_at": "invalid"}, "ended_at"),
        ]:
            with self.subTest(changes=changes):
                response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
                self.assertEqual(response.status_code, 400)
                self.assertIn(field, response.data)
                self.assert_original_unchanged()

    def test_sanitization_and_empty_thumbnail(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "title": " <b>Safe</b> ", "description": "<i>Work</i>", "thumbnail": None,
        }, format="json")
        self.assertEqual(response.status_code, 201)
        obj = Experience.objects.get(pk=response.data["id"])
        self.assertEqual((obj.title, obj.description, obj.thumbnail), ("Safe", "Work", None))

    def test_computed_fields_identity_and_star_relation_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        forged = str(uuid.uuid4())
        response = self.client.post(self.list_url, {
            **self.payload, "id": forged, "started_at": "2000-01-01T00:00:00Z",
            "star_count": 99, "is_starred": True, "starred_by": [self.visitor.id], "category_display": "Fake",
        }, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(response.data["id"], forged)
        self.assertFalse(response.data["started_at"].startswith("2000"))
        self.assertEqual(response.data["category_display"], "Volunteer")
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(Experience.objects.get(pk=response.data["id"]).starred_by.count(), 0)

    def test_star_uses_request_user_and_toggles_for_every_logged_in_role(self):
        self.assertEqual(self.client.post(self.star_url).status_code, 403)
        self.assertEqual(self.experience.starred_by.count(), 0)
        for user in (self.visitor, self.editor, self.owner):
            self.client.force_authenticate(user=user)
            response = self.client.post(self.star_url, {"user_id": self.owner.id}, format="json")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data["star_count"], 1)
            self.assertTrue(response.data["is_starred"])
            self.assertEqual(list(self.experience.starred_by.values_list("id", flat=True)), [user.id])
            response = self.client.post(self.star_url)
            self.assertFalse(response.data["is_starred"])
            self.assertEqual(response.data["star_count"], 0)
            self.assertEqual(self.experience.starred_by.count(), 0)

    def test_search_category_and_empty_results(self):
        Experience.objects.create(title="Research Volunteer", description="Work", category="volunteer")
        response = self.client.get(self.list_url, {"q": "RESEARCH", "category": "research"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["id"] for item in response.data], [str(self.experience.id)])
        self.assertEqual(self.client.get(self.list_url, {"q": "no-match"}).data, [])
        self.assertEqual(len(self.client.get(self.list_url).data), 2)
        response = self.client.get(self.list_url, {"category": "invalid"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("category", response.data)

    def test_missing_objects_wrong_methods_and_head(self):
        self.client.force_authenticate(user=self.owner)
        missing = uuid.uuid4()
        self.assertEqual(self.client.get(reverse("api:experience-detail", args=[missing])).status_code, 404)
        self.assertEqual(self.client.post(reverse("api:experience-star", args=[missing])).status_code, 404)
        self.assertEqual(self.client.delete(self.list_url).status_code, 405)
        self.assertEqual(self.client.get(self.star_url).status_code, 405)
        self.assertEqual(self.client.head(self.list_url).status_code, 200)

    def test_prefetch_avoids_queries_for_each_experience(self):
        for i in range(8):
            obj = Experience.objects.create(title=f"Experience {i}", description="Work")
            obj.starred_by.add(self.visitor)
        self.client.force_authenticate(user=self.visitor)
        with self.assertNumQueries(2):
            response = self.client.get(self.list_url)
        self.assertEqual(len(response.data), 9)
        self.assertEqual(sum(item["star_count"] for item in response.data), 8)

    def test_real_session_without_csrf_cannot_change_any_data(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="experience-owner", password="test-password"))
        for method, url in [("post", self.list_url), ("put", self.detail_url), ("patch", self.detail_url), ("delete", self.detail_url), ("post", self.star_url)]:
            response = getattr(client, method)(url, self.payload, format="json")
            self.assertEqual(response.status_code, 403)
            self.assertIn("CSRF", str(response.data))
            self.assert_original_unchanged()

    def test_real_sessions_with_csrf_work_for_each_role(self):
        for user, method, url, payload, expected in [
            (self.visitor, "post", self.star_url, {}, 200),
            (self.editor, "patch", self.detail_url, {"title": "Edited"}, 200),
            (self.owner, "post", self.list_url, self.payload, 201),
        ]:
            client = APIClient(enforce_csrf_checks=True)
            self.assertTrue(client.login(username=user.username, password="test-password"))
            self.assertEqual(client.get(reverse("main:show_experience")).status_code, 200)
            token = client.cookies["csrftoken"].value
            response = getattr(client, method)(url, payload, format="json", HTTP_X_CSRFTOKEN=token)
            self.assertEqual(response.status_code, expected)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Edited")
        self.assertTrue(self.experience.starred_by.filter(pk=self.visitor.pk).exists())

    def test_upload_create_and_editor_patch_preserve_file_contents(self):
        with TemporaryDirectory() as directory, override_settings(BASE_DIR=Path(directory)):
            self.client.force_authenticate(user=self.owner)
            response = self.client.post(self.list_url, {
                **self.payload, "thumbnail_source": "upload",
                "thumbnail_file": SimpleUploadedFile("photo.png", self.png, content_type="image/png"),
            }, format="multipart")
            self.assertEqual(response.status_code, 201, response.data)
            first_path = response.data["thumbnail"]
            self.assertTrue(first_path.startswith("/static/img/experience-"))
            self.assertEqual((Path(directory) / first_path.lstrip("/")).read_bytes(), self.png)
            self.assertNotIn("thumbnail_source", response.data)
            self.assertNotIn("thumbnail_file", response.data)
            self.client.force_authenticate(user=self.editor)
            detail = reverse("api:experience-detail", args=[response.data["id"]])
            response = self.client.patch(detail, {
                "thumbnail_source": "upload",
                "thumbnail_file": SimpleUploadedFile("replacement.png", self.png, content_type="image/png"),
            }, format="multipart")
            self.assertEqual(response.status_code, 200, response.data)
            self.assertNotEqual(response.data["thumbnail"], first_path)
            self.assertEqual((Path(directory) / response.data["thumbnail"].lstrip("/")).read_bytes(), self.png)

    def test_invalid_uploads_do_not_create_rows_or_files(self):
        self.client.force_authenticate(user=self.owner)
        cases = [
            ("bad.png", b"<script>alert(1)</script>"),
            ("bad.html", self.png),
            ("big.png", self.png + b"0" * (5 * 1024 * 1024)),
        ]
        with TemporaryDirectory() as directory, override_settings(BASE_DIR=Path(directory)):
            for filename, contents in cases:
                response = self.client.post(self.list_url, {
                    **self.payload, "thumbnail_source": "upload",
                    "thumbnail_file": SimpleUploadedFile(filename, contents),
                }, format="multipart")
                self.assertEqual(response.status_code, 400)
                self.assertIn("thumbnail_file", response.data)
                self.assert_original_unchanged()
            response = self.client.post(self.list_url, {**self.payload, "thumbnail_source": "upload"}, format="json")
            self.assertEqual(response.status_code, 400)
            self.assertIsInstance(response.data["thumbnail_file"], list)
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_existing_uploaded_thumbnail_can_be_kept_when_editing(self):
        self.experience.thumbnail = f"/static/img/experience-{uuid.uuid4().hex}.png"
        self.experience.save()
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(self.detail_url, {
            "description": "Updated", "thumbnail_source": "url", "thumbnail": self.experience.thumbnail,
        }, format="json")
        self.assertEqual(response.status_code, 200, response.data)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.description, "Updated")
        self.assertEqual(response.data["thumbnail"], self.experience.thumbnail)
        response = self.client.patch(self.detail_url, {"thumbnail": "/static/img/experience-forged.png"}, format="json")
        self.assertEqual(response.status_code, 400)
        self.experience.refresh_from_db()
        self.assertNotEqual(self.experience.thumbnail, "/static/img/experience-forged.png")

    def test_page_uses_drf_modal_for_editor_without_gallery(self):
        self.assertEqual(self.client.get(self.list_url, HTTP_ACCEPT="text/html").status_code, 200)
        for user, can_edit, can_create in [(None, False, False), (self.visitor, False, False), (self.editor, True, False), (self.owner, True, True)]:
            self.client.logout()
            if user is not None:
                self.client.force_login(user)
            page = self.client.get(reverse("main:show_experience"))
            self.assertEqual(page.status_code, 200)
            self.assertContains(page, self.list_url)
            self.assertNotContains(page, reverse("main:create_experience_ajax"))
            self.assertNotContains(page, 'id="award-gallery"')
            self.assertEqual('id="experience-form"' in page.content.decode(), can_edit)
            self.assertEqual('id="add-experience-button"' in page.content.decode(), can_create)

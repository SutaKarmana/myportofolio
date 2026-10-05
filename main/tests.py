from django.contrib.auth.models import Group, Permission, User
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from main.forms import AwardForm, EducationForm, ExperienceForm, ProjectForm
from main.models import Award, Education, Experience, Project


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertNotContains(response, self.experience.title)
        data = self.client.get(reverse("main:get_experience_json")).json()["items"][0]
        self.assertEqual(data["title"], self.experience.title)
        self.assertEqual(data["description"], self.experience.description)
        self.assertEqual(data["category"], "Part-Time")
        self.assertIsNone(data["ended_at"])
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Memuat data")
        self.assertEqual(self.client.get(reverse("main:get_experience_json")).json()["items"], [])

    def test_experience_form_requires_uploaded_thumbnail(self):
        form = ExperienceForm(
            data={
                "title": "Pengalaman",
                "description": "Deskripsi",
                "category": "research",
                "thumbnail_source": "upload",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("thumbnail_file", form.errors)

    def test_experience_json_endpoint(self):
        response = self.client.get(reverse("main:get_experience_json"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertContains(response, self.experience.title)

    def test_education_crud(self):
        self.client.force_login(
            User.objects.create_superuser(
                username="education-owner",
                password="test-password",
                email="education-owner@example.com",
            )
        )
        create_response = self.client.post(
            reverse("main:create_education"),
            {
                "institusi": "Universitas Indonesia",
                "program": "Sistem Informasi",
                "description": "Mempelajari sistem informasi.",
                "started_year": 2022,
                "ended_year": "",
                "thumbnail": "",
            },
        )
        education = Education.objects.get(institusi="Universitas Indonesia")

        self.assertRedirects(create_response, reverse("main:show_education"))
        self.assertTrue(
            EducationForm(
                data={
                    "institusi": education.institusi,
                    "program": education.program,
                    "description": education.description,
                    "started_year": education.started_year,
                    "ended_year": "",
                    "thumbnail": "",
                }
            ).is_valid()
        )

        update_response = self.client.post(
            reverse("main:update_education", args=[education.id]),
            {
                "institusi": "Universitas Terbaru",
                "program": "Sistem Informasi",
                "description": "Deskripsi terbaru.",
                "started_year": 2022,
                "ended_year": 2026,
                "thumbnail": "",
            },
        )
        education.refresh_from_db()

        self.assertRedirects(update_response, reverse("main:show_education"))
        self.assertEqual(education.institusi, "Universitas Terbaru")

        delete_response = self.client.post(
            reverse("main:delete_education", args=[education.id])
        )

        self.assertRedirects(delete_response, reverse("main:show_education"))
        self.assertFalse(Education.objects.filter(pk=education.id).exists())

    def test_education_page(self):
        education = Education.objects.create(
            institusi="Universitas Indonesia",
            program="Sistem Informasi",
            description="Mempelajari sistem informasi dan pengembangan aplikasi.",
            started_year=2022,
        )

        response = self.client.get(reverse("main:show_education"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education.html")
        self.assertNotContains(response, education.description)
        data = self.client.get(reverse("main:get_education_json")).json()["items"][0]
        self.assertEqual(data["institusi"], education.institusi)
        self.assertEqual(data["program"], education.program)
        self.assertEqual(data["description"], education.description)
        self.assertIsNone(data["ended_year"])

    def test_empty_education_page(self):
        response = self.client.get(reverse("main:show_education"))

        self.assertContains(response, "Memuat data")
        self.assertEqual(self.client.get(reverse("main:get_education_json")).json()["items"], [])

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        data = self.client.get(reverse("main:get_experience_json")).json()["items"][0]
        self.assertEqual(data["ended_at"], self.experience.ended_at.isoformat())

    def test_award_model(self):
        award = Award.objects.create(
            title="Juara 1 Web Design",
            issuer="INVOFEST",
            year=2023,
        )

        self.assertEqual(str(award), "Juara 1 Web Design (2023)")
        self.assertEqual(award.issuer, "INVOFEST")
        self.assertEqual(award.year, 2023)

    def test_awards_url_is_accessible(self):
        response = self.client.get(reverse("main:show_awards"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "awards.html")

    def test_awards_page(self):
        award = Award.objects.create(
            title="Juara 2 Brain Challenge Competition",
            issuer="Brain Challenge Universitas Telkom",
            year=2024,
            thumbnail="/static/img/BrainChallenge.jpg",
            certificate_url="/static/pdfPrestasi/YaudahlahYa.pdf",
        )

        response = self.client.get(reverse("main:show_awards"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "awards.html")
        self.assertNotContains(response, award.title)
        data = self.client.get(reverse("main:get_awards_json")).json()["awards"][0]
        self.assertEqual(data["title"], award.title)
        self.assertEqual(data["issuer"], award.issuer)
        self.assertEqual(data["thumbnail"], award.thumbnail)
        self.assertEqual(data["certificate_url"], award.certificate_url)

    def test_awards_are_ordered_by_year(self):
        older_award = Award.objects.create(
            title="Juara 1 Web Design",
            issuer="INVOFEST",
            year=2023,
        )
        newer_award = Award.objects.create(
            title="Juara 2 Brain Challenge Competition",
            issuer="Brain Challenge Universitas Telkom",
            year=2024,
        )

        awards = list(Award.objects.all())

        self.assertEqual(awards, [newer_award, older_award])

    def test_empty_awards_page(self):
        response = self.client.get(reverse("main:show_awards"))

        self.assertContains(response, "Memuat data")
        self.assertEqual(self.client.get(reverse("main:get_awards_json")).json()["awards"], [])

    def test_award_form_validates_year(self):
        form = AwardForm(
            data={
                "title": "Juara 1",
                "issuer": "Penyelenggara",
                "year": "bukan tahun",
                "thumbnail": "",
                "certificate_url": "",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("year", form.errors)

    def test_award_crud(self):
        self.client.force_login(
            User.objects.create_superuser(
                username="award-owner",
                password="test-password",
                email="award-owner@example.com",
            )
        )
        create_response = self.client.post(
            reverse("main:create_award"),
            {
                "title": "Juara 1",
                "issuer": "Penyelenggara",
                "year": 2025,
                "thumbnail": "",
                "certificate_url": "",
            },
        )
        award = Award.objects.get(title="Juara 1")

        self.assertRedirects(create_response, reverse("main:show_awards"))

        update_response = self.client.post(
            reverse("main:update_award", args=[award.id]),
            {
                "title": "Juara Utama",
                "issuer": "Penyelenggara",
                "year": 2025,
                "thumbnail": "",
                "certificate_url": "",
            },
        )
        award.refresh_from_db()

        self.assertRedirects(update_response, reverse("main:show_awards"))
        self.assertEqual(award.title, "Juara Utama")

        delete_response = self.client.post(
            reverse("main:delete_award", args=[award.id])
        )

        self.assertRedirects(delete_response, reverse("main:show_awards"))
        self.assertFalse(Award.objects.filter(pk=award.id).exists())


class ProjectAuthorizationTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="Portfolio",
            description="Website portfolio",
            tech_stack="Django",
        )
        self.award = Award.objects.create(
            title="Award",
            issuer="Issuer",
            year=2026,
        )
        self.education = Education.objects.create(
            institusi="University",
            program="Information Systems",
            description="Education record",
            started_year=2022,
        )
        self.experience = Experience.objects.create(
            title="Experience",
            description="Experience record",
            category="part-time",
        )
        self.regular_user = User.objects.create_user(
            username="regular",
            password="test-password",
        )
        self.editor_user = User.objects.create_user(
            username="editor",
            password="test-password",
        )
        editor_group = Group.objects.create(name="Editor")
        editor_group.permissions.add(
            Permission.objects.get(
                codename="change_project",
                content_type__app_label="main",
            ),
            Permission.objects.get(
                codename="change_award",
                content_type__app_label="main",
            ),
            Permission.objects.get(
                codename="change_education",
                content_type__app_label="main",
            ),
            Permission.objects.get(
                codename="change_experience",
                content_type__app_label="main",
            ),
        )
        self.editor_user.groups.add(editor_group)
        self.owner = User.objects.create_superuser(
            username="owner",
            password="test-password",
            email="owner@example.com",
        )

    def test_superuser_project_page_renders_add_modal_and_form(self):
        self.client.force_login(self.owner)
        response = self.client.get(reverse("main:show_projects"))

        self.assertContains(response, 'popovertarget="add-project-modal"')
        self.assertContains(response, 'id="add-project-modal"')
        self.assertContains(response, 'id="project-form"')
        self.assertContains(response, 'name="title"')

    def test_superuser_can_add_project_via_ajax(self):
        self.client.force_login(self.owner)
        response = self.client.post(
            reverse("main:create_project_ajax"),
            {
                "title": "New project",
                "description": "Built with Django",
                "tech_stack": "Django",
                "project_url": "",
                "project_image_url": "",
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Project.objects.filter(title="New project").exists())

    def test_project_page_is_public_but_star_requires_login(self):
        response = self.client.get(reverse("main:show_projects"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Star")

        response = self.client.post(
            reverse("main:toggle_star", args=[self.project.id])
        )
        self.assertRedirects(
            response,
            f"{reverse('main:login')}?next={reverse('main:toggle_star', args=[self.project.id])}",
        )

    def test_regular_user_can_star_but_cannot_change_projects(self):
        self.client.force_login(self.regular_user)

        star_response = self.client.post(
            reverse("main:toggle_star", args=[self.project.id])
        )
        self.assertRedirects(star_response, reverse("main:show_projects"))
        self.assertTrue(self.project.starred_by.filter(pk=self.regular_user.pk).exists())

        self.assertEqual(
            self.client.get(reverse("main:create_project")).status_code,
            403,
        )
        self.assertEqual(
            self.client.get(
                reverse("main:update_project", args=[self.project.id])
            ).status_code,
            403,
        )
        self.assertEqual(
            self.client.post(
                reverse("main:delete_project", args=[self.project.id])
            ).status_code,
            403,
        )

    def test_editor_can_edit_but_cannot_create_or_delete(self):
        self.client.force_login(self.editor_user)

        update_response = self.client.post(
            reverse("main:update_project", args=[self.project.id]),
            {
                "title": "Updated Portfolio",
                "description": "Updated description",
                "tech_stack": "Django, Python",
                "project_url": "",
                "project_image_url": "",
            },
        )
        self.assertRedirects(update_response, reverse("main:show_projects"))
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Updated Portfolio")
        self.assertEqual(
            self.client.get(reverse("main:create_project")).status_code,
            403,
        )
        self.assertEqual(
            self.client.post(
                reverse("main:delete_project", args=[self.project.id])
            ).status_code,
            403,
        )

    def test_superuser_can_create_edit_and_delete(self):
        self.client.force_login(self.owner)

        self.assertEqual(
            self.client.get(reverse("main:create_project")).status_code,
            200,
        )
        self.assertEqual(
            self.client.get(
                reverse("main:update_project", args=[self.project.id])
            ).status_code,
            200,
        )
        delete_response = self.client.post(
            reverse("main:delete_project", args=[self.project.id])
        )
        self.assertRedirects(delete_response, reverse("main:show_projects"))
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())

    def test_star_endpoint_accepts_only_post(self):
        self.client.force_login(self.regular_user)
        response = self.client.get(
            reverse("main:toggle_star", args=[self.project.id])
        )
        self.assertEqual(response.status_code, 405)

    def test_award_permissions_match_roles(self):
        self.assertEqual(
            self.client.get(reverse("main:show_awards")).status_code,
            200,
        )
        self.assertEqual(
            self.client.get(reverse("main:create_award")).status_code,
            302,
        )

        self.client.force_login(self.regular_user)
        self.assertEqual(
            self.client.get(reverse("main:create_award")).status_code,
            403,
        )
        self.assertEqual(
            self.client.get(reverse("main:update_award", args=[self.award.id])).status_code,
            403,
        )
        self.assertEqual(
            self.client.post(reverse("main:delete_award", args=[self.award.id])).status_code,
            403,
        )

        self.client.force_login(self.editor_user)
        self.assertEqual(
            self.client.get(reverse("main:update_award", args=[self.award.id])).status_code,
            200,
        )
        self.assertEqual(
            self.client.get(reverse("main:create_award")).status_code,
            403,
        )
        self.assertEqual(
            self.client.post(reverse("main:delete_award", args=[self.award.id])).status_code,
            403,
        )

        self.client.force_login(self.owner)
        self.assertEqual(
            self.client.get(reverse("main:create_award")).status_code,
            200,
        )
        self.assertEqual(
            self.client.get(reverse("main:update_award", args=[self.award.id])).status_code,
            200,
        )
        delete_response = self.client.post(
            reverse("main:delete_award", args=[self.award.id])
        )
        self.assertRedirects(delete_response, reverse("main:show_awards"))

    def test_education_permissions_match_roles(self):
        self.assertEqual(
            self.client.get(reverse("main:show_education")).status_code,
            200,
        )
        self.assertEqual(
            self.client.get(reverse("main:create_education")).status_code,
            302,
        )

        self.client.force_login(self.regular_user)
        self.assertEqual(
            self.client.get(reverse("main:create_education")).status_code,
            403,
        )
        self.assertEqual(
            self.client.get(
                reverse("main:update_education", args=[self.education.id])
            ).status_code,
            403,
        )
        self.assertEqual(
            self.client.post(
                reverse("main:delete_education", args=[self.education.id])
            ).status_code,
            403,
        )

        self.client.force_login(self.editor_user)
        self.assertEqual(
            self.client.get(
                reverse("main:update_education", args=[self.education.id])
            ).status_code,
            200,
        )
        self.assertEqual(
            self.client.get(reverse("main:create_education")).status_code,
            403,
        )
        self.assertEqual(
            self.client.post(
                reverse("main:delete_education", args=[self.education.id])
            ).status_code,
            403,
        )

        self.client.force_login(self.owner)
        self.assertEqual(
            self.client.get(reverse("main:create_education")).status_code,
            200,
        )
        self.assertEqual(
            self.client.get(
                reverse("main:update_education", args=[self.education.id])
            ).status_code,
            200,
        )

    def test_experience_permissions_match_roles(self):
        self.assertEqual(
            self.client.get(reverse("main:show_experience")).status_code,
            200,
        )
        self.assertEqual(
            self.client.get(reverse("main:create_experience")).status_code,
            302,
        )

        self.client.force_login(self.regular_user)
        self.assertEqual(
            self.client.get(reverse("main:create_experience")).status_code,
            403,
        )
        self.assertEqual(
            self.client.get(
                reverse("main:update_experience", args=[self.experience.id])
            ).status_code,
            403,
        )
        self.assertEqual(
            self.client.post(
                reverse("main:delete_experience", args=[self.experience.id])
            ).status_code,
            403,
        )

        self.client.force_login(self.editor_user)
        self.assertEqual(
            self.client.get(
                reverse("main:update_experience", args=[self.experience.id])
            ).status_code,
            200,
        )
        self.assertEqual(
            self.client.get(reverse("main:create_experience")).status_code,
            403,
        )
        self.assertEqual(
            self.client.post(
                reverse("main:delete_experience", args=[self.experience.id])
            ).status_code,
            403,
        )

        self.client.force_login(self.owner)
        self.assertEqual(
            self.client.get(reverse("main:create_experience")).status_code,
            200,
        )
        self.assertEqual(
            self.client.get(
                reverse("main:update_experience", args=[self.experience.id])
            ).status_code,
            200,
        )

    def test_award_like_requires_login_and_toggles_for_users(self):
        response = self.client.get(reverse("main:show_awards"))
        self.assertContains(response, 'id="grid"')
        data = self.client.get(reverse("main:get_awards_json")).json()["awards"][0]
        self.assertFalse(data["is_liked"])

        like_url = reverse("main:toggle_like", args=[self.award.id])
        response = self.client.post(like_url)
        self.assertRedirects(
            response,
            f"{reverse('main:login')}?next={like_url}",
        )

        self.client.force_login(self.regular_user)
        response = self.client.post(like_url)
        self.assertRedirects(response, reverse("main:show_awards"))
        self.assertTrue(self.award.liked_by.filter(pk=self.regular_user.pk).exists())

        response = self.client.post(like_url)
        self.assertRedirects(response, reverse("main:show_awards"))
        self.assertFalse(self.award.liked_by.filter(pk=self.regular_user.pk).exists())

        self.assertEqual(self.client.get(like_url).status_code, 405)

    def test_ajax_creation_checks_all_roles_and_http_status(self):
        cases = [
            ("create_project_ajax", {"title": "New", "description": "Description", "tech_stack": "Django"}, Project),
            ("create_award_ajax", {"title": "New", "issuer": "UI", "year": 2026}, Award),
            ("create_education_ajax", {"institusi": "New", "program": "SI", "description": "Description", "started_year": 2026}, Education),
            ("create_experience_ajax", {"title": "New", "description": "Description", "category": "research"}, Experience),
        ]
        for route, payload, model in cases:
            url = reverse(f"main:{route}")
            for user in (None, self.regular_user, self.editor_user):
                self.client.logout()
                if user:
                    self.client.force_login(user)
                before = model.objects.count()
                response = self.client.post(url, payload)
                self.assertEqual(response.status_code, 403, route)
                self.assertIn("message", response.json())
                self.assertEqual(model.objects.count(), before)
            self.client.force_login(self.owner)
            self.assertEqual(self.client.get(url).status_code, 405)
            self.assertEqual(self.client.post(url, {}).status_code, 400)
            before = model.objects.count()
            response = self.client.post(url, payload)
            self.assertEqual(response.status_code, 201, route)
            self.assertEqual(model.objects.count(), before + 1)

    def test_ajax_csrf_token_required_on_every_add_endpoint(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.owner)
        for section, route, payload in [
            ("projects", "project", {"title": "CSRF", "description": "Description", "tech_stack": "Django"}),
            ("awards", "award", {"title": "CSRF", "issuer": "UI", "year": 2026}),
            ("education", "education", {"institusi": "CSRF", "program": "SI", "description": "Description", "started_year": 2026}),
            ("experience", "experience", {"title": "CSRF", "description": "Description", "category": "research"}),
        ]:
            url = reverse(f"main:create_{route}_ajax")
            self.assertEqual(client.post(url, payload).status_code, 403)
            client.get(reverse(f"main:show_{section}"))
            token = client.cookies["csrftoken"].value
            self.assertEqual(client.post(url, payload, HTTP_X_CSRFTOKEN=token).status_code, 201)

    def test_ajax_search_without_unused_star_data(self):
        for section, record in [("education", self.education), ("experience", self.experience)]:
            url = reverse(f"main:get_{section}_json")
            self.assertEqual(self.client.get(url, {"q": "no-match"}).json()["items"], [])
            # Tanpa relasi Star, daftar hanya membutuhkan satu query database.
            with self.assertNumQueries(1):
                item = self.client.get(url).json()["items"][0]
            self.assertEqual(item["id"], str(record.id))
            for field in ("star_count", "is_starred", "reaction_url"):
                self.assertNotIn(field, item)
            self.assertEqual(item["edit_url"], reverse(f"main:update_{section}", args=[record.id]))
            self.assertEqual(item["delete_url"], reverse(f"main:delete_{section}", args=[record.id]))

    def test_form_sanitizes_text_and_rejects_xss_only_values(self):
        payloads = [
            (ProjectForm, {"title": "New", "description": "Description", "tech_stack": "Django"}, ("title", "description", "tech_stack")),
            (AwardForm, {"title": "New", "issuer": "UI", "year": 2026}, ("title", "issuer")),
            (EducationForm, {"institusi": "UI", "program": "SI", "description": "Description", "started_year": 2026}, ("institusi", "program", "description")),
            (ExperienceForm, {"title": "New", "description": "Description", "category": "research"}, ("title", "description")),
        ]
        for form_class, payload, fields in payloads:
            for field in fields:
                form = form_class({**payload, field: '<img src="x" onerror="alert(1)">'})
                self.assertFalse(form.is_valid(), (form_class, field))
                self.assertIn(field, form.errors)
                form = form_class({**payload, field: '<b>Teks aman</b>'})
                self.assertTrue(form.is_valid(), form.errors)
                self.assertEqual(form.cleaned_data[field], "Teks aman")

    def test_validation_rejects_unsafe_urls_and_inconsistent_years(self):
        education = EducationForm({"institusi": "UI", "program": "SI", "description": "Text", "started_year": 2026, "ended_year": 2025})
        self.assertFalse(education.is_valid())
        self.assertIn("ended_year", education.errors)
        award = AwardForm({"title": "Award", "issuer": "UI", "year": 2026, "certificate_url": "javascript:alert(1)"})
        self.assertFalse(award.is_valid())
        self.assertIn("certificate_url", award.errors)

    def test_like_and_delete_keep_role_restrictions(self):
        self.client.force_login(self.regular_user)
        like_url = reverse("main:toggle_like", args=[self.award.id])
        self.assertRedirects(self.client.post(like_url), reverse("main:show_awards"))
        self.assertTrue(self.award.liked_by.filter(pk=self.regular_user.pk).exists())
        for model, record, section in [(Award, self.award, "award"), (Education, self.education, "education"), (Experience, self.experience, "experience")]:
            url = reverse(f"main:delete_{section}", args=[record.id])
            response = self.client.post(url)
            self.assertEqual(response.status_code, 403)
            self.assertTrue(model.objects.filter(pk=record.id).exists())
            self.client.force_login(self.owner)
            self.assertEqual(self.client.post(url).status_code, 302)
            self.assertFalse(model.objects.filter(pk=record.id).exists())
            self.client.force_login(self.regular_user)

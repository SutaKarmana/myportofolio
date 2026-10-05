from django.contrib.auth.models import Permission, User
from django.test import Client, TestCase
from django.urls import reverse
from main.models import Award


class AwardAjaxTest(TestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser('ajax-owner', 'owner@example.com', 'password')
        self.viewer = User.objects.create_user('ajax-viewer')
        self.editor = User.objects.create_user('ajax-editor')
        self.editor.user_permissions.add(Permission.objects.get(codename='change_award'))
        self.award = Award.objects.create(title='Juara Web', issuer='UI', year=2026)
        self.award.liked_by.add(self.viewer)
        self.payload = {'title': 'Baru', 'issuer': 'UI', 'year': 2026}

    def test_public_json_search_and_user_like(self):
        url = reverse('main:get_awards_json')
        data = self.client.get(url).json()['awards'][0]
        self.assertEqual(data['like_count'], 1)
        self.assertFalse(data['is_liked'])
        self.assertEqual(self.client.get(url, {'q': 'Tidak ada'}).json()['awards'], [])
        self.assertEqual(len(self.client.get(url, {'q': 'WEB'}).json()['awards']), 1)
        self.client.force_login(self.viewer)
        self.assertTrue(self.client.get(url).json()['awards'][0]['is_liked'])

    def test_page_is_shell_and_modal_matches_role(self):
        for user in (None, self.viewer, self.editor, self.owner):
            self.client.logout()
            if user:
                self.client.force_login(user)
            response = self.client.get(reverse('main:show_awards'))
            self.assertEqual(response.status_code, 200)
            self.assertNotContains(response, self.award.title)
            self.assertContains(response, 'id="award-grid"')
            if user == self.owner:
                self.assertContains(response, 'id="award-form"')
            else:
                self.assertNotContains(response, 'id="award-form"')

    def test_creation_authorization_validation_and_xss(self):
        url = reverse('main:create_award_ajax')
        for user in (None, self.viewer, self.editor):
            self.client.logout()
            if user:
                self.client.force_login(user)
            response = self.client.post(url, self.payload)
            self.assertEqual(response.status_code, 403)
            self.assertIn('message', response.json())
        self.client.force_login(self.owner)
        self.assertEqual(self.client.get(url).status_code, 405)
        response = self.client.post(url, {**self.payload, 'year': 'invalid'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('year', response.json()['errors'])
        response = self.client.post(url, {**self.payload, 'title': '<img src="x" onerror="alert(1)">'})
        self.assertEqual(response.status_code, 400)
        response = self.client.post(url, {**self.payload, 'title': '<b>Baru</b>', 'issuer': '<i>UI</i>'})
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Award.objects.filter(title='Baru', issuer='UI').exists())
        response = self.client.post(url, {**self.payload, 'certificate_url': 'javascript:alert(1)'})
        self.assertEqual(response.status_code, 400)

    def test_csrf_required(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.owner)
        url = reverse('main:create_award_ajax')
        self.assertEqual(client.post(url, self.payload).status_code, 403)
        client.get(reverse('main:show_awards'))
        token = client.cookies['csrftoken'].value
        response = client.post(url, {**self.payload, 'csrfmiddlewaretoken': token})
        self.assertEqual(response.status_code, 201)

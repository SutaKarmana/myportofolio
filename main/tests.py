from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Award, Education, Experience


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
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Present")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

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
        self.assertContains(response, education.institusi)
        self.assertContains(response, education.program)
        self.assertContains(response, education.description)
        self.assertContains(response, "Sekarang")

    def test_empty_education_page(self):
        response = self.client.get(reverse("main:show_education"))

        self.assertContains(response, "Belum ada riwayat pendidikan yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, self.experience.ended_at.strftime("%B %Y"))
        self.assertNotContains(response, "Present")

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
        self.assertContains(response, award.title)
        self.assertContains(response, award.issuer)
        self.assertContains(response, award.thumbnail)
        self.assertContains(response, award.certificate_url)

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

        self.assertContains(response, "Belum ada penghargaan yang ditambahkan.")
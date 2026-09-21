from django import forms

from main.models import Award, Education, Experience, Project


class ExperienceForm(forms.ModelForm):
    # Tugas 3: ModelForm untuk bagian Experience dengan field yang dapat diisi.
    thumbnail_source = forms.ChoiceField(
        label="Sumber Thumbnail",
        choices=[
            ("url", "Link"),
            ("upload", "Upload file"),
        ],
        widget=forms.RadioSelect,
        initial="url",
        required=False,
    )
    thumbnail_file = forms.FileField(
        label="File Thumbnail",
        required=False,
        widget=forms.ClearableFileInput(attrs={"accept": "image/*"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order_fields(
            [
                "title",
                "description",
                "category",
                "thumbnail_source",
                "thumbnail",
                "thumbnail_file",
            ]
        )

    def clean(self):
        cleaned_data = super().clean()
        source = cleaned_data.get("thumbnail_source") or "url"

        if source == "upload" and not cleaned_data.get("thumbnail_file"):
            self.add_error("thumbnail_file", "Pilih file gambar untuk di-upload.")

        return cleaned_data

    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
        ]

        labels = {
            "title": "Judul Pengalaman",
            "description": "Deskripsi Pengalaman",
            "category": "Kategori",
            "thumbnail": "Link Thumbnail",
        }

        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Asisten Dosen"}),
            "description": forms.Textarea(
                attrs={"placeholder": "Ceritakan pengalamanmu", "rows": 4}
            ),
            "thumbnail": forms.URLInput(
                attrs={
                    "placeholder": "https://example.com/gambar.jpg",
                }
            ),
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "tech_stack",
            "project_url",
            "project_image_url",
        ]

        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "tech_stack": "Teknologi yang Digunakan",
            "project_url": "URL Proyek",
            "project_image_url": "URL Gambar Proyek",
        }

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Ceritakan Proyekmu",
                    "rows": 3,
                }
            ),
            "tech_stack": forms.TextInput(
                attrs={
                    "placeholder": "Django, Python, HTML, CSS",
                }
            ),
            "project_url": forms.URLInput(
                attrs={
                    "placeholder": "https://github.com/username/project",
                }
            ),
            "project_image_url": forms.URLInput(
                attrs={
                    "placeholder": "https://example.com/image.jpg",
                }
            ),
        }


class EducationForm(forms.ModelForm):
    # Form untuk menambah dan mengubah data pendidikan.
    class Meta:
        model = Education
        fields = [
            "institusi",
            "program",
            "description",
            "started_year",
            "ended_year",
            "thumbnail",
        ]
        labels = {
            "institusi": "Nama Institusi",
            "program": "Program Studi",
            "description": "Deskripsi",
            "started_year": "Tahun Mulai",
            "ended_year": "Tahun Selesai",
            "thumbnail": "Link Thumbnail",
        }
        widgets = {
            "institusi": forms.TextInput(attrs={"placeholder": "Universitas Indonesia"}),
            "program": forms.TextInput(attrs={"placeholder": "Sistem Informasi"}),
            "description": forms.Textarea(attrs={"placeholder": "Ceritakan pendidikanmu", "rows": 4}),
            "started_year": forms.NumberInput(attrs={"placeholder": "2023"}),
            "ended_year": forms.NumberInput(attrs={"placeholder": "2027"}),
            "thumbnail": forms.URLInput(attrs={"placeholder": "https://example.com/logo.jpg"}),
        }


class AwardForm(forms.ModelForm):
    # Form untuk menambah dan mengubah data penghargaan.
    class Meta:
        model = Award
        fields = [
            "title",
            "issuer",
            "year",
            "thumbnail",
            "certificate_url",
        ]
        labels = {
            "title": "Nama Penghargaan",
            "issuer": "Pemberi Penghargaan",
            "year": "Tahun",
            "thumbnail": "Link Thumbnail",
            "certificate_url": "Link Sertifikat",
        }
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Juara 1 Business Plan"}),
            "issuer": forms.TextInput(attrs={"placeholder": "Nama Penyelenggara"}),
            "year": forms.NumberInput(attrs={"placeholder": "2025"}),
            "thumbnail": forms.URLInput(attrs={"placeholder": "https://example.com/award.jpg"}),
            "certificate_url": forms.URLInput(attrs={"placeholder": "https://example.com/certificate.pdf"}),
        }
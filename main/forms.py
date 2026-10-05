from django import forms

from django.core.exceptions import ValidationError
from django.utils.html import strip_tags

from main.models import Award, Education, Experience, Project

class ExperienceForm(forms.ModelForm):
    def _clean_text(self, field):
        value = strip_tags(self.cleaned_data[field]).strip()
        if not value:
            raise ValidationError("Isian tidak boleh kosong atau hanya berisi tag HTML.")
        return value

    def clean_title(self):
        return self._clean_text("title")

    def clean_description(self):
        return self._clean_text("description")

    def clean_thumbnail(self):
        value = self.cleaned_data.get("thumbnail")
        if value and not value.lower().startswith(("http://", "https://")):
            raise ValidationError("URL harus menggunakan http:// atau https://.")
        return value

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

    def clean_thumbnail_file(self):
        file = self.cleaned_data.get("thumbnail_file")
        if file:
            header = file.read(12)
            file.seek(0)
            allowed = (
                header.startswith(b"\x89PNG\r\n\x1a\n")
                or header.startswith(b"\xff\xd8\xff")
                or header.startswith((b"GIF87a", b"GIF89a"))
                or (header.startswith(b"RIFF") and header[8:12] == b"WEBP")
            )
            extension = file.name.rsplit(".", 1)[-1].lower()
            if not allowed or extension not in {"png", "jpg", "jpeg", "gif", "webp"}:
                raise ValidationError("Upload hanya menerima gambar PNG, JPG, GIF, atau WebP.")
            if file.size > 5 * 1024 * 1024:
                raise ValidationError("Ukuran gambar maksimal 5 MB.")
        return file

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
    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama proyek tidak boleh hanya berisi tag HTML.")
        return title

    def clean_tech_stack(self):
        value = strip_tags(self.cleaned_data["tech_stack"]).strip()
        if not value:
            raise ValidationError("Teknologi tidak boleh kosong atau hanya berisi HTML.")
        return value

    def clean_description(self):
        value = strip_tags(self.cleaned_data["description"]).strip()
        if not value:
            raise ValidationError("Deskripsi tidak boleh kosong atau hanya berisi HTML.")
        return value

    def _clean_safe_url(self, field_name):
        value = self.cleaned_data.get(field_name)
        if value and not value.lower().startswith(("http://", "https://")):
            raise ValidationError("URL harus menggunakan http:// atau https://.")
        return value

    def clean_project_url(self):
        return self._clean_safe_url("project_url")

    def clean_project_image_url(self):
        return self._clean_safe_url("project_image_url")


class EducationForm(forms.ModelForm):
    def _clean_text(self, field):
        value = strip_tags(self.cleaned_data[field]).strip()
        if not value:
            raise ValidationError("Isian tidak boleh kosong atau hanya berisi tag HTML.")
        return value

    def clean_institusi(self):
        return self._clean_text("institusi")

    def clean_program(self):
        return self._clean_text("program")

    def clean_description(self):
        return self._clean_text("description")

    def clean_thumbnail(self):
        value = self.cleaned_data.get("thumbnail")
        if value and not value.lower().startswith(("http://", "https://")):
            raise ValidationError("URL harus menggunakan http:// atau https://.")
        return value

    def clean(self):
        data = super().clean()
        start, end = data.get("started_year"), data.get("ended_year")
        if start is not None and end is not None and end < start:
            self.add_error("ended_year", "Tahun selesai tidak boleh sebelum tahun mulai.")
        return data

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
    def clean_title(self):
        value = strip_tags(self.cleaned_data["title"]).strip()
        if not value:
            raise ValidationError("Nama penghargaan tidak boleh kosong atau hanya berisi HTML.")
        return value

    def clean_issuer(self):
        value = strip_tags(self.cleaned_data["issuer"]).strip()
        if not value:
            raise ValidationError("Pemberi penghargaan tidak boleh kosong atau hanya berisi HTML.")
        return value

    def _clean_safe_url(self, field):
        value = self.cleaned_data.get(field)
        if value and not value.lower().startswith(("https://", "http://")):
            raise ValidationError("URL harus menggunakan http:// atau https://.")
        return value

    def clean_thumbnail(self):
        return self._clean_safe_url("thumbnail")

    def clean_certificate_url(self):
        return self._clean_safe_url("certificate_url")

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

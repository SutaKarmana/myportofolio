from pathlib import Path
from uuid import uuid4

from django.conf import settings
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.models import Award, Experience, Education, Project
from main.forms import AwardForm, EducationForm, ExperienceForm, ProjectForm

PROFILE_NAME = "I Nyoman Yadnya Suta Karmana"


# Menyimpan thumbnail upload ke static/img lalu mencatat alamatnya pada Experience.
def _save_experience_thumbnail(form, experience):
    source = form.cleaned_data.get("thumbnail_source") or "url"
    thumbnail_file = form.cleaned_data.get("thumbnail_file")

    if source == "upload" and thumbnail_file:
        image_directory = Path(settings.BASE_DIR) / "static" / "img"
        image_directory.mkdir(parents=True, exist_ok=True)
        file_name = f"experience-{uuid4().hex}{Path(thumbnail_file.name).suffix.lower()}"
        file_path = image_directory / file_name

        with file_path.open("wb+") as destination:
            for chunk in thumbnail_file.chunks():
                destination.write(chunk)

        experience.thumbnail = f"/static/img/{file_name}"
    else:
        experience.thumbnail = experience.thumbnail or ""

    experience.save()


def show_main(request):
    # Menyiapkan data profil untuk halaman utama.
    context = {
        "name": PROFILE_NAME,
        "npm": "2506615993",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "An Information Systems student with a strong interest  "
            "An Information Systems student with a strong interest in Data Analytics, currently developing skills in Software Development and Business Development. Enthusiastic about Business Plan Competitions and Data Mining Competition."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    # Tugas 3: mengambil data dalam format JSON
    json_response = get_experience_json(request)
    experiences = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experiences = [experience.object for experience in experiences]

    context = {
        "name": PROFILE_NAME,
        "experience_list": experiences,
    }
    return render(request, "experience.html", context)


def create_experience(request):
    # Tugas 3: membuat data Experience menggunakan form.
    form = ExperienceForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        experience = form.save(commit=False)
        _save_experience_thumbnail(form, experience)
        messages.success(request, "Pengalaman baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        "name": PROFILE_NAME,
        "form": form,
    }
    return render(request, "experience_form.html", context)


def update_experience(request, experience_id):
    # Tugas 3: memperbarui data Experience menggunakan form yang sudah terisi.
    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(
        request.POST or None,
        request.FILES or None,
        instance=experience,
    )

    if request.method == "POST" and form.is_valid():
        experience = form.save(commit=False)
        _save_experience_thumbnail(form, experience)
        messages.success(request, "Pengalaman berhasil diperbarui!")
        return redirect("main:show_experience")

    context = {
        "name": PROFILE_NAME,
        "form": form,
        "experience": experience,
    }
    return render(request, "experience_form.html", context)


def delete_experience(request, experience_id):
    # Tugas 3: menghapus data Experience dari tombol delete pada halaman.
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Pengalaman berhasil dihapus!")

    return redirect("main:show_experience")


def get_experience_json(request):
    # Tugas 3: menyediakan data Experience dalam format JSON.
    experiences = Experience.objects.all()
    experiences_json = serializers.serialize("json", experiences)
    return HttpResponse(experiences_json, content_type="application/json")


def show_education(request):
    # Mengambil semua data pendidikan untuk ditampilkan pada template.
    context = {
        "name": PROFILE_NAME,
        "education_list": Education.objects.all(),
    }
    return render(request, "education.html", context)


def create_education(request):
    # Memproses form untuk menambahkan data pendidikan baru.
    form = EducationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pendidikan baru berhasil ditambahkan!")
        return redirect("main:show_education")

    return render(request, "education_form.html", {"name": PROFILE_NAME, "form": form})


def update_education(request, education_id):
    # Mengisi form dengan data lama untuk proses edit pendidikan.
    education = get_object_or_404(Education, pk=education_id)
    form = EducationForm(request.POST or None, instance=education)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pendidikan berhasil diperbarui!")
        return redirect("main:show_education")

    return render(
        request,
        "education_form.html",
        {"name": PROFILE_NAME, "form": form, "education": education},
    )


def delete_education(request, education_id):
    # Menghapus data pendidikan setelah tombol hapus dikirim melalui POST.
    education = get_object_or_404(Education, pk=education_id)
    if request.method == "POST":
        education.delete()
        messages.success(request, "Pendidikan berhasil dihapus!")
    return redirect("main:show_education")


def show_awards(request):
    # Mengambil data penghargaan sesuai urutan dari model.
    context = {
        "name": PROFILE_NAME,
        "award_list": Award.objects.all(),
    }
    return render(request, "awards.html", context)


def create_award(request):
    # Memproses form untuk menambahkan penghargaan baru.
    form = AwardForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Penghargaan baru berhasil ditambahkan!")
        return redirect("main:show_awards")

    return render(request, "award_form.html", {"name": PROFILE_NAME, "form": form})


def update_award(request, award_id):
    # Mengisi form dengan data lama untuk proses edit penghargaan.
    award = get_object_or_404(Award, pk=award_id)
    form = AwardForm(request.POST or None, instance=award)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Penghargaan berhasil diperbarui!")
        return redirect("main:show_awards")

    return render(
        request,
        "award_form.html",
        {"name": PROFILE_NAME, "form": form, "award": award},
    )


def delete_award(request, award_id):
    # Menghapus data penghargaan setelah tombol hapus dikirim melalui POST.
    award = get_object_or_404(Award, pk=award_id)
    if request.method == "POST":
        award.delete()
        messages.success(request, "Penghargaan berhasil dihapus!")
    return redirect("main:show_awards")


#Tutorial 3

def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": PROFILE_NAME,
        "form": form,
    }
    return render(request, "projects_form.html", context)


def update_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST or None, instance=project)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek berhasil diperbarui!")
        return redirect("main:show_projects")

    context = {
        "name": PROFILE_NAME,
        "form": form,
        "project": project,
    }
    return render(request, "projects_form.html", context)


def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": PROFILE_NAME,
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "project.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")
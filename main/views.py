from django.shortcuts import render
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.models import Award, Experience, Education, Project
from main.forms import ExperienceForm, ProjectForm

PROFILE_NAME = "I Nyoman Yadnya Suta Karmana"

def show_main(request):
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
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
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
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
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
    context = {
        "name": PROFILE_NAME,
        "education_list": Education.objects.all(),
    }
    return render(request, "education.html", context)


def show_awards(request):
    context = {
        "name": PROFILE_NAME,
        "award_list": Award.objects.all(),
    }
    return render(request, "awards.html", context)


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
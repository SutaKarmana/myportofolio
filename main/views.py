from django.shortcuts import render
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.models import Award, Experience, Education,Project
from main.forms import ProjectForm

def show_main(request):
    context = {
        "name": "I Nyoman Yadnya Suta Karmana",
        "npm": "2506615993",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "An Information Systems student with a strong interest  "
            "An Information Systems student with a strong interest in Data Analytics, currently developing skills in Software Development and Business Development. Enthusiastic about Business Plan Competitions and Data Mining Competition."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "I Nyoman Yadnya Suta Karmana",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_education(request):
    context = {
        "name": "I Nyoman Yadnya Suta Karmana",
        "education_list": Education.objects.all(),
    }
    return render(request, "education.html", context)


def show_awards(request):
    context = {
        "name": "I Nyoman Yadnya Suta Karmana",
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
        "name": "Burhan",
        "form": form,
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
        "name": "Burhan",
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
from django.shortcuts import render

from main.models import Award, Experience, Education


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

from pathlib import Path
from uuid import uuid4
import datetime

from django.conf import settings
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required  
from django.core.exceptions import PermissionDenied       
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.urls import reverse

from main.models import Award, Experience, Education, Project
from main.forms import AwardForm, EducationForm, ExperienceForm, ProjectForm

PROFILE_NAME = "I Nyoman Yadnya Suta Karmana"


@login_required(login_url="/login/")
@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403,
        )

    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk": str(project.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

def can_edit_projects(user):
    return user.is_authenticated and (
        user.is_superuser or user.has_perm("main.change_project")
    )

#Tutorial4
def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": PROFILE_NAME,
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": PROFILE_NAME,
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

# Tanpa cek is_superuser: semua akun yang sudah login boleh memberi star
@login_required(login_url="/login/")
@require_POST
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    # Kalau akun ini sudah pernah memberi star, batalkan star-nya.
    # Kalau belum, tambahkan star.
    if request.user in project.starred_by.all():
        project.starred_by.remove(request.user)
    else:
        project.starred_by.add(request.user)

    return redirect("main:show_projects")

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
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": PROFILE_NAME,
        "npm": "2506615993",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "An Information Systems student with a strong interest in Data Analytics, currently developing skills in Software Development and Business Development. Enthusiastic about Business Plan Competitions and Data Mining Competition."
        ),
        "last_login": last_login,
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


@login_required(login_url="/login/")
def create_experience(request):
    # Tugas 3: membuat data Experience menggunakan form.
    if not request.user.is_superuser:
        raise PermissionDenied
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


@login_required(login_url="/login/")
def update_experience(request, experience_id):
    # Tugas 3: memperbarui data Experience menggunakan form yang sudah terisi.
    if not (request.user.is_superuser or request.user.has_perm("main.change_experience")):
        raise PermissionDenied
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


@login_required(login_url="/login/")
@require_POST
def delete_experience(request, experience_id):
    # Tugas 3: menghapus data Experience dari tombol delete pada halaman.
    if not request.user.is_superuser:
        raise PermissionDenied
    experience = get_object_or_404(Experience, pk=experience_id)

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


@login_required(login_url="/login/")
def create_education(request):
    # Memproses form untuk menambahkan data pendidikan baru.
    if not request.user.is_superuser:
        raise PermissionDenied
    form = EducationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pendidikan baru berhasil ditambahkan!")
        return redirect("main:show_education")

    return render(request, "education_form.html", {"name": PROFILE_NAME, "form": form})


@login_required(login_url="/login/")
def update_education(request, education_id):
    # Mengisi form dengan data lama untuk proses edit pendidikan.
    if not (request.user.is_superuser or request.user.has_perm("main.change_education")):
        raise PermissionDenied
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


@login_required(login_url="/login/")
@require_POST
def delete_education(request, education_id):
    # Menghapus data pendidikan setelah tombol hapus dikirim melalui POST.
    if not request.user.is_superuser:
        raise PermissionDenied
    education = get_object_or_404(Education, pk=education_id)
    education.delete()
    messages.success(request, "Pendidikan berhasil dihapus!")
    return redirect("main:show_education")


def show_awards(request):
    # Mengambil data penghargaan sesuai urutan dari model.
    context = {
        "name": PROFILE_NAME,
        "form": AwardForm(),
    }
    return render(request, "awards.html", context)


@require_POST
def create_award_ajax(request):
    # Jangan memakai login_required di sini: AJAX perlu JSON 403, bukan redirect HTML.
    if not request.user.is_authenticated or not request.user.is_superuser:
        return JsonResponse({"message": "Hanya pemilik portofolio dapat menambah penghargaan."}, status=403)
    form = AwardForm(request.POST)
    if not form.is_valid():
        return JsonResponse({"errors": form.errors.get_json_data()}, status=400)
    award = form.save()
    return JsonResponse({"message": "Penghargaan berhasil ditambahkan.", "id": str(award.id)}, status=201)


def get_awards_json(request):
    # Endpoint publik: browser meminta data, lalu Django membalas JSON.
    query = request.GET.get("q", "").strip()
    awards = Award.objects.prefetch_related("liked_by").all()
    if query:
        awards = awards.filter(title__icontains=query)

    data = []
    for award in awards:
        liked_users = list(award.liked_by.all())
        data.append({
            "id": str(award.id),
            "title": award.title,
            "issuer": award.issuer,
            "year": award.year,
            "thumbnail": award.thumbnail or "",
            "certificate_url": award.certificate_url or "",
            "like_count": len(liked_users),
            "is_liked": request.user.is_authenticated and request.user in liked_users,
            "edit_url": reverse("main:update_award", args=[award.id]),
            "delete_url": reverse("main:delete_award", args=[award.id]),
            "like_url": reverse("main:toggle_like", args=[award.id]),
        })
    return JsonResponse({"awards": data})


@login_required(login_url="/login/")
def create_award(request):
    # Memproses form untuk menambahkan penghargaan baru.
    if not request.user.is_superuser:
        raise PermissionDenied
    form = AwardForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Penghargaan baru berhasil ditambahkan!")
        return redirect("main:show_awards")

    return render(request, "award_form.html", {"name": PROFILE_NAME, "form": form})


@login_required(login_url="/login/")
def update_award(request, award_id):
    # Mengisi form dengan data lama untuk proses edit penghargaan.
    if not (request.user.is_superuser or request.user.has_perm("main.change_award")):
        raise PermissionDenied
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


@login_required(login_url="/login/")
@require_POST
def delete_award(request, award_id):
    # Menghapus data penghargaan setelah tombol hapus dikirim melalui POST.
    if not request.user.is_superuser:
        raise PermissionDenied
    award = get_object_or_404(Award, pk=award_id)
    award.delete()
    messages.success(request, "Penghargaan berhasil dihapus!")
    return redirect("main:show_awards")


#Tutorial 3
@login_required(login_url="/login/")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied
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


@login_required(login_url="/login/")
def update_project(request, project_id):
    if not can_edit_projects(request.user):
        raise PermissionDenied

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


#Tutorial 5
def show_projects(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": PROFILE_NAME,
        "title_query": title_query,
        "form": ProjectForm(),
    }
    return render(request, "project.html", context)


from django.http import JsonResponse

#Tutorial 5
def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.prefetch_related('starred_by').all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    # Konstruksi data JSON secara manual agar bisa menyisipkan logika Star
    data = []
    for project in projects:
        starred_users = project.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(project.id),
            "fields": {
                "title": project.title,
                "description": project.description,
                "tech_stack": project.tech_stack,
                "project_url": project.project_url,
                "project_image_url": project.project_image_url,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)

@login_required(login_url="/login/")
@require_POST
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    project = get_object_or_404(Project, pk=project_id)

    project.delete()
    messages.success(request, "Project berhasil dihapus!")
    return redirect("main:show_projects")

    return redirect("main:show_projects")


@login_required(login_url="/login/")
@require_POST
def toggle_like(request, award_id):
    award = get_object_or_404(Award, pk=award_id)

    if request.user in award.liked_by.all():
        award.liked_by.remove(request.user)
    else:
        award.liked_by.add(request.user)

    return redirect("main:show_awards")

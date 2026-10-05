from django.urls import path
from django.contrib import admin
from main.views import (
    create_project_ajax,
    get_education_json,
    create_education_ajax,
    create_experience_ajax,
    show_awards,
    get_awards_json,
    create_award_ajax,
    show_main,
    show_experience,
    create_experience,
    update_experience,
    delete_experience,
    get_experience_json,
    show_education,
    create_education,
    update_education,
    delete_education,
    create_award,
    update_award,
    delete_award,
    show_projects,
    create_project,
    update_project,
    get_projects_json,
    delete_project,
    register,
    login_user,
    logout_user,
    toggle_star,
    toggle_like,
)

app_name = "main"

urlpatterns = [
    path("api/education/", get_education_json, name="get_education_json"),
    path("education/add-ajax/", create_education_ajax, name="create_education_ajax"),
    path("experience/add-ajax/", create_experience_ajax, name="create_experience_ajax"),
    path("admin/", admin.site.urls),
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    # Tugas 3: URL untuk create, update, delete, dan JSON Experience.
    path("experience/add/", create_experience, name="create_experience"),
    path("experience/<uuid:experience_id>/edit/", update_experience, name="update_experience"),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
    path("api/experience/", get_experience_json, name="get_experience_json"),
    
    path("education/", show_education, name="show_education"),
    path("education/add/", create_education, name="create_education"),
    path("education/<uuid:education_id>/edit/", update_education, name="update_education"),
    path("education/<uuid:education_id>/delete/", delete_education, name="delete_education"),
    path("awards/", show_awards, name="show_awards"),
    path("api/awards/", get_awards_json, name="get_awards_json"),
    path("awards/add-ajax/", create_award_ajax, name="create_award_ajax"),
    path("awards/add/", create_award, name="create_award"),
    path("awards/<uuid:award_id>/edit/", update_award, name="update_award"),
    path("awards/<uuid:award_id>/delete/", delete_award, name="delete_award"),
    path("projects/", show_projects, name="show_projects"),
    path("projects/add/", create_project, name="create_project"),
    path("projects/<uuid:project_id>/edit/", update_project, name="update_project"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/<uuid:project_id>/delete/",delete_project,name="delete_project"),

    #tutorial04
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    # Tambahkan path ini ke dalam urlpatterns
    path(
        "projects/<uuid:project_id>/star/",
        toggle_star,
        name="toggle_star",
    ),
    path(
        "awards/<uuid:award_id>/like/",
        toggle_like,
        name="toggle_like",
    ),
    path("projects/add-ajax/", create_project_ajax, name="create_project_ajax"),
]

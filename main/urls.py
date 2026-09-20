from django.urls import path
from django.contrib import admin
from main.views import (
    show_awards,
    show_main,
    show_experience,
    create_experience,
    update_experience,
    delete_experience,
    get_experience_json,
    show_education,
    show_projects,
    create_project,
    get_projects_json,
    delete_project
)

app_name = "main"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("experience/add/", create_experience, name="create_experience"),
    path("experience/<uuid:experience_id>/edit/", update_experience, name="update_experience"),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
    path("api/experience/", get_experience_json, name="get_experience_json"),
    path("education/", show_education, name="show_education"),
    path("awards/", show_awards, name="show_awards"),
    path("projects/", show_projects, name="show_projects"),
    path("projects/add/", create_project, name="create_project"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/<uuid:project_id>/delete/",delete_project,name="delete_project")
]

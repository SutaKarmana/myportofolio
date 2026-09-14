from django.urls import path
from django.contrib import admin
from main.views import show_main, show_experience, show_education

app_name = "main"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("education/", show_education, name="show_education")
]
from django.contrib import admin

from .models import Award, Education, Experience, Project

admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(Award)
admin.site.register(Project)

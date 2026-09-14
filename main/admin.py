from django.contrib import admin

from .models import Award, Education, Experience

admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(Award)

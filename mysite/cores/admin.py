from django.contrib import admin

# Register your models here.

from .models import Job,Core,Layer

admin.site.register([Job,Core,Layer])


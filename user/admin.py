from django.contrib import admin as a

from .models import Profile

a.site.register(Profile)
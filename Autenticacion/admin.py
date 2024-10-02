from django.contrib import admin
from .models import AutenticacionUsuario
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(AutenticacionUsuario, UserAdmin)
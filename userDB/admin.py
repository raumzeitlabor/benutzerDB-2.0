from django.contrib import admin

from .models import *

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)
    list_filter = ("member",)
    readonly_fields = ("pin",)

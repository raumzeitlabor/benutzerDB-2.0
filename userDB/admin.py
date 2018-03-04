from django.contrib import admin

from .models import Profile, MACAddress


class MACInline(admin.StackedInline):
    model = MACAddress


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)
    list_filter = ("member",)
    readonly_fields = ("pin",)
    #inlines = (MACInline,)


@admin.register(MACAddress)
class MACAdressAdmin(admin.ModelAdmin):
    list_display = ("user", "mac", "hostname")

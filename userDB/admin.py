from django.contrib import admin
from .models import *


class MACInline(admin.StackedInline):
    model = MACAddress


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'member')
    list_filter = ('member',)
    readonly_fields = ('pin',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name')


@admin.register(SSHKey)
class SSHKeyAdmin(admin.ModelAdmin):
    readonly_fields = ('hash_md5',)


@admin.register(MACAddress)
class MACAdressAdmin(admin.ModelAdmin):
    list_display = ("user", "mac", "hostname")

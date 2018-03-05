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
    readonly_fields = ('hash_md5', 'key_type')
    list_display = ('profile', 'key_type', 'hash_md5')
    list_filter = ('key_type',)
    search_fields = ('profile__user__username', 'hash_md5', 'key')


@admin.register(MACAddress)
class MACAdressAdmin(admin.ModelAdmin):
    list_display = ('user', 'mac', 'hostname')

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^i18n/setlang/(?P<language>[a-zA-Z\-]+)/', views.switch_language,
        name='switch-language'),
    url('ssh/add/', views.SSHKeyCreate.as_view(), name='ssh-keys-add'),
    url('ssh/(?P<pk>[0-9]+)/delete/', views.SSHKeyDelete.as_view(),
        name='ssh-keys-delete'),
    url('ssh/', views.SSHKeyView.as_view(), name='ssh-keys-list'),
    url('mac/add/', views.MACAddressCreate.as_view(), name='mac-addresses-add'),
    url('mac/(?P<pk>[0-9]+)/delete/', views.MACAddressDelete.as_view(),
        name='mac-addresses-delete'),
    url('mac/', views.MACAddressView.as_view(), name='mac-addresses-list'),
    url('pin/', views.pin_detail, name='pin-detail'),
    # compatibility with old BenutzerDB
    url(r'BenutzerDB/pins/', views.pinpad_pinlist, name='pinpad-pinlist'),
]

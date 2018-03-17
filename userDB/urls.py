#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^i18n/setlang/(?P<language>[a-zA-Z\-]+)/', views.switch_language,
        name='switch-language'),
    url(r'ssh/', views.SSHKeyView.as_view(), name='ssh-keys-list'),
    url(r'mac/', views.MACAddressView.as_view(), name='mac-addresses-list'),
    # compatibility with old BenutzerDB
    url(r'BenutzerDB/pins/', views.pinpad_pinlist, name='pinpad-pinlist'),
]

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'ssh/', views.SSHKeyView.as_view(), name='ssh-keys-list')
]

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.conf.urls import url

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^login$', auth_views.login, name="login"),
    url(r'^logout$', auth_views.logout, name="logout"),
]

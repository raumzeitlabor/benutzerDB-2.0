# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-03-05 00:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userDB', '0008_auto_20180305_0022'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='macaddress',
            options={'ordering': ['user__username'], 'verbose_name': 'MAC address', 'verbose_name_plural': 'MAC addresses'},
        ),
    ]

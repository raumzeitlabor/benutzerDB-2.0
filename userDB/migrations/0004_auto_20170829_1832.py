# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-29 18:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userDB', '0003_auto_20170829_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='pin',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-18 13:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('urlshortener', '0002_auto_20170718_1519'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Urlshortener',
            new_name='Urlshort',
        ),
    ]

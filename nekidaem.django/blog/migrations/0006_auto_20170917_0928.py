# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-17 06:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20170916_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='published',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Опубликовано'),
        ),
    ]

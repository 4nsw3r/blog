# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-16 06:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='subscribes',
            field=models.ManyToManyField(blank=True, to='blog.Profile'),
        ),
    ]

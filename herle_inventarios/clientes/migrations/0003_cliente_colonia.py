# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-13 03:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0002_auto_20160504_0151'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='colonia',
            field=models.CharField(default='', max_length=50),
        ),
    ]

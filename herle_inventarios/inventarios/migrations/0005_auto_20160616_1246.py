# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-16 17:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventarios', '0004_auto_20160609_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventario',
            name='num_rollo',
            field=models.CharField(blank=True, default='', error_messages={'unique': 'El numero de rollo ya existe'}, max_length=30, unique=True),
        ),
    ]
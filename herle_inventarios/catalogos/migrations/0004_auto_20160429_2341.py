# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-29 23:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogos', '0003_auto_20160428_0150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogo',
            name='nombre',
            field=models.CharField(default='', error_messages={'unique': 'El catalogo ya existe'}, max_length=50, unique=True),
        ),
    ]

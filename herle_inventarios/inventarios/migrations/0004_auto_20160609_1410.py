# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-09 19:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventarios', '0003_auto_20160609_1404'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventario',
            old_name='valor_tonelada_pesos',
            new_name='valor_tonelada_dolar',
        ),
    ]

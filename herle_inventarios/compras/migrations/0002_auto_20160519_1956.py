# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-20 00:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='proveedor',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, related_name='compra_id_proveedor', to='proveedores.Proveedor'),
        ),
    ]

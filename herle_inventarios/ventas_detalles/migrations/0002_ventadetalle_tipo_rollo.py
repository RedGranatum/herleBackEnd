# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-12 04:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo_detalles', '0002_auto_20160605_2200'),
        ('ventas_detalles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ventadetalle',
            name='tipo_rollo',
            field=models.ForeignKey(default=b'0150000', on_delete=django.db.models.deletion.PROTECT, related_name='tipoRollo_venta', to='catalogo_detalles.CatalogoDetalle'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-04 03:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras_detalles', '0006_auto_20160629_2216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compradetalle',
            name='precio',
            field=models.DecimalField(decimal_places=4, default=0.0, max_digits=10),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-04 03:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0002_auto_20160519_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='precio_dolar',
            field=models.DecimalField(decimal_places=4, default=0.0, max_digits=18),
        ),
    ]

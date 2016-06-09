# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-06 03:00
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo_detalles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogodetalle',
            name='monto1',
            field=models.DecimalField(decimal_places=4, default=Decimal('0.00'), max_digits=18),
        ),
        migrations.AlterField(
            model_name='catalogodetalle',
            name='monto2',
            field=models.DecimalField(decimal_places=4, default=Decimal('0.00'), max_digits=18),
        ),
    ]
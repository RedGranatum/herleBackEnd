# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-17 01:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='fec_cancelacion',
            field=models.DateField(default='1900-01-01'),
        ),
        migrations.AlterField(
            model_name='venta',
            name='cantidad_pago',
            field=models.IntegerField(default=0, help_text=''),
        ),
    ]

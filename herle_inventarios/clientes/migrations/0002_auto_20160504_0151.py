# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-04 01:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo_detalles', '0001_initial'),
        ('clientes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='banco',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, related_name='cliente_banco', to='catalogo_detalles.CatalogoDetalle'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='calle',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='cliente',
            name='codigo',
            field=models.CharField(default='', error_messages={'unique': 'El codigo del Cliente ya existe'}, max_length=7, unique=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='comentarios',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='cliente',
            name='cp',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AddField(
            model_name='cliente',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='cliente',
            name='estado',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, related_name='cliente_estado', to='catalogo_detalles.CatalogoDetalle'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='nombre',
            field=models.CharField(default='', error_messages={'unique': 'El nombre del Cliente ya existe'}, max_length=100, unique=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='numero',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='cliente',
            name='pais',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, related_name='cliente_pais', to='catalogo_detalles.CatalogoDetalle'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='rfc',
            field=models.CharField(default='', max_length=13),
        ),
        migrations.AddField(
            model_name='cliente',
            name='telefono',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]

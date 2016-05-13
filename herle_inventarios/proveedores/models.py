from django.db import models
from django.core.validators import RegexValidator
from catalogo_detalles.models import CatalogoDetalle


class Proveedor(models.Model):
	codigo  = models.CharField(max_length=7,default="",unique=True,error_messages={'unique':"El codigo del Proveedor ya existe"})
	nombre  = models.CharField(max_length=100, default='', unique=True,error_messages={'unique':"El nombre del Proveedor ya existe"})
	calle   = models.CharField(max_length=200, default='')
	numero  = models.CharField(max_length=50, default='')
	colonia = models.CharField(max_length=50, default='')
	cp      = models.CharField(max_length=10, default = '')
	pais    = models.ForeignKey(CatalogoDetalle,to_field='cdu_catalogo',default='',related_name='proveedor_pais',limit_choices_to={'catalogos': 1}, on_delete=models.PROTECT)						
	estado  = models.ForeignKey(CatalogoDetalle,to_field='cdu_catalogo',default='',related_name='proveedor_estado',limit_choices_to={'catalogos': 2}, on_delete=models.PROTECT)						
	rfc     = models.CharField(max_length=13, default='')
	telefono = models.CharField(max_length=50, blank=True, default='')
	email   = models.EmailField(max_length=50,blank=True, default='')
	comentarios = models.CharField(max_length=200,blank=True,default='') 
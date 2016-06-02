from django.db import models
from catalogo_detalles.models import CatalogoDetalle

class Cliente(models.Model):
	codigo  = models.CharField(max_length=7,default="",unique=True,error_messages={'unique':"El codigo del Cliente ya existe"})
	nombre  = models.CharField(max_length=100, default='', unique=True,error_messages={'unique':"El nombre del Cliente ya existe"})
	calle   = models.CharField(max_length=200, default='')
	numero  = models.CharField(max_length=50, default='')
	colonia = models.CharField(max_length=50, default='')
	cp      = models.CharField(max_length=10, default = '')
	pais    = models.ForeignKey(CatalogoDetalle,to_field='cdu_catalogo',default='',related_name='cliente_pais',limit_choices_to={'catalogos': 1}, on_delete=models.PROTECT)						
	estado  = models.ForeignKey(CatalogoDetalle,to_field='cdu_catalogo',default='',related_name='cliente_estado',limit_choices_to={'catalogos': 2}, on_delete=models.PROTECT)						
	rfc     = models.CharField(max_length=13, default='')
	telefono = models.CharField(max_length=50, blank=True, default='')
	email   = models.EmailField(max_length=50,blank=True, default='')
	banco  = models.ForeignKey(CatalogoDetalle,to_field='cdu_catalogo',default='',related_name='cliente_banco',limit_choices_to={'catalogos': 3}, on_delete=models.PROTECT)						
	comentarios = models.CharField(max_length=200,blank=True,default='') 

	def __str__(self):
		return self.codigo
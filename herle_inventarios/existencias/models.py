from django.db import models
from inventarios.models import Proveedor
from catalogo_detalles.models import CatalogoDetalle

class Existencia(models.Model):
	num_rollo      = models.CharField(max_length=30,default="")
	entrada_kg     = models.DecimalField(max_digits=13, decimal_places=5,default=0.00)
	salida_kg      = models.DecimalField(max_digits=13, decimal_places=5,default=0.00)
	id_operacion   = models.IntegerField(default=0)
	operacion      = models.CharField(max_length=10,default="",blank=True)

	def __str__(self):
		return self.num_rollo
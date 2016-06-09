from django.db import models
from compras.models import Compra
from catalogo_detalles.models import CatalogoDetalle

class CompraDetalle(models.Model):
	compra 	       = models.ForeignKey(Compra,default='',related_name='compra_detalles', on_delete=models.PROTECT)		
	material       = models.ForeignKey(CatalogoDetalle,to_field='cdu_catalogo',default='',related_name='compra_detalles_material',limit_choices_to={'catalogos': 5}, on_delete=models.PROTECT)
	dsc_material   = models.CharField(max_length=100,default="",blank=True)
	calibre        = models.DecimalField(max_digits=4, decimal_places=3,default=0.00)
	ancho          = models.DecimalField(max_digits=5, decimal_places=2,default=0.00)
	largo          = models.IntegerField(default=0)
	peso_kg        = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
	peso_lb        = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
	num_rollo      = models.CharField(max_length=30,default="",blank=True)
	precio         = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)

	def __str__(self):
		return str(self.compra)
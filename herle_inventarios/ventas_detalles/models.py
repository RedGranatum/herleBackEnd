from django.db import models
from django.db import transaction
from ventas.models import Venta
from catalogo_detalles.models import CatalogoDetalle
from existencias.models import Existencia

class VentaDetalle(models.Model):
	venta 	       = models.ForeignKey(Venta,default='',related_name='venta_detalles', on_delete=models.PROTECT)		
	num_rollo      = models.CharField(max_length=30,default="",blank=True)
	peso_kg        = models.DecimalField(max_digits=13, decimal_places=5,default=0.00)
	precio_neto    = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)

	@transaction.atomic
	def save(self, *args, **kwargs):
		super(VentaDetalle, self).save(*args, **kwargs)
	
		existencias = Existencia()
		existencias.num_rollo = self.num_rollo
		existencias.entrada_kg = 0.0
		existencias.salida_kg = self.peso_kg
		existencias.operacion = 'venta'
		existencias.id_operacion = self.id
		existencias.save()

	def __str__(self):
		return str(self.num_rollo)

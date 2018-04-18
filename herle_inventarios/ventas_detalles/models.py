from django.db import models
from django.db import transaction
from django.core.exceptions import ValidationError
from ventas.models import Venta
from catalogo_detalles.models import CatalogoDetalle
from existencias.models import Existencia
from existencias.views import ExistenciaRollo

class VentaDetalle(models.Model):
	venta 	       = models.ForeignKey(Venta,default='',related_name='venta_detalles', on_delete=models.PROTECT)
	num_rollo      = models.CharField(max_length=30,default="",blank=True)
	peso_kg        = models.DecimalField(max_digits=13, decimal_places=5,default=0.00)
	precio_neto    = models.DecimalField(max_digits=13, decimal_places=2,default=0.00)
	tipo_rollo     = models.ForeignKey(CatalogoDetalle,to_field='cdu_catalogo',default='0150000',related_name='tipoRollo_venta',limit_choices_to={'catalogos': 15}, on_delete=models.PROTECT)

	@transaction.atomic
	def save(self, *args, **kwargs):

		self.validarExistencia(self.num_rollo,self.peso_kg)

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

	def validarExistencia(self,num_rollo,salida_kg):
		existencia = ExistenciaRollo()
		cant = existencia.existencias_por_num_rollo(num_rollo)
		if(cant.count()==0):
			raise ValidationError('El numero de rollo no existe')
		exis =  cant[0]['existencia_kg']
		if(exis < self.peso_kg):
			raise ValidationError('No hay existencias disponibles para el rollo ' + self.num_rollo)
		return True


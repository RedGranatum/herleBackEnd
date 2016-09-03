from django.db import models
from clientes.models import Cliente
from catalogo_detalles.models import CatalogoDetalle
#from ventas_detalles.models import VentaDetalle

class Venta(models.Model):
	fec_venta 	   = models.DateField(default='1900-01-01')
	tipo_doc 	   = models.ForeignKey(CatalogoDetalle,to_field='cdu_catalogo',default='',related_name='tipoDoc_venta',limit_choices_to={'catalogos': 10}, on_delete=models.PROTECT)		
	num_documento  = models.CharField(max_length=30,default="",blank=True ,unique=True,error_messages={'unique':"El numero de documento ya existe"})
	bln_activa     = models.BooleanField(default=True)
	fec_inventario = models.DateField(default='1900-01-01')
	cliente 	   = models.ForeignKey(Cliente,default="",related_name='venta_id_cliente', on_delete=models.PROTECT)
	metodo_pago    = models.ForeignKey(CatalogoDetalle,to_field='cdu_catalogo',default='',related_name='metodoPago_venta',limit_choices_to={'catalogos': 11}, on_delete=models.PROTECT)
	banco_cliente  = models.ForeignKey(CatalogoDetalle,to_field='cdu_catalogo',default='',related_name='bancoCliente_venta',limit_choices_to={'catalogos': 3}, on_delete=models.PROTECT)
	periodo_pago   = models.ForeignKey(CatalogoDetalle,to_field='cdu_catalogo',default='',related_name='periodoPago_venta',limit_choices_to={'catalogos': 12}, on_delete=models.PROTECT)
	cantidad_pago  = models.IntegerField(default=0,help_text="")
	observaciones  = models.CharField(max_length=100,default="",blank=True)
	fec_cancelacion = models.DateField(default='1900-01-01')
	empresa         = models.ForeignKey(CatalogoDetalle,to_field='cdu_catalogo',default='0140000',related_name='empresa_venta',limit_choices_to={'catalogos': 14}, on_delete=models.PROTECT) 


	def __str__(self):
		return str(self.id) + '-' + self.num_documento

from django.db import models
from proveedores.models import Proveedor
from catalogo_detalles.models import CatalogoDetalle

class Compra(models.Model):
	invoice 	   = models.CharField(max_length=10,default="",unique=True,error_messages={'unique':"El numero de invoice ya existe"})
	proveedor 	   = models.ForeignKey(Proveedor,related_name='compra_id_proveedor', on_delete=models.PROTECT)		
	fec_solicitud  = models.DateField(default='1900-01-01')
	fec_aduana 	   = models.DateField(default='1900-01-01')
	fec_inventario = models.DateField(default='1900-01-01')
	fec_real 	   = models.DateField(default='1900-01-01')
	casa_cambio    = models.CharField(max_length=30,default="",blank=True)
	precio_dolar   = models.DecimalField(max_digits=5, decimal_places=2,default=0.00)
	tipo_moneda    = models.ForeignKey(CatalogoDetalle,to_field='cdu_catalogo',default='',related_name='compra_tipo_moneda',limit_choices_to={'catalogos': 4}, on_delete=models.PROTECT)
	transporte 	   = models.CharField(max_length=50,default="",blank=True)
	bln_activa     = models.BooleanField(default=True)
	descripcion    = models.CharField(max_length=100,default="",blank=True)
	comentarios    = models.CharField(max_length=100,default="",blank=True)
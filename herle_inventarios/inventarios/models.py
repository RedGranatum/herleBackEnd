from django.db import models
from proveedores.models import Proveedor
from catalogo_detalles.models import CatalogoDetalle
from compras_detalles.models import CompraDetalle

class Inventario(models.Model):
	compra_detalle 		 	= models.ForeignKey(CompraDetalle,default="",related_name='inventario_id_compra_detalle', on_delete=models.PROTECT)		
	invoice_compra 		 	= models.CharField(max_length=10,default="")
	material    			= models.ForeignKey(CatalogoDetalle,to_field='cdu_catalogo',default='',related_name='inventario_detalles_material',limit_choices_to={'catalogos': 5}, on_delete=models.PROTECT)
	calibre        		 	= models.DecimalField(max_digits=4, decimal_places=3,default=0.00)
	ancho          		 	= models.DecimalField(max_digits=5, decimal_places=2,default=0.00)
	largo          		 	= models.IntegerField(default=0)
	codigo_producto		 	= models.CharField(max_length=30,default="")
	num_rollo      		 	= models.CharField(max_length=30,default="",blank=True)
	peso_kg        		 	= models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
	peso_lb        		 	= models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
	transporte 	   		 	= models.CharField(max_length=50,default="",blank=True)
	pais  		   		 	= models.ForeignKey(CatalogoDetalle,to_field='cdu_catalogo',default='',related_name='inventario_pais',limit_choices_to={'catalogos': 1}, on_delete=models.PROTECT)						
	precio_libra   		 	= models.DecimalField(max_digits=18, decimal_places=4,default=0.00)
	factor		   		 	= models.DecimalField(max_digits=18, decimal_places=4,default=0.00)
	precio_dolar   		 	= models.DecimalField(max_digits=18, decimal_places=4,default=0.00)
	factor_impuesto		 	= models.DecimalField(max_digits=18, decimal_places=4,default=0.00)
	con_comercializadora 	= models.BooleanField(default=False)
	factor_kilos		 	= models.DecimalField(max_digits=18, decimal_places=4,default=0.00)
	valor_kilo_dolar	 	= models.DecimalField(max_digits=18, decimal_places=4,default=0.00)
	valor_tonelada_pesos	= models.DecimalField(max_digits=18, decimal_places=4,default=0.00)
	valor_kilo_persos	 	= models.DecimalField(max_digits=18, decimal_places=4,default=0.00)
	valor_final_kilo_pesos	= models.DecimalField(max_digits=18, decimal_places=4,default=0.00)
	descripcion   			= models.CharField(max_length=100,default="",blank=True)
	comentarios    			= models.CharField(max_length=100,default="",blank=True)	

	def __str__(self):
		return self.id + '[' + self.compra_detalle + ']'
from django.db import models
from django.db import transaction
import datetime
from django.core.exceptions import ValidationError
from proveedores.models import Proveedor
from catalogo_detalles.models import CatalogoDetalle
from compras_detalles.models import CompraDetalle
from compras.models import Compra
from existencias.models import Existencia
from inventarios.funciones    import CalculoCodigo,CalculoPrecios,Conversor

class Inventario(models.Model):
	compra_detalle 		 	= models.ForeignKey(CompraDetalle,default="",related_name='inventario_id_compra_detalle', on_delete=models.PROTECT)		
	invoice_compra 		 	= models.CharField(max_length=10,default="")
	material    			= models.ForeignKey(CatalogoDetalle,to_field='cdu_catalogo',default='',related_name='inventario_detalles_material',limit_choices_to={'catalogos': 5}, on_delete=models.PROTECT)
	calibre        		 	= models.DecimalField(max_digits=4, decimal_places=3,default=0.00)
	ancho          		 	= models.DecimalField(max_digits=5, decimal_places=2,default=0.00)
	largo          		 	= models.IntegerField(default=0)
	codigo_producto		 	= models.CharField(max_length=30,default="",blank=False)
	num_rollo      		 	= models.CharField(max_length=30,default="",blank=True,unique=True,error_messages={'unique':"El numero de rollo ya existe"})
	peso_kg        		 	= models.DecimalField(max_digits=13, decimal_places=5,default=0.00)
	peso_lb        		 	= models.DecimalField(max_digits=13, decimal_places=5,default=0.00)
	transporte 	   		 	= models.CharField(max_length=50,default="",blank=True)
	pais  		   		 	= models.ForeignKey(CatalogoDetalle,to_field='cdu_catalogo',default='',related_name='inventario_pais',limit_choices_to={'catalogos': 1}, on_delete=models.PROTECT)						
	precio_libra   		 	= models.DecimalField(max_digits=18, decimal_places=4,default=0.00)
	factor		   		 	= models.DecimalField(max_digits=18, decimal_places=4,default=0.00)
	precio_dolar   		 	= models.DecimalField(max_digits=18, decimal_places=4,default=0.00)
	factor_impuesto		 	= models.DecimalField(max_digits=18, decimal_places=4,default=0.00)
	con_comercializadora 	= models.BooleanField(default=False)
	porc_comercializadora	= models.DecimalField(max_digits=18, decimal_places=4,default=0.00)
	precio_tonelada_dolar	= models.DecimalField(max_digits=18, decimal_places=4,default=0.00)
	factor_kilos		 	= models.DecimalField(max_digits=18, decimal_places=4,default=0.00)
	valor_kilo_dolar	 	= models.DecimalField(max_digits=18, decimal_places=4,default=0.00)
	valor_tonelada_dolar	= models.DecimalField(max_digits=18, decimal_places=4,default=0.00)
	valor_kilo_pesos	 	= models.DecimalField(max_digits=18, decimal_places=4,default=0.00)
	valor_final_kilo_pesos	= models.DecimalField(max_digits=18, decimal_places=4,default=0.00)
	descripcion   			= models.CharField(max_length=100,default="",blank=True)
	comentarios    			= models.CharField(max_length=100,default="",blank=True)	

	@transaction.atomic
	def save(self, *args, **kwargs):

		conversor = Conversor();
		conversor.pais = self.pais.cdu_catalogo
		conversor.kilogramo = self.peso_kg
		conversor.libra = self.peso_lb
		conversor.transformarPorPais()
		self.peso_kg = str(conversor.kilogramo)
		self.peso_lb = str(conversor.libra)
		


		self.validarDetalleCompra()
		calculoCodigos = CalculoCodigo()
		calculoCodigos.calibre = self.calibre
		calculoCodigos.cdu_material = self.material.cdu_catalogo
		calculoCodigos.ancho = self.ancho
		calculoCodigos.largo = self.largo
		codigo = calculoCodigos.generarCodigoProducto()
		self.validarCodigo(codigo)
		
		self.codigo_producto = codigo


		calculo = CalculoPrecios()		
		calculo.cdu_pais = self.pais.cdu_catalogo
		calculo.precio_tonelada_dolar  = self.precio_tonelada_dolar
		calculo.factor_impuesto_china = self.factor_impuesto
		calculo.con_comercializadora  = self.con_comercializadora
		calculo.precio_libra_centavos = self.precio_libra
		calculo.factor = self.factor
		calculo.precio_dolar = self.precio_dolar
		calculo.factor_impuesto = self.factor_impuesto
		calculo.porc_comercializadora = self.porc_comercializadora

		self.valor_kilo_dolar = calculo.kiloEnDolar()
		self.valor_kilo_pesos = calculo.kiloEnPeso()
		self.valor_tonelada_dolar = calculo.ToneladaEnDolar()
		self.valor_final_kilo_pesos = calculo.kiloEnPesosFinal()

		self.validarCalculosPrecio(self.valor_final_kilo_pesos)

		compdet_id = self.compra_detalle.id
		compradet = CompraDetalle.objects.get(id=compdet_id)
		compradet.validado=True
		compradet.save()
		fecha_actual = datetime.datetime.now()
		Compra.objects.filter(id=compradet.compra_id).update(fec_inventario=fecha_actual,fec_real=fecha_actual)
	
		super(Inventario, self).save(*args, **kwargs)
	
		existencias = Existencia()
		existencias.num_rollo = self.num_rollo
		existencias.entrada_kg = self.peso_kg
		existencias.salida_kg = 0.0
		existencias.operacion = 'compra'
		existencias.id_operacion = self.id
		existencias.save()
	
	def validarCodigo(self,codigo_producto):
		if(codigo_producto.strip()==''):
			raise ValidationError('El codigo de producto no puede estar vacio')
		return True

	def validarCalculosPrecio(self,valor_final_kilo_pesos):
		if((self.pais.cdu_catalogo=="0010001" or self.pais.cdu_catalogo=="0010002") and float(valor_final_kilo_pesos) <= 0):
			raise ValidationError('El valor final de kilo en pesos no puede ser 0')
		return True

	def validarDetalleCompra(self):
		# Si si el detalle de la compra no ha sido ya validado
		cantidad =  CompraDetalle.objects.filter(id=self.compra_detalle.id,validado=True).count()
		if(cantidad==1):
			raise ValidationError('Este detalle de compra ya habia sido validado')
		return True

	def __str__(self):
		return str(self.id)
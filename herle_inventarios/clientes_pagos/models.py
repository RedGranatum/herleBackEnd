from django.db import models
from django.db import transaction
import datetime
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Sum
from decimal import *
from ventas.models import Venta
from catalogo_detalles.models import CatalogoDetalle

class ClientesPago(models.Model):
	ventas	   		 	    = models.ForeignKey(Venta,default="",related_name='venta_id_pagos', on_delete=models.PROTECT)		
	fecha  				    = models.DateField(default='1900-01-01')
	cargo    				= models.DecimalField(max_digits=10, decimal_places=2,default=0.0,validators=[MinValueValidator(Decimal('0.00'))])
	abono    				= models.DecimalField(max_digits=10, decimal_places=2,default=0.0,validators=[MinValueValidator(Decimal('0.00'))])
	observaciones    		= models.CharField(max_length=100,default="",blank=True)	

	def save(self, *args, **kwargs):
		self.validarSoloCargo_o_Abono()
		self.validarAbonoNoEsMayorAlSaldo()
		
		super(ClientesPago, self).save(*args, **kwargs)

	def validarSoloCargo_o_Abono(self):
		if(self.cargo > 0 and self.abono>0):
			raise ValidationError('Solo puede exister un cargo o un abono')
		return True

	def validarAbonoNoEsMayorAlSaldo(self):
		qr = ClientesPagoConsultas()
		res = qr.saldo_agrupado_por_venta(self.ventas) 
		if(self.abono > res['saldo']):
			raise ValidationError('El abono no puede ser mayor al saldo de la factura')
		return True

class ClientesPagoConsultas:
	def saldo_agrupado_por_venta(self,venta):
			resultado = ClientesPago.objects.values('ventas').filter(ventas = venta).annotate(cargo_suma=Sum('cargo'),abono_suma=Sum('abono'),saldo=Sum('cargo')-Sum('abono'))
			if(resultado.count() == 0):
				return {'saldo': 0.0}
			return resultado[0]

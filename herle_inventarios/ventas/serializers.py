from rest_framework import serializers
from decimal import *
from .models import Venta
from ventas_detalles.models import VentaDetalle
from clientes_pagos.models import ClientesPago

from ventas_detalles.serializers import VentaDetalleSerializer
from clientes.serializers import ClienteSerializer

class VentaSerializer(serializers.ModelSerializer):
		class Meta:
			model = Venta
			fields = ('id','fec_venta','tipo_doc','num_documento','bln_activa','fec_inventario','cliente','metodo_pago','banco_cliente','periodo_pago','cantidad_pago','observaciones','fec_cancelacion')

class VentaConDetalleNuevaSerializer(serializers.ModelSerializer):
	fec_venta = serializers.DateTimeField(format='%d/%m/%Y',input_formats=['%d/%m/%Y'])
	fec_inventario = serializers.DateTimeField(format='%d/%m/%Y',input_formats=['%d/%m/%Y'])
	fec_cancelacion = serializers.DateTimeField(format='%d/%m/%Y',input_formats=['%d/%m/%Y'])
	

	venta_detalles = VentaDetalleSerializer(many=True)

	class Meta:
		model = Venta
		fields = ('id','fec_venta','tipo_doc','num_documento','bln_activa','fec_inventario','cliente','metodo_pago','banco_cliente','periodo_pago','cantidad_pago','observaciones','venta_detalles','fec_cancelacion')

	def create(self, validated_data):
		venta_detalles_datos = validated_data.pop('venta_detalles')
		venta = Venta.objects.create(**validated_data)
		importe_total = Decimal('0.0')
		for detalle_datos in venta_detalles_datos:
			importe_total = importe_total + (detalle_datos.get('peso_kg') * detalle_datos.get('precio_neto') )
			VentaDetalle.objects.create(venta=venta, **detalle_datos)
		cliente_pago = ClientesPago()
		cliente_pago.ventas = venta
		cliente_pago.fecha = venta.fec_venta
		cliente_pago.cargo = importe_total
		cliente_pago.abono = 0.0
		cliente_pago.observaciones = 'Cargo de la venta'	
		cliente_pago.save()

		return venta

class VentaConDetalleSerializer(serializers.ModelSerializer):
	fec_venta = serializers.DateTimeField(format='%d/%m/%Y',input_formats=['%d/%m/%Y'])
	fec_inventario = serializers.DateTimeField(format='%d/%m/%Y',input_formats=['%d/%m/%Y'])
	fec_cancelacion = serializers.DateTimeField(format='%d/%m/%Y',input_formats=['%d/%m/%Y'])

	venta_detalles = VentaDetalleSerializer(many=True)
	cliente = ClienteSerializer(read_only=False, required=False)

	class Meta:
		model = Venta
		fields = ('id','fec_venta','tipo_doc','num_documento','bln_activa','fec_inventario','cliente','metodo_pago','banco_cliente','periodo_pago','cantidad_pago','observaciones','venta_detalles','fec_cancelacion')

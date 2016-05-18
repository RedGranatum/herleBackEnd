from rest_framework import serializers
from compras.models import Compra
from compras_detalles.models import CompraDetalle
from compras_detalles.serializers import CompraDetalleSerializer

class CompraSerializer(serializers.ModelSerializer):
		fec_solicitud =serializers.DateTimeField(format='%d/%m/%Y',input_formats=['%d/%m/%Y'])
		fec_aduana =serializers.DateTimeField(format='%d/%m/%Y',input_formats=['%d/%m/%Y'])
		fec_inventario =serializers.DateTimeField(format='%d/%m/%Y',input_formats=['%d/%m/%Y'])
		fec_real =serializers.DateTimeField(format='%d/%m/%Y',input_formats=['%d/%m/%Y'])
		
		class Meta:
			model = Compra
			fields = ( 'id','invoice','proveedor','fec_solicitud','fec_aduana',
				'fec_inventario','fec_real','casa_cambio','precio_dolar','tipo_moneda',
				'transporte','bln_activa','descripcion','comentarios',)

class CompraConDetalleSerializer(serializers.ModelSerializer):
	fec_solicitud =serializers.DateTimeField(format='%d/%m/%Y',input_formats=['%d/%m/%Y'])
	fec_aduana =serializers.DateTimeField(format='%d/%m/%Y',input_formats=['%d/%m/%Y'])
	fec_inventario =serializers.DateTimeField(format='%d/%m/%Y',input_formats=['%d/%m/%Y'])
	fec_real =serializers.DateTimeField(format='%d/%m/%Y',input_formats=['%d/%m/%Y'])
	compra_detalles = CompraDetalleSerializer(many=True)

	class Meta:
		model = Compra
		fields = ( 'id','invoice','proveedor','fec_solicitud','fec_aduana',
				'fec_inventario','fec_real','casa_cambio','precio_dolar','tipo_moneda',
				'transporte','bln_activa','descripcion','comentarios','compra_detalles')
		
	def create(self, validated_data):
		compra_detalles_datos = validated_data.pop('compra_detalles')
		compra = Compra.objects.create(**validated_data)
		for detalle_datos in compra_detalles_datos:
			CompraDetalle.objects.create(compra=compra, **detalle_datos)
		return compra

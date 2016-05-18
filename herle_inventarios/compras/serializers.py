from rest_framework import serializers
from compras.models import Compra
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
    compra_detalles = CompraDetalleSerializer(many=True, read_only=True)

    class Meta:
        model = Compra
        fields = ( 'id','invoice','compra_detalles','proveedor','fec_solicitud','fec_aduana',
				'fec_inventario','fec_real','casa_cambio','precio_dolar','tipo_moneda',
				'transporte','bln_activa','descripcion','comentarios',)

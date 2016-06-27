from rest_framework import serializers
from .models import Venta
from ventas_detalles.models import VentaDetalle
from ventas_detalles.serializers import VentaDetalleSerializer
from clientes.serializers import ClienteSerializer

class VentaSerializer(serializers.ModelSerializer):
		class Meta:
			model = Venta
			fields = ('id','fec_venta','tipo_doc','num_documento','bln_activa','fec_inventario','cliente','metodo_pago','banco_cliente','periodo_pago','cantidad_pago','observaciones',)

class VentaConDetalleNuevaSerializer(serializers.ModelSerializer):
	fec_venta = serializers.DateTimeField(format='%d/%m/%Y',input_formats=['%d/%m/%Y'])
	fec_inventario = serializers.DateTimeField(format='%d/%m/%Y',input_formats=['%d/%m/%Y'])
	
	venta_detalles = VentaDetalleSerializer(many=True)

	class Meta:
		model = Venta
		fields = ('id','fec_venta','tipo_doc','num_documento','bln_activa','fec_inventario','cliente','metodo_pago','banco_cliente','periodo_pago','cantidad_pago','observaciones','venta_detalles',)

	def create(self, validated_data):
		venta_detalles_datos = validated_data.pop('venta_detalles')
		venta = Venta.objects.create(**validated_data)
		for detalle_datos in venta_detalles_datos:
			VentaDetalle.objects.create(venta=venta, **detalle_datos)
		return venta

class VentaConDetalleSerializer(serializers.ModelSerializer):
	fec_venta = serializers.DateTimeField(format='%d/%m/%Y',input_formats=['%d/%m/%Y'])
	fec_inventario = serializers.DateTimeField(format='%d/%m/%Y',input_formats=['%d/%m/%Y'])
	venta_detalles = VentaDetalleSerializer(many=True)
	cliente = ClienteSerializer(read_only=False, required=False)

	class Meta:
		model = Venta
		fields = ('id','fec_venta','tipo_doc','num_documento','bln_activa','fec_inventario','cliente','metodo_pago','banco_cliente','periodo_pago','cantidad_pago','observaciones','venta_detalles',)

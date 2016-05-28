from rest_framework import serializers
from compras.models import Compra
from compras_detalles.models import CompraDetalle
from compras_detalles.serializers import CompraDetalleSerializer,CompraDetalleRelacionSerializer,CompraDetalleModificacionSerializer
from proveedores.serializers import ProveedorSerializer

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
	compra_detalles = CompraDetalleRelacionSerializer(many=True)
	#proveedor = serializers.PrimaryKeyRelatedField(read_only=True)
	proveedor = ProveedorSerializer(read_only=False, required=False)

	class Meta:
		model = Compra
		fields = ( 'id','invoice','proveedor','fec_solicitud','fec_aduana',
				'fec_inventario','fec_real','casa_cambio','precio_dolar','tipo_moneda',
				'transporte','bln_activa','descripcion','comentarios','compra_detalles')

	def create(self, validated_data):
		#import ipdb;ipdb.set_trace()
		#validated_data['proveedor_id']=1
		compra_detalles_datos = validated_data.pop('compra_detalles')
		compra = Compra.objects.create(**validated_data)
		for detalle_datos in compra_detalles_datos:
			CompraDetalle.objects.create(compra=compra, **detalle_datos)
		return compra

class CompraConDetalleNuevaSerializer(serializers.ModelSerializer):
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
		#import ipdb;ipdb.set_trace()
		#validated_data['proveedor_id']=1
		compra_detalles_datos = validated_data.pop('compra_detalles')
		compra = Compra.objects.create(**validated_data)
		for detalle_datos in compra_detalles_datos:
			CompraDetalle.objects.create(compra=compra, **detalle_datos)
		return compra

class CompraConDetalleModificacionSerializer(serializers.ModelSerializer):
	fec_solicitud =serializers.DateTimeField(format='%d/%m/%Y',input_formats=['%d/%m/%Y'])
	fec_aduana =serializers.DateTimeField(format='%d/%m/%Y',input_formats=['%d/%m/%Y'])
	fec_inventario =serializers.DateTimeField(format='%d/%m/%Y',input_formats=['%d/%m/%Y'])
	fec_real =serializers.DateTimeField(format='%d/%m/%Y',input_formats=['%d/%m/%Y'])
	compra_detalles = CompraDetalleModificacionSerializer(many=True)

	class Meta:
		model = Compra
		fields = ( 'id','invoice','proveedor','fec_solicitud','fec_aduana',
				'fec_inventario','fec_real','casa_cambio','precio_dolar','tipo_moneda',
				'transporte','bln_activa','descripcion','comentarios','compra_detalles')

	def update(self, instance, validated_data):
			instance.invoice = validated_data.get('invoice', instance.invoice)
			instance.transporte = validated_data.get('transporte', instance.transporte)
			compra_detalles_datos = validated_data.pop('compra_detalles')
			instance.save()
			for detalle_datos in compra_detalles_datos:
				if detalle_datos['id']==-1:
					import ipdb;ipdb.set_trace()
					if 'id' in detalle_datos: del detalle_datos['id']
					CompraDetalle.objects.create(compra=instance, **detalle_datos)
				else:
					pk = detalle_datos['id']
					detalle = CompraDetalle.objects.get(pk=pk)
					detalle.material = detalle_datos["material"]
					detalle.dsc_material = detalle_datos["dsc_material"]
					detalle.save()
					#import ipdb;ipdb.set_trace()
					#detalle_datos["material"]=detalle_datos["material"].cdu_catalogo
					#serializer = CompraDetalleRelacionSerializer(detalle,data=detalle_datos)
					#if serializer.is_valid():
					#	serializer.save()
			return instance

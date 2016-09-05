from rest_framework import serializers
from compras.models import Compra
from compras_detalles.models import CompraDetalle
from compras_detalles.serializers import CompraDetalleSerializer,CompraDetalleRelacionSerializer,CompraDetalleModificacionSerializer
from proveedores.serializers import ProveedorSerializer

class CompraSimpleSerializer(serializers.ModelSerializer):
		fec_solicitud =serializers.DateTimeField(format='%d/%m/%Y',input_formats=['%d/%m/%Y'])
				
		class Meta:
			model = Compra
			fields = ( 'id','invoice','fec_solicitud',)


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
			instance.proveedor = validated_data.get('proveedor', instance.proveedor)
			
			instance.transporte = validated_data.get('transporte', instance.transporte)
			instance.fec_solicitud = validated_data.get('fec_solicitud', instance.fec_solicitud)
			instance.fec_aduana = validated_data.get('fec_aduana', instance.fec_aduana)
			instance.fec_inventario = validated_data.get('fec_inventario', instance.fec_inventario)
			instance.fec_real = validated_data.get('fec_real', instance.fec_real)

			instance.casa_cambio = validated_data.get('casa_cambio', instance.casa_cambio)
			instance.precio_dolar = validated_data.get('precio_dolar', instance.precio_dolar)
			instance.tipo_moneda = validated_data.get('tipo_moneda', instance.tipo_moneda)
			
			instance.bln_activa = validated_data.get('bln_activa', instance.bln_activa)
			instance.descripcion = validated_data.get('descripcion', instance.descripcion)
			instance.comentarios = validated_data.get('comentarios', instance.comentarios)
			
			
			compra_detalles_datos = validated_data.pop('compra_detalles')
			instance.save()
			for detalle_datos in compra_detalles_datos:
				if detalle_datos['id']==-1:
					if 'id' in detalle_datos: del detalle_datos['id']
					CompraDetalle.objects.create(compra=instance, **detalle_datos)
				else:
					pk = detalle_datos['id']
					detalle = CompraDetalle.objects.get(pk=pk)

					detalle.material = detalle_datos["material"]
					detalle.dsc_material = detalle_datos["dsc_material"]
					detalle.calibre = detalle_datos["calibre"]
					detalle.ancho = detalle_datos["ancho"]
					detalle.largo = detalle_datos["largo"]
					detalle.peso_kg = detalle_datos["peso_kg"]
					detalle.peso_lb = detalle_datos["peso_lb"]
					detalle.num_rollo = detalle_datos["num_rollo"]
					detalle.precio = detalle_datos["precio"]
					detalle.save()
			return instance
from rest_framework import serializers
from .models import CompraDetalle
from catalogo_detalles.serializers import CatalogoDetalleSerializer

class CompraDetalleSerializer(serializers.ModelSerializer):		
		class Meta:
			model = CompraDetalle
			fields = ("id","compra","material","dsc_material","calibre","ancho",
				"largo","peso_kg","peso_lb","num_rollo","precio")

class CompraDetalleRelacionSerializer(serializers.ModelSerializer):		
		material = CatalogoDetalleSerializer(read_only=False, required=False)
		class Meta:
			model = CompraDetalle
			fields = ("id","compra","material","dsc_material","calibre","ancho",
				"largo","peso_kg","peso_lb","num_rollo","precio")

class CompraDetalleModificacionSerializer(serializers.ModelSerializer):	
		id = serializers.IntegerField()	
		class Meta:
			model = CompraDetalle
			fields = ("id","compra","material","dsc_material","calibre","ancho",
				"largo","peso_kg","peso_lb","num_rollo","precio")
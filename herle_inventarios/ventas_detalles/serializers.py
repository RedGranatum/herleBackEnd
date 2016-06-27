from rest_framework import serializers
from .models import VentaDetalle
from catalogo_detalles.serializers import CatalogoDetalleSerializer


class VentaDetalleSerializer(serializers.ModelSerializer):		
		class Meta:
			model = VentaDetalle
			fields = ("id","venta","num_rollo","peso_kg","precio_neto",)
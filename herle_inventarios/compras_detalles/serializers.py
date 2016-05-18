from rest_framework import serializers
from .models import CompraDetalle

class CompraDetalleSerializer(serializers.ModelSerializer):		
		class Meta:
			model = CompraDetalle
			fields = ("id","compra","material","dsc_material","calibre","ancho",
				"largo","peso_kg","peso_lb","num_rollo","precio")

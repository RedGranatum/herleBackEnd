from rest_framework import serializers
from .models import Compra

class CompraSerializer(serializers.ModelSerializer):
		class Meta:
			model = Compra
			fields = ( 'id','invoice','proveedor','fec_solicitud','fec_aduana',
				'fec_inventario','fec_real','casa_cambio','precio_dolar','tipo_moneda',
				'transporte','bln_activa','descripcion','comentarios',)

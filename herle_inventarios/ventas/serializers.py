from rest_framework import serializers
from .models import Venta

class VentaSerializer(serializers.ModelSerializer):
		class Meta:
			model = Venta
			fields = ('id','fec_venta','tipo_doc','num_documento','bln_activa','fec_inventario','cliente','metodo_pago','banco_cliente','periodo_pago','cantidad_pago','observaciones',)

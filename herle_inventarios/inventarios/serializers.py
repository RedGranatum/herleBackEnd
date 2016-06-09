from rest_framework import serializers
from .models import Inventario

class InventarioSerializer(serializers.ModelSerializer):		
		class Meta:
			model = Inventario
			fields = ("id","compra_detalle","invoice_compra","material","calibre","ancho","largo",
					  "codigo_producto","num_rollo","peso_kg","peso_lb","transporte","pais",
					  "precio_libra","factor","precio_dolar","factor_impuesto","con_comercializadora",
					   "porc_comercializadora", "factor_kilos","valor_kilo_dolar","valor_tonelada_dolar","valor_kilo_pesos",
					  "valor_final_kilo_pesos","descripcion","comentarios")

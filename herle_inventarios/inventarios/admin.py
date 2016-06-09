from django.contrib import admin
from .models import Inventario
					
class InvetarioAdmin(admin.ModelAdmin):
	list_display =("id","compra_detalle","invoice_compra","material","calibre","ancho","largo",
					  "codigo_producto","num_rollo","peso_kg","peso_lb","transporte","pais",
					  "precio_libra","factor","precio_dolar","factor_impuesto","con_comercializadora",
					  "factor_kilos","valor_kilo_dolar","valor_tonelada_pesos","valor_kilo_persos",
					  "valor_final_kilo_pesos","descripcion","comentarios",)

	search_fields = ('id','compra_detalle','pais') # Campos por los que se puede buscar, si son campos foraneos se usa campo__nomcampoforaneo
	list_filter =('pais',)
	
admin.site.register(Inventario,InvetarioAdmin)
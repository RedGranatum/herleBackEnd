from django.contrib import admin
from .models import VentaDetalle
					
class VentaDetallesAdmin(admin.ModelAdmin):
	list_display =("id","venta","num_rollo","peso_kg","precio_neto",)

	list_filter =('num_rollo',)

admin.site.register(VentaDetalle,VentaDetallesAdmin)


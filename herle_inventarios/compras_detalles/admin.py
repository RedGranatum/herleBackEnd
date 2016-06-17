from django.contrib import admin
from .models import CompraDetalle
					
class ComprasDetallesAdmin(admin.ModelAdmin):
	list_display =("id","compra","material","dsc_material","calibre","ancho",
				"largo","peso_kg","peso_lb","num_rollo","precio","validado",)

	search_fields = ('material','dsc_material',) # Campos por los que se puede buscar, si son campos foraneos se usa campo__nomcampoforaneo
	list_filter =('compra',)
	list_editable = ('validado',)

admin.site.register(CompraDetalle,ComprasDetallesAdmin)
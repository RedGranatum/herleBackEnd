from django.contrib import admin
from .models import CompraDetalle
					
class ComprasDetallesAdmin(admin.ModelAdmin):
	list_display =("id","compra","material","dsc_material","calibre","ancho",
				"largo","peso_kg","peso_lb","num_rollo","precio","validado",)

	search_fields = ('material','dsc_material',) # Campos por los que se puede buscar, si son campos foraneos se usa campo__nomcampoforaneo
	list_filter =('compra',)
	#list_editable = ('invoice',) # Hace el campo editable, (no debe ser el primer campo del list_display)
	#raw_id_fields = ('pais','estado') # Para que me muestre solo el id y si queremos buscarlo por nombre nos pone una lupita

admin.site.register(CompraDetalle,ComprasDetallesAdmin)
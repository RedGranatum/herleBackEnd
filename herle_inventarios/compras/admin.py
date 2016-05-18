from django.contrib import admin
from .models import Compra
					
class ComprasAdmin(admin.ModelAdmin):
	list_display =('id','invoice','proveedor','fec_solicitud','fec_aduana',
				'fec_inventario','fec_real','casa_cambio','precio_dolar','tipo_moneda',
				'transporte','bln_activa','descripcion','comentarios',)

	search_fields = ('invoice','nombre','pais','rfc','email') # Campos por los que se puede buscar, si son campos foraneos se usa campo__nomcampoforaneo
	list_filter =('proveedor',)
	list_editable = ('invoice',) # Hace el campo editable, (no debe ser el primer campo del list_display)
	#raw_id_fields = ('pais','estado') # Para que me muestre solo el id y si queremos buscarlo por nombre nos pone una lupita

admin.site.register(Compra,ComprasAdmin)
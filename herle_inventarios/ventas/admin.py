from django.contrib import admin
from .models import Venta
					
class VentaAdmin(admin.ModelAdmin):
	list_display =('id','empresa','fec_venta','tipo_doc','num_documento','bln_activa','fec_inventario','cliente','metodo_pago','banco_cliente','periodo_pago','cantidad_pago','observaciones','fec_cancelacion')

	search_fields = ('num_documento',) # Campos por los que se puede buscar, si son campos foraneos se usa campo__nomcampoforaneo
	list_filter =('cliente','bln_activa','empresa')
	list_editable = ('bln_activa','tipo_doc',) # Hace el campo editable, (no debe ser el primer campo del list_display)
	#raw_id_fields = ('pais','estado') # Para que me muestre solo el id y si queremos buscarlo por nombre nos pone una lupita

admin.site.register(Venta,VentaAdmin)
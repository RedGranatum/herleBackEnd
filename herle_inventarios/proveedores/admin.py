from django.contrib import admin
from .models import Proveedor
					
class ProveedorAdmin(admin.ModelAdmin):
	list_display =('id','codigo','nombre','calle','numero','cp','pais','estado','rfc','telefono','email','comentarios',)

	search_fields = ('codigo','nombre','pais','rfc','email') # Campos por los que se puede buscar, si son campos foraneos se usa campo__nomcampoforaneo
	list_filter =('pais','estado',)
	list_editable = ('nombre','rfc') # Hace el campo editable, (no debe ser el primer campo del list_display)
	raw_id_fields = ('pais','estado') # Para que me muestre solo el id y si queremos buscarlo por nombre nos pone una lupita

admin.site.register(Proveedor,ProveedorAdmin)
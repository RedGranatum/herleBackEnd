from django.contrib import admin

from .models import CatalogoDetalle

class CatalogoDetalleAdmin(admin.ModelAdmin):
	list_display =('cdu_catalogo','catalogos','num_dcatalogo','descripcion1','descripcion2','monto1','monto2','cdu_default')
	list_filter =('catalogos',)
	search_fields = ('descripcion1',) # Campos por los que se puede buscar, si son campos foraneos se usa campo__nomcampoforaneo
	list_editable = ('catalogos','descripcion1','descripcion2','monto1','monto2','cdu_default') # Hace el campo editable, (no debe ser el primer campo del list_display)

admin.site.register(CatalogoDetalle,CatalogoDetalleAdmin)
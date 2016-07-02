from django.contrib import admin
from .models import ClientesPago
					
class ClientesPagoAdmin(admin.ModelAdmin):
	list_display =('id','ventas','fecha','cargo','abono','observaciones',)

	search_fields = ('ventas','id') # Campos por los que se puede buscar, si son campos foraneos se usa campo__nomcampoforaneo
	list_filter =('ventas',)
	list_editable = ('cargo','abono') # Hace el campo editable, (no debe ser el primer campo del list_display)

admin.site.register(ClientesPago,ClientesPagoAdmin)



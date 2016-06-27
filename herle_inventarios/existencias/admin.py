from django.contrib import admin
from .models import Existencia
					
class ExistenciaAdmin(admin.ModelAdmin):
	list_display =("id","num_rollo","entrada_kg","salida_kg","id_operacion","operacion",)

	search_fields = ('id','num_rollo') # Campos por los que se puede buscar, si son campos foraneos se usa campo__nomcampoforaneo
	list_filter =('operacion',)
	
admin.site.register(Existencia,ExistenciaAdmin)


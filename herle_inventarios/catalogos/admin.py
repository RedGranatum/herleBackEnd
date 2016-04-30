from django.contrib import admin
from .models import Catalogo  

class CatalogoAdmin(admin.ModelAdmin):
	list_display = ('id','nombre') # Campos que se mostraran en el administrador
	#list_filter = ('nombre') # Campos por los que podemos filtrar en el administrador
	#search_fields = ('nombre',)
	#list_editable = ('nombre','editable')
admin.site.register(Catalogo,CatalogoAdmin)
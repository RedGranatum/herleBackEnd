from rest_framework import serializers
from .models import Proveedor

class ProveedorSerializer(serializers.ModelSerializer):
		class Meta:
			model = Proveedor
			fields = ( 'id','codigo','nombre','calle','numero','cp','pais','estado','rfc','telefono','email','comentarios')

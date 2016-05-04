from rest_framework import serializers
from .models import Cliente

class ClienteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Cliente
		fields = ( 'codigo','nombre','calle','numero','cp','pais','estado','rfc','telefono','email','banco','comentarios')

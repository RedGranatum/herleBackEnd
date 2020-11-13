from rest_framework import serializers
from .models import Cliente

class ClienteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Cliente
		fields = ( 'id','codigo','nombre','calle','numero','colonia','cp','pais','estado','rfc','telefono','email','banco','comentarios','limite_credito')

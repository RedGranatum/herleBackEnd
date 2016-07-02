from rest_framework import serializers
from .models import ClientesPago

class ClientesPagoSerializer(serializers.ModelSerializer):
		fecha =serializers.DateTimeField(format='%d/%m/%Y',input_formats=['%d/%m/%Y'])
		class Meta:
			model = ClientesPago
			fields = ('id', 'ventas','fecha','cargo','abono','observaciones',)
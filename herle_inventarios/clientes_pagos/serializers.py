from rest_framework import serializers
from .models import ClientesPago

class ClientesPagoSerializer(serializers.ModelSerializer):
		class Meta:
			model = ClientesPago
			fields = ( 'ventas','fecha','cargo','abono','observaciones',)
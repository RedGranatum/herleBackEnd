from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from django.db.models import Sum
from .models import ClientesPago,ClientesPagoConsultas
from .serializers import ClientesPagoSerializer


class ClientesPagoDetalleMixin(object):
	queryset = ClientesPago.objects.all()
	serializer_class = ClientesPagoSerializer

class ClientesPagoLista(ClientesPagoDetalleMixin, ListCreateAPIView):
	pass

class DetalleCargoAbonoPorVenta(APIView):
	def get(self ,request,venta):
		queryset = ClientesPago.objects.filter(ventas=venta).order_by('id',)
		serializer_class = ClientesPagoSerializer(queryset,many=True)
		return  Response(data=serializer_class.data, status=status.HTTP_201_CREATED)

class SaldoAgrupadoPorVenta(APIView):
	def get(self ,request,venta):
		resultado = ClientesPago.objects.values('ventas').filter(ventas = venta).annotate(cargo_suma=Sum('cargo'),abono_suma=Sum('abono'),saldo=Sum('cargo')-Sum('abono'))
		qr = ClientesPagoConsultas()
		resultado = qr.saldo_agrupado_por_venta(venta)
		return  Response(data=resultado, status=status.HTTP_201_CREATED)


class SaldoAgrupadoPorVentasConAdeudo(APIView):
	def get(self ,request):
		resultado = ClientesPago.objects.values('ventas','ventas__num_documento').annotate(cargo_suma=Sum('cargo'),abono_suma=Sum('abono'),saldo=Sum('cargo')-Sum('abono')).filter(saldo__gt=0)
		return  Response(data=resultado, status=status.HTTP_201_CREATED)


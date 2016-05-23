from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import render
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from compras_detalles.models import CompraDetalle
from compras_detalles.serializers import CompraDetalleSerializer

class CompraDetalleMixin(object):
	queryset = CompraDetalle.objects.all()
	serializer_class = CompraDetalleSerializer

class CompraDetalleLista(CompraDetalleMixin, ListCreateAPIView):
	pass

class CompraDetalleIndividual(CompraDetalleMixin,RetrieveUpdateDestroyAPIView):
	pass


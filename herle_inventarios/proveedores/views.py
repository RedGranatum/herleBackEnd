from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
import django_filters
from rest_framework import filters,generics,status
from rest_framework.response import Response
from rest_framework.views import APIView
from proveedores.models import Proveedor
from proveedores.serializers import ProveedorSerializer


class ProveedorDetalleMixin(object):
	queryset = Proveedor.objects.all()
	serializer_class = ProveedorSerializer

class ProveedorLista(ProveedorDetalleMixin, ListCreateAPIView):
	pass

class ProveedorIndividual(ProveedorDetalleMixin,RetrieveUpdateDestroyAPIView):
	pass

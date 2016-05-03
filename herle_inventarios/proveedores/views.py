from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
import django_filters
from django.db.models import Q
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


class ProveedoreFiltrosMixin(object):
	model = Proveedor
	serializer_class = ProveedorSerializer


class ProveedorBusqueda(ProveedoreFiltrosMixin,ListAPIView):
	def get_queryset(self):
		valor_buscado = self.kwargs['valor_buscado']
		queryset=self.model.objects.filter(Q(codigo__icontains = valor_buscado) | Q(nombre__icontains = valor_buscado) | Q(rfc__icontains = valor_buscado) )
		return queryset

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
import django_filters
from rest_framework import filters,generics,status
from rest_framework.response import Response
from rest_framework.views import APIView
from catalogo_detalles.models import CatalogoDetalle
from catalogo_detalles.serializers import CatalogoDetalleSerializer


class CatalogoDetalleMixin(object):
	queryset = CatalogoDetalle.objects.all()
	serializer_class = CatalogoDetalleSerializer

class CatalogoDetalleLista(CatalogoDetalleMixin, ListCreateAPIView):
	pass

class CatalogoDetalleIndividual(CatalogoDetalleMixin,RetrieveUpdateDestroyAPIView):
	pass
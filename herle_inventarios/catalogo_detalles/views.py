from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
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

class CatalogoDetalleCatalogo(ListAPIView):
	model = CatalogoDetalle
	serializer_class = CatalogoDetalleSerializer

	def get_queryset(self):
		catalogos_id = self.kwargs['catalogos_id']
		queryset = self.model.objects.filter(catalogos=catalogos_id)
		return queryset
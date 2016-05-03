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

class CatalogoDetalleFiltrosMixin(object):
	model = CatalogoDetalle
	serializer_class = CatalogoDetalleSerializer

class CatalogoDetalleCatalogo(CatalogoDetalleFiltrosMixin,ListAPIView):
	def get_queryset(self):
		catalogos_id = self.kwargs['catalogos_id']
		queryset = self.model.objects.filter(catalogos=catalogos_id)
		return queryset

class CatalogoDetallePorCduDefault(CatalogoDetalleFiltrosMixin,ListAPIView):
	def get_queryset(self):
		cdu_default = self.kwargs['cdu_default']
		queryset = self.model.objects.filter(cdu_default=cdu_default)
		return queryset

class CatalogoDetallesFilter(filters.FilterSet):
	valor_buscado = django_filters.CharFilter(name="descripcion1", lookup_type='icontains')
	class Meta:
		model = CatalogoDetalle
		fields = ['valor_buscado']

class CatalogoDetallesBusqueda(generics.ListAPIView):
	queryset = CatalogoDetalle.objects.all()
	serializer_class = CatalogoDetalleSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_class = CatalogoDetallesFilter
	
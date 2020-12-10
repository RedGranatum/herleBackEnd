from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
import django_filters
from rest_framework import filters,generics,status
from rest_framework.response import Response
from rest_framework.views import APIView
from catalogo_detalles.models import CatalogoDetalle
from catalogo_detalles.serializers import CatalogoDetalleSerializer
from rest_framework.permissions import IsAuthenticated

class CatalogoDetalleMasivo(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		datos = request.data;
		serializer = CatalogoDetalleSerializer(data=request.data,many=True)
		if serializer.is_valid():
			try:
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			except IntegrityError as e:
				return Response({"La clave de la empresa ya existe"}, status=status.HTTP_403_FORBIDDEN)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CatalogoDetalleMixin(object):
	permission_classes = (IsAuthenticated,)
	queryset = CatalogoDetalle.objects.all().order_by('catalogos', 'num_dcatalogo')
	serializer_class = CatalogoDetalleSerializer

class CatalogoDetalleLista(CatalogoDetalleMixin, ListCreateAPIView):
	permission_classes = (IsAuthenticated,)
	pass

class CatalogoDetalleIndividual(CatalogoDetalleMixin,RetrieveUpdateDestroyAPIView):
	permission_classes = (IsAuthenticated,)
	pass

class CatalogoDetalleFiltrosMixin(object):
	permission_classes = (IsAuthenticated,)
	model = CatalogoDetalle
	serializer_class = CatalogoDetalleSerializer

class CatalogoDetalleCatalogo(CatalogoDetalleFiltrosMixin,ListAPIView):
	permission_classes = (IsAuthenticated,)
	def get_queryset(self):
		catalogos_id = self.kwargs['catalogos_id']
		queryset = self.model.objects.filter(catalogos=catalogos_id)
		return queryset

class CatalogoDetallePorCduDefault(CatalogoDetalleFiltrosMixin,ListAPIView):
	permission_classes = (IsAuthenticated,)
	def get_queryset(self):
		cdu_default = self.kwargs['cdu_default']
		queryset = self.model.objects.filter(cdu_default=cdu_default)
		return queryset

class CatalogoDetallesFilter(filters.FilterSet):
	permission_classes = (IsAuthenticated,)
	valor_buscado = django_filters.CharFilter(name="descripcion1", lookup_type='icontains')
	class Meta:
		model = CatalogoDetalle
		fields = ['valor_buscado']

class CatalogoDetallesBusqueda(generics.ListAPIView):
	permission_classes = (IsAuthenticated,)
	queryset = CatalogoDetalle.objects.all()
	serializer_class = CatalogoDetalleSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_class = CatalogoDetallesFilter
	
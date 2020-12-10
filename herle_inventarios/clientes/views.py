from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.db.models import Q
from .models import Cliente
from .serializers import ClienteSerializer
from rest_framework.permissions import IsAuthenticated

class ClienteDetalleMixin(object):
	permission_classes = (IsAuthenticated,)
	queryset = Cliente.objects.all()
	serializer_class = ClienteSerializer

class ClienteLista(ClienteDetalleMixin, ListCreateAPIView):
	pass

class ClienteIndividual(ClienteDetalleMixin,RetrieveUpdateDestroyAPIView):
	pass

class ClienteFiltrosMixin(object):
	permission_classes = (IsAuthenticated,)
	model = Cliente
	serializer_class = ClienteSerializer

class ClienteBusqueda(ClienteFiltrosMixin,ListAPIView):
	def get_queryset(self):
		valor_buscado = self.kwargs['valor_buscado']
		queryset=self.model.objects.filter(Q(codigo__icontains = valor_buscado) | Q(nombre__icontains = valor_buscado) | Q(rfc__icontains = valor_buscado) )
		return queryset

from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import render
from django.db.models import Q

from compras.models import Compra
from compras.serializers import CompraSerializer

class CompraDetalleMixin(object):
	queryset = Compra.objects.all()
	serializer_class = CompraSerializer

class CompraLista(CompraDetalleMixin, ListCreateAPIView):
	pass

class CompraIndividual(CompraDetalleMixin,RetrieveUpdateDestroyAPIView):
	pass

class CompraFiltrosMixin(object):
	model = Compra
	serializer_class = CompraSerializer


class CompraBusqueda(CompraFiltrosMixin,ListAPIView):
	def get_queryset(self):
		valor_buscado = self.kwargs['valor_buscado']
		queryset=self.model.objects.filter(Q(invoice__icontains = valor_buscado))
		return queryset

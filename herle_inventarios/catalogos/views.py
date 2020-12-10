from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.exceptions import ValidationError
import django_filters
from rest_framework import filters,generics,status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from catalogos.models import Catalogo
from catalogos.serializers import CatalogoSerializer
from rest_framework.permissions import IsAuthenticated

class CatalogoMixin(object):
	permission_classes = (IsAuthenticated,)
	queryset = Catalogo.objects.all()
	serializer_class = CatalogoSerializer

class CatalogoLista(CatalogoMixin, ListCreateAPIView):
	"""
	Retorna todos los catalogos
				o
	Crea un nuevo catalogo
	"""
	pass

class CatalogoIndividual(CatalogoMixin,RetrieveUpdateDestroyAPIView):
	"""
	Retorna un Catalogo por su pk,
	Modifica un Catalogo por su pk
	Elimina un Catalogo por su pk
	"""
	pass


class CatalogoFilter(filters.FilterSet):
	permission_classes = (IsAuthenticated,)
	valor_buscado = django_filters.CharFilter(name="nombre", lookup_type='icontains')
	class Meta:
		model = Catalogo
		fields = ['valor_buscado']

class CatalogoBusqueda(generics.ListAPIView):
	permission_classes = (IsAuthenticated,)
	queryset = Catalogo.objects.all()
	serializer_class = CatalogoSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_class = CatalogoFilter
	
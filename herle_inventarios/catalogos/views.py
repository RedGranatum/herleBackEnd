from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from catalogos.models import Catalogo
from catalogos.serializers import CatalogoSerializer

# Create your views here.
class CatalogoLista(APIView):
	def get(self, request, format=None):
		catalogo = Catalogo.objects.all()
		serializer = CatalogoSerializer(catalogo, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = CatalogoSerializer(data=request.data)
		if not serializer.is_valid():
			return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
		try:
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		except Exception as e:
			pass
		return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

class CatalogoIndividual(APIView):
	def get_object(self, pk):
		return get_object_or_404(Catalogo, pk=pk)
			
	def get(self, request, pk, format=None):
		catalogo = self.get_object(pk)
		serializer = CatalogoSerializer(catalogo)
		return Response(serializer.data)

	def put(self, request, pk, format=None):
		catalogo = self.get_object(pk)
		serializer = CatalogoSerializer(catalogo, data=request.data)
		if not serializer.is_valid():
			return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
		try:	
			serializer.save()
			return Response(serializer.data)
		except Exception as e:
			pass
		return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		snippet = self.get_object(pk)
		snippet.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class CatalogoBusqueda(APIView):
	def get(self, request, valor_buscado, format=None):
		catalogos = self.busqueda_por_nombre(valor_buscado)
		serializer = CatalogoSerializer(catalogos,many=True)
		return Response(serializer.data)

	def busqueda_por_nombre(self,valor_buscado):
		qs = Catalogo.objects.all()
		for valor in valor_buscado.split():
			qs=qs.filter(Q(nombre__icontains = valor))
		return qs
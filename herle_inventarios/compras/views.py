from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.db import IntegrityError
from django.db.models import Q
from compras.models import Compra
from compras.serializers import CompraSerializer,CompraConDetalleSerializer,CompraConDetalleNuevaSerializer

class CompraMixin(object):
	queryset = Compra.objects.all()
	serializer_class = CompraSerializer

class CompraLista(CompraMixin, ListCreateAPIView):
	pass

class CompraIndividual(CompraMixin,RetrieveUpdateDestroyAPIView):
	pass


class CompraConDetallesMixin(object):
	queryset = Compra.objects.all()
	#queryset =Compra.objects.select_related()
	serializer_class = CompraConDetalleSerializer

class CompraConDetallesNuevaMixin(object):
	queryset = Compra.objects.all()
	#queryset =Compra.objects.select_related()
	serializer_class = CompraConDetalleNuevaSerializer


class CompraConDetallesLista(APIView):
	def get(self, request, pk=None, format=None):
		if(pk!=None):
			print(pk)

		queryset = Compra.objects.all()
		serializer_class = CompraConDetalleNuevaSerializer(queryset,many=True)
		return  Response(serializer_class.data)

	def post(self, request, format=None):
		serializer_class = CompraConDetalleNuevaSerializer(data=request.data)
		serializer_class.is_valid()
		#import ipdb;ipdb.set_trace()
		if serializer_class.is_valid():
			try:
				response = serializer_class.save()
				datos = CompraConDetalleSerializer(response)		
				return Response(datos.data, status=status.HTTP_201_CREATED)
			except IntegrityError as e:
				return Response({"El numero de invoice ya existe"}, status=status.HTTP_403_FORBIDDEN)
		return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

# class CompraConDetallesLista(APIView):
# 	def get(self, request, pk=None, format=None):
# 		compras = Compra.objects.all()
# 		serializer = CompraConDetalleSerializer(compras,many=True)
# 		return Response(serializer.data)

# 	def post(self, request, format=None):
# 		serializer = CompraConDetalleSerializer(data=request.data)
# 		serializer.is_valid()
# 		response = serializer.save()
# 		datos_json = CompraConDetalleSerializer(response)

# 		serializer = CompraConDetalleSerializer(data=request.DATA)
# 		if serializer.is_valid():
# 			try:
# 				serializer.save()
# 				return Response(serializer.data, status=status.HTTP_201_CREATED)
# 			except IntegrityError as e:
# 				return Response({"La clave de la empresa ya existe"}, status=status.HTTP_403_FORBIDDEN)
# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#class CompraConDetalleIndividualMixin(object):
#	queryset =Compra.objects.select_related()
#	serializer_class = CompraConDetalleSerializer


class CompraConDetallesIndividual(CompraConDetallesMixin,RetrieveUpdateDestroyAPIView):
	pass	

class CompraFiltrosMixin(object):
	model = Compra
	serializer_class = CompraSerializer


class CompraBusqueda(CompraFiltrosMixin,ListAPIView):
	def get_queryset(self):
		valor_buscado = self.kwargs['valor_buscado']
		queryset=self.model.objects.filter(Q(invoice__icontains = valor_buscado))
		return queryset

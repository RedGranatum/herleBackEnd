from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.db.models import Q
from django.shortcuts import render
from django.db import IntegrityError
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ventas.models import Venta
from ventas.serializers import VentaSerializer,VentaConDetalleNuevaSerializer,VentaConDetalleSerializer

class VentaConDetallesMixin(object):
	queryset = Venta.objects.all()
	#queryset =Compra.objects.select_related()
	serializer_class = VentaConDetalleSerializer


class VentasConDetallesIndividual(VentaConDetallesMixin,RetrieveUpdateDestroyAPIView):
	pass	

class VentasLista(APIView):	
	def get(self, request, format=None):
		queryset = Venta.objects.all()
		serializer_class = VentaSerializer(queryset,many=True)
		return  Response(serializer_class.data)

	def post(self, request, format=None):
		serializer_class = VentaSerializer(data=request.data)
		if serializer_class.is_valid():
			try:
				serializer_class.save()
				return Response(serializer_class.data, status=status.HTTP_201_CREATED)
			except IntegrityError as ex:
				return Response({"La clave ya existe"}, status=status.HTTP_403_FORBIDDEN)
			except ValidationError as ex:
				return Response({'error': str(ex)}, status=status.HTTP_403_FORBIDDEN)
			except ObjectDoesNotExist as ex:
				return Response({'error': str(ex)}, status=status.HTTP_403_FORBIDDEN)			
			except Exception as ex:				
				return Response({'error': str(ex)}, status=status.HTTP_403_FORBIDDEN)
		return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

class VentaConDetallesLista(APIView):
	def get(self, request, pk=None, format=None):
		if(pk!=None):
			print(pk)

		queryset = Venta.objects.all()
		serializer_class = VentaConDetalleNuevaSerializer(queryset,many=True)
		return  Response(serializer_class.data)

	def post(self, request, format=None):
		serializer_class = VentaConDetalleNuevaSerializer(data=request.data)
		serializer_class.is_valid()
		if serializer_class.is_valid():
			try:
				response = serializer_class.save()
				datos = VentaConDetalleSerializer(response)		
				return Response(datos.data, status=status.HTTP_201_CREATED)
			except IntegrityError as e:
				return Response({'error': str(ex)}, status=status.HTTP_403_FORBIDDEN)
		return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

class VentaFiltrosMixin(object):
	model = Venta
	serializer_class = VentaSerializer

class VentaBusqueda(VentaFiltrosMixin,ListAPIView):
	def get_queryset(self):
		valor_buscado = self.kwargs['valor_buscado']
		queryset=self.model.objects.filter(Q(num_documento__icontains = valor_buscado))
		return queryset

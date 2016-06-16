from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import render
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from inventarios.funciones import CalculoCodigo,CalculoPrecios
from inventarios.serializers import InventarioSerializer
from inventarios.models import Inventario
# Create your views here.

class InventarioMixin(object):
	queryset = Inventario.objects.all()
	serializer_class = InventarioSerializer

class InventarioLista(APIView):
	def get(self, request, pk=None, format=None):
		if(pk!=None):
			print(pk)
		queryset = Inventario.objects.all()
		serializer_class = InventarioSerializer(queryset,many=True)
		return  Response(serializer_class.data)

	def post(self, request, format=None):
		serializer_class = InventarioSerializer(data=request.data)
		serializer_class.is_valid()
		if serializer_class.is_valid():
			try:
				serializer_class.save()
				return Response(serializer_class.data, status=status.HTTP_201_CREATED)
			except IntegrityError as ex:
				return Response({"La clave ya existe"}, status=status.HTTP_403_FORBIDDEN)
			except ValidationError as ex:
				return Response({"Este detalle de compra ya habia sido validado"}, status=status.HTTP_403_FORBIDDEN)
		import ipdb;ipdb.set_trace()
		return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

class CodigoProducto(APIView):
	def get(self, request):
		calibre 	 = request.GET['rango']
		cdu_material = request.GET['cdu_material']
		ancho 		 = request.GET['ancho']
		largo		 = request.GET['largo']
		codigo 		 = self.probarCodigoCalculo(calibre,cdu_material,ancho,largo)
		return  Response(data=codigo, status=status.HTTP_201_CREATED)

	def probarCodigoCalculo(self,calibre,cdu_material,ancho,largo):
		calculoCodigos = CalculoCodigo()
		calculoCodigos.calibre = calibre
		calculoCodigos.cdu_material = cdu_material
		calculoCodigos.ancho = ancho
		calculoCodigos.largo = largo
		codigo = calculoCodigos.generarCodigoProducto()
		return codigo

class CalculoDePrecios(APIView):
	def get(self, request):
		calculo = CalculoPrecios()
		calculo.cdu_pais 			  	= request.GET['cdu_pais']
		calculo.con_comercializadora  	= request.GET['con_comercializadora'] 
		calculo.precio_libra_centavos 	= request.GET['precio_libra_centavos']
		calculo.factor 				 	= request.GET['factor']
		calculo.precio_dolar 			= request.GET['precio_dolar']
		calculo.factor_impuesto 		= request.GET['factor_impuesto']
		calculo.porc_comercializadora 	= request.GET['porc_comercializadora']
		calculo.precio_tonelada_dolar  	= request.GET['precio_tonelada_dolar']
		calculo.factor_impuesto_china 	= request.GET['factor_impuesto_china']
		kilo_en_dolar = calculo.kiloEnDolar()
		kilo_en_pesos = calculo.kiloEnPeso()
		tonelada_en_dolar = calculo.ToneladaEnDolar()
		kilo_en_pesos_final = calculo.kiloEnPesosFinal()
		resultados ={'kilo_en_dolar':kilo_en_dolar,'kilo_en_pesos':kilo_en_pesos,'tonelada_en_dolar': tonelada_en_dolar,'kilo_en_pesos_final':kilo_en_pesos_final}
		return  Response(data=resultados, status=status.HTTP_201_CREATED)
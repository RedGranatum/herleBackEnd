from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from inventarios.funciones import CalculoCodigo
# Create your views here.
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
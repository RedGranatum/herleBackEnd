from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from .models import Existencia

# Create your views here.
#Existencia.objects.filter(num_rollo='AC22').aggregate(Sum('entrada_kg'),Sum('salida_kg'))
#Existencia.objects.values('num_rollo').annotate(entradas_kd=Sum('entrada_kg'),salidas_kg=Sum('salida_kg'))
class ExistenciaRollo(APIView):
	def get(self ,request,num_rollo):
		resultado 		 = self.existencias_por_num_rollo(num_rollo)
		return  Response(data=resultado, status=status.HTTP_201_CREATED)

	def existencias_por_num_rollo(self,num_rollo):
		exist = Existencia.objects.values('num_rollo').filter(num_rollo=num_rollo).annotate(entradas_kd=Sum('entrada_kg'),salidas_kg=Sum('salida_kg'),existencia_kg=Sum('entrada_kg')-Sum('salida_kg'))
		return exist

class ExistenciaAgrupada(APIView):
	def get(self ,request):
		resultado = Existencia.objects.values('num_rollo').annotate(entradas_kd=Sum('entrada_kg'),salidas_kg=Sum('salida_kg'),existencia_kg=Sum('entrada_kg')-Sum('salida_kg'))
		return  Response(data=resultado, status=status.HTTP_201_CREATED)
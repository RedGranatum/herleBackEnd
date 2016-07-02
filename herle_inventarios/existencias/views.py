from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.db.models import Sum
from django.db import connection
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
		cursor = connection.cursor()

		consulta ="""
			select exist.num_rollo as id, exist.num_rollo,inv.codigo_producto,inv.calibre,inv.ancho,
			sum(exist.entrada_kg) as entradas_kg,sum(exist.salida_kg) as salidas_kg,
			sum(exist.entrada_kg) - sum(exist.salida_kg) as existencia_kg
			from existencias_existencia as exist
			join inventarios_inventario as inv on exist.num_rollo = inv.num_rollo
			group by exist.num_rollo,inv.codigo_producto,inv.calibre,inv.ancho
			"""
		cursor.execute(consulta)
		#resultado= cursor.fetchall()
		resultado = self.dictfetchall(cursor)
		#resultado = Existencia.objects.values('num_rollo').annotate(entradas_kd=Sum('entrada_kg'),salidas_kg=Sum('salida_kg'),existencia_kg=Sum('entrada_kg')-Sum('salida_kg'))
		return  Response(data=resultado, status=status.HTTP_201_CREATED)

	def dictfetchall(self,cursor):
		"Return all rows from a cursor as a dict"
		columns = [col[0] for col in cursor.description]
		return [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]

class ExistenciaAgrupadaNumRollo(APIView):
	def get(self ,request,num_rollo):
		resultado = Existencia.objects.values('num_rollo').filter(num_rollo__icontains =num_rollo).annotate(entradas_kd=Sum('entrada_kg'),salidas_kg=Sum('salida_kg'),existencia_kg=Sum('entrada_kg')-Sum('salida_kg'))
		return  Response(data=resultado, status=status.HTTP_201_CREATED)


import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.db.models import Sum
from django.db import connection
from catalogo_detalles.models import CatalogoDetalle
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

		producto = ''
		num_rollo = ''

		if 'producto' in request.GET:
			producto = request.GET['producto']

		if 'num_rollo' in request.GET:
			num_rollo = request.GET['num_rollo']
	
		cursor = connection.cursor()

		columnas ="""
			select exist.num_rollo as id, exist.num_rollo,inv.codigo_producto,inv.calibre,inv.ancho,
			sum(exist.entrada_kg) as entradas_kg,sum(exist.salida_kg) as salidas_kg,
			sum(exist.entrada_kg) - sum(exist.salida_kg) as existencia_kg
			from existencias_existencia as exist
			join inventarios_inventario as inv on exist.num_rollo = inv.num_rollo
			"""
		condicion_por_num_rollo = "where lower(exist.num_rollo) like lower(%s)"	
		
		condicion_por_producto = "where lower(inv.codigo_producto) like lower(%s)"	

		agrupado ="group by exist.num_rollo,inv.codigo_producto,inv.calibre,inv.ancho"

		condicion =""
		valor_busqueda =""

		if(num_rollo != ""):
			valor_busqueda = '%' + num_rollo + '%'
			condicion = condicion_por_num_rollo
		
		if(producto != ""):
			valor_busqueda = '%' + producto + '%'
			condicion = condicion_por_producto

		consulta = columnas + condicion + agrupado

		cursor.execute(consulta,[valor_busqueda])
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

class ExistenciaSobranteRollo(APIView):
	def post(self, request, format=None):
		num_rollo = request.data["num_rollo"]
		det_existencia = Existencia.objects.values('num_rollo').filter(num_rollo=num_rollo).annotate(entradas_kd=Sum('entrada_kg'),salidas_kg=Sum('salida_kg'),existencia_kg=Sum('entrada_kg')-Sum('salida_kg'))
		if(det_existencia.count() == 0):
			mensaje = "No existe el rollo"
			return Response({mensaje}, status=status.HTTP_403_FORBIDDEN)

		existencia_kg = det_existencia[0]['existencia_kg']

		# Revisar en los parametros lo minimo que se puede enviar a desperdicio
		cat = CatalogoDetalle.objects.get(cdu_catalogo="0090008")
		if(existencia_kg<=0):
			mensaje = "No hay existencias para enviar a desperdicios"
			return Response({mensaje}, status=status.HTTP_403_FORBIDDEN)
		if(existencia_kg> cat.monto1):
			mensaje = "Lo maximo que se puede enviar a desperdicios son " + str(cat.monto1) + " kg"
			return Response({mensaje}, status=status.HTTP_403_FORBIDDEN)
	
		nuevo_desperdicio = Existencia(num_rollo=num_rollo ,entrada_kg=0.0, salida_kg=existencia_kg, id_operacion=0 , operacion='sobrantes')
		nuevo_desperdicio.fecha = datetime.datetime.now()
		nuevo_desperdicio.save()
		mensaje = 'Sobrante enviado a desperdicios'
		return Response({mensaje}, status=status.HTTP_403_FORBIDDEN)
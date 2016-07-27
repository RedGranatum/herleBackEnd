from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.db.models import Q
from django.shortcuts import render
from django.db import IntegrityError
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
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

	@transaction.atomic
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

	@transaction.atomic	
	def post(self, request, format=None):
		serializer_class = VentaConDetalleNuevaSerializer(data=request.data)
		if serializer_class.is_valid():
			try:
				response = serializer_class.save()
				datos = VentaConDetalleSerializer(response)		
				return Response(datos.data, status=status.HTTP_201_CREATED)
			except IntegrityError as ex:
				return Response({'error': str(ex)}, status=status.HTTP_403_FORBIDDEN)
			except Exception as ex:
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

class CostosPorNumRollo(APIView):
	def get(self ,request):
		num_rollo = request.GET['num_rollo']

		cursor = connection.cursor()

		columnas ="""
			select  row_number() over() as id,inv.id as inventario_id,inv.codigo_producto,inv.num_rollo,inv.compra_detalle_id,
			inv.peso_lb ,inv.peso_kg as compra_peso_kg,inv.valor_final_kilo_pesos as precio_kg_compra,
			comprac.invoice,comprac.proveedor_id,comprac.fec_real as fec_compra,
			proveedor.codigo as codigo_proveedor,proveedor.nombre as nombre_proveedor,ventad.peso_kg as venta_peso_kg,
			ventad.precio_neto as precio_kg_venta,ventad.venta_id,
			ventac.fec_venta,ventac.num_documento,ventac.bln_activa,ventac.cliente_id,
			cliente.codigo as codigo_cliente,cliente.nombre as nombre_cliente, 
			(ventad.peso_kg * inv.valor_final_kilo_pesos) as precio_neto_compra,
			(ventad.peso_kg * ventad.precio_neto) as precio_neto_venta,
			(ventad.peso_kg * ventad.precio_neto) - (ventad.peso_kg * inv.valor_final_kilo_pesos) as utilidad
			,exist.salidas_kg as total_salida_kg, exist.existencia_kg
			, (exist.existencia_kg * inv.valor_final_kilo_pesos) as costo_inventario
			from inventarios_inventario as inv 
			join compras_detalles_compradetalle as comprad on inv.compra_detalle_id = comprad.id
			join compras_compra as comprac on comprac.id = comprad.compra_id
			join proveedores_proveedor as proveedor on proveedor.id = comprac.proveedor_id
			left join ventas_detalles_ventadetalle  as ventad on ventad.num_rollo = inv.num_rollo
			left join ventas_venta as ventac on ventad.venta_id = ventac.id
			left join clientes_cliente as cliente  on cliente.id = ventac.cliente_id
			left join (
				select  exist.num_rollo,
				sum(exist.entrada_kg) as entradas_kg,sum(exist.salida_kg) as salidas_kg,
				sum(exist.entrada_kg) - sum(exist.salida_kg) as existencia_kg
				from existencias_existencia as exist
				group by exist.num_rollo
				) exist
				on exist.num_rollo = inv.num_rollo
			
			"""
		condicion = ""

		orden =" order by inv.num_rollo,ventac.id"
		
		condicion_por_num_rollo = """
					where lower(inv.num_rollo) = LOWER( %s)
				"""
		if(num_rollo != ""):
			condicion = condicion_por_num_rollo
			consulta = columnas + condicion + orden
			cursor.execute(consulta,[num_rollo])
			resultado = self.dictfetchall(cursor)
			return  Response(data=resultado, status=status.HTTP_201_CREATED)

		consulta = columnas + condicion + orden
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



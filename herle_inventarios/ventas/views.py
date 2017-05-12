from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.db.models import Sum,F,Q
from django.db.models.functions import Coalesce
from django.shortcuts import render
from django.db import IntegrityError
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from ventas.models import Venta
from ventas_detalles.models import VentaDetalle
from existencias.models import Existencia
from catalogo_detalles.models import CatalogoDetalle
from clientes_pagos.models import ClientesPago
from inventarios.models import Inventario
from ventas.serializers import VentaSerializer,VentaConDetalleNuevaSerializer,VentaConDetalleSerializer
import datetime
import json as simplejson
from django.core import serializers

class VentaConDetallesMixin(object):
	queryset = Venta.objects.all()
	#queryset =Compra.objects.select_related()
	serializer_class = VentaConDetalleSerializer


class VentasConDetallesIndividual(VentaConDetallesMixin,RetrieveUpdateDestroyAPIView):
	def retrieve(self, request, *args, **kwargs):
		self.object = self.get_object()
		serializer = self.get_serializer(self.object,context={'open_tok': 'hola'})
		respuesta = Response(serializer.data)
		for det in respuesta.data['venta_detalles']:
			tipo = Inventario.objects.filter(num_rollo = det['num_rollo'])
			det['tipo'] = ''
			if( tipo.count()>0):
				tam = str(tipo[0].largo) if tipo[0].largo>0 else str(tipo[0].calibre) + ' x '  + str(tipo[0].ancho)
				det['tipo']=tipo[0].material.descripcion1 + ' ' + tam + ' ' + det['tipo_rollo']['descripcion1']


		return Response(respuesta.data)

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

class VentasSiguienteNumero(APIView):	
	def get(self, request, format=None):
		cat=CatalogoDetalle.objects.get(cdu_catalogo = request.GET['empresa'])
		cat.monto1 = cat.monto1 + 1
		siguiente = str(int(cat.monto1)) # + cat.descripcion1[0:1]
		#request.data["num_documento"] = siguiente
		return  Response({'Siguiente': siguiente})


class VentaConDetallesLista(APIView):
	def get(self, request, pk=None, format=None):
		if(pk!=None):
			print(pk)

		queryset = Venta.objects.all()
		serializer_class = VentaConDetalleNuevaSerializer(queryset,many=True)
		return  Response(serializer_class.data)

	def post(self, request, format=None):
		if(request.data["num_documento"].isnumeric() == False):
			return Response({'error': 'El Numero de documento debe ser un entero'}, status=status.HTTP_403_FORBIDDEN)

		cat=CatalogoDetalle.objects.get(cdu_catalogo = request.data["empresa"])
		cat.monto1 = request.data["num_documento"]
		siguiente = str(int(cat.monto1))  + cat.descripcion1[0:1]
		request.data["num_documento"] = siguiente

		serializer_class = VentaConDetalleNuevaSerializer(data=request.data)

		if serializer_class.is_valid():
			try:
				with transaction.atomic():
					response = serializer_class.save()
					cat.save()
				datos = VentaConDetalleSerializer(response)
				respuesta = Response(datos.data)
				for det in respuesta.data['venta_detalles']:
					tipo = Inventario.objects.filter(num_rollo = det['num_rollo'])
					det['tipo'] = ''
					if( tipo.count()>0):
						tam = str(tipo[0].largo) if tipo[0].largo>0 else str(tipo[0].calibre) + ' x '  + str(tipo[0].ancho)
						det['tipo']=tipo[0].material.descripcion1 + ' ' + tam + ' ' + det['tipo_rollo']['descripcion1']
				return Response(respuesta.data, status=status.HTTP_201_CREATED)
			except IntegrityError as ex:
				return Response({'error': str(ex)}, status=status.HTTP_403_FORBIDDEN)
			except Exception as ex:
				return Response({'error': str(ex)}, status=status.HTTP_403_FORBIDDEN)
		return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

class VentasIndividual(APIView):

	def get_object(self, pk):
		try:
			return Venta.objects.get(pk=pk)
		except Venta.DoesNotExist:
			raise Http404


	def get(self, request, pk=None, format=None):
		if(pk!=None):
			venta = self.get_object(pk)
			serializer = VentaSerializer(venta)
			return Response(serializer.data)
		queryset = Venta.objects.all()
		serializer_class = VentaSerializer(queryset,many=True)
		return  Response(serializer_class.data)

	@transaction.atomic	
	def put(self, request, pk=None,format=None):
		venta = self.get_object(pk)
		formatmx = "%d/%m/%Y"
		if(venta.bln_activa==False):
			request.data['bln_activa']='false'
			request.data['fec_cancelacion']=venta.fec_cancelacion.strftime(formatmx)
		else:
			num_cancelaciones =  Venta.objects.filter(bln_activa=False).count()
			#import ipdb;ipdb.set_trace()
			request.data['num_documento']=  venta.num_documento + '_C' +  str(num_cancelaciones)
		serializer = VentaSerializer(venta, data =request.data)
		if serializer.is_valid():
			try:
				with transaction.atomic():
					actual_activa = venta.bln_activa
					response = serializer.save()	
					venta_detalles = VentaDetalle.objects.filter(venta = pk)
					#venta_detalles= ClientesPago.objects.filter(ventas = 76)
				
					# Si se va a cancelar una venta que esta activa
					if(actual_activa==True and request.data['bln_activa']=='false'):
						for detalle in venta_detalles:
							nueva_existencia = Existencia(num_rollo=detalle.num_rollo ,entrada_kg=0.0, salida_kg=(detalle.peso_kg*-1), id_operacion=detalle.id , operacion='can.venta')
							nueva_existencia.save()
						#saldo1 = ClientesPago.objects.filter(ventas = 76).aggregate(Sum('cargo', field="sum_cargo"),Sum('abono', field="sum_abono"))
						num_venta = pk
						cargo = ClientesPago.objects.filter(ventas = num_venta).aggregate(Sum('cargo', coalesce=F('sumacargo')) ) or 0
						abono = ClientesPago.objects.filter(ventas = num_venta).aggregate(Sum('abono', coalesce=F('sumabono')) ) or 0
						saldo = (cargo['cargo__sum']  or 0) - (abono['abono__sum'] or 0)
						#saldo = ClientesPago.objects.filter(ventas = pk)
						if saldo > 0:
							#saldo = ClientesPago.objects.get(ventas = venta.id)
							# Hay que sumar el saldo que le queda
							cliente_pago = ClientesPago()
							cliente_pago.ventas = venta
							cliente_pago.fecha = venta.fec_venta
							cliente_pago.cargo = 0.0
							cliente_pago.abono =  saldo
							cliente_pago.observaciones = 'Cancelacion de venta'	
							cliente_pago.save()

				datos = VentaConDetalleSerializer(response)	
				respuesta = Response(datos.data)
				for det in respuesta.data['venta_detalles']:
					tipo = Inventario.objects.filter(num_rollo = det['num_rollo'])
					det['tipo'] = ''
					if( tipo.count()>0):
						tam = str(tipo[0].largo) if tipo[0].largo>0 else str(tipo[0].calibre) + ' x '  + str(tipo[0].ancho)
						det['tipo']=tipo[0].material.descripcion1 + ' ' + tam + ' ' + det['tipo_rollo']['descripcion1']
				return Response(respuesta.data, status=status.HTTP_201_CREATED)
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
			comprac.invoice,comprac.proveedor_id,
			to_char(comprac.fec_real, 'DD-MM-YYYY') as fec_compra,
			proveedor.codigo as codigo_proveedor,proveedor.nombre as nombre_proveedor,ventadc.peso_kg as venta_peso_kg,
			(ventadc.precio_neto ) as precio_kg_venta,ventadc.venta_id,
			to_char(ventadc.fec_venta, 'DD-MM-YYYY') as fec_venta,ventadc.num_documento,ventadc.bln_activa,ventadc.cliente_id,
			cliente.codigo as codigo_cliente,cliente.nombre as nombre_cliente, 
			(ventadc.peso_kg * inv.valor_final_kilo_pesos) as precio_neto_compra,
			((ventadc.peso_kg * ventadc.precio_neto ) ) as precio_neto_venta,
			((ventadc.peso_kg * ventadc.precio_neto )) - (ventadc.peso_kg * inv.valor_final_kilo_pesos) as utilidad
			,exist.salidas_kg as total_salida_kg, exist.existencia_kg
			, (exist.existencia_kg * inv.valor_final_kilo_pesos) as costo_inventario
			from inventarios_inventario as inv 
			join compras_detalles_compradetalle as comprad on inv.compra_detalle_id = comprad.id
			join compras_compra as comprac on comprac.id = comprad.compra_id
			join proveedores_proveedor as proveedor on proveedor.id = comprac.proveedor_id
			left join (
				select ventac.id,ventad.peso_kg,ventad.precio_neto,ventad.venta_id,ventac.fec_venta,ventac.num_documento,
				ventac.bln_activa,ventac.cliente_id,ventad.num_rollo
				from ventas_venta as ventac 
				left join ventas_detalles_ventadetalle as ventad 
				on ventac.id = ventad.venta_id 
				where ventac.bln_activa=true
				) as ventadc on ventadc.num_rollo  = inv.num_rollo
			
			left join clientes_cliente as cliente  on cliente.id = ventadc.cliente_id
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

		orden =" order by inv.num_rollo,ventadc.id"
		
		condicion_por_num_rollo = """
					where lower(inv.num_rollo) like lower( %s)
				"""
		if(num_rollo != ""):
			condicion = condicion_por_num_rollo
			consulta = columnas + condicion + orden
			num_rollo = '%' + num_rollo + '%'
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

class VentasConDetallesInventarioConsulta(APIView):
	def dictfetchall(self,cursor):
		"Return all rows from a cursor as a dict"
		columns = [col[0] for col in cursor.description]
		return [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]

	def get(self ,request):
		num_documento = request.GET['num_documento']
		clave_cliente = request.GET['clave_cliente']

		formatmx = "%d/%m/%Y"
		formateu = "%Y%m%d"
		fec_inicial = datetime.datetime.strptime(request.GET['fec_inicial'], formatmx).strftime(formateu)
		fec_final   = datetime.datetime.strptime(request.GET['fec_final'], formatmx).strftime(formateu)
		
		cursor = connection.cursor()


		columnas_venta =  """
				select  ventac.id,ventac.num_documento,ventac.cliente_id,to_char(ventac.fec_venta, 'DD-MM-YYYY') as fec_venta,ventac.bln_activa,
						clie.nombre as cliente,clie.codigo as cliente_codigo,
						CASE WHEN ventac.bln_activa = true THEN suma_venta.venta_neta ELSE 0 END AS venta_neta,	  
						CASE WHEN ventac.bln_activa = true THEN suma_venta.venta_utilidad ELSE 0 END AS venta_utilidad,	  
						CASE WHEN ventac.bln_activa = true THEN suma_venta.venta_iva ELSE 0 END AS venta_iva,	  
											
						CASE WHEN ventac.bln_activa = true THEN 'VENTA' ELSE 'CANCELADA' END AS estatus,
						"""

		columnas_detalle = """ 				
				ventad.id as id,ventad.id as id_detalle,ventad.venta_id,ventad.num_rollo,ventad.peso_kg,ventad.precio_neto,
						""" 

		columnas_inventario = """ 
				inv.id as inventario_id,inv.codigo_producto as inventario_codigo_producto,
				inv.peso_lb as inventario_peso_lb ,inv.peso_kg as inventario_peso_kg,
				inv.valor_final_kilo_pesos as inventario_precio_kg_compra,
				(ventad.peso_kg * inv.valor_final_kilo_pesos) as total_neto_compra,

				((ventad.peso_kg * ventad.precio_neto )/1.16) as total_neto_venta,
				(((ventad.peso_kg * ventad.precio_neto )/1.16) * 0.16) as iva,
			    ((ventad.peso_kg * ventad.precio_neto ) - (ventad.peso_kg * inv.valor_final_kilo_pesos)) as utilidad
					"""
		#((ventadc.peso_kg * ventadc.precio_neto ) /1.16) as precio_neto_venta,
		union =""" 
				from ventas_venta as ventac 
				left join ventas_detalles_ventadetalle as ventad 
				on ventac.id = ventad.venta_id
				join clientes_cliente as clie on clie.id = ventac.cliente_id
				left join inventarios_inventario as inv 
				on ventad.num_rollo  = inv.num_rollo 
				left join(
				  select ventad.venta_id, 
				  sum( (ventad.peso_kg * ventad.precio_neto)/1.16 ) as venta_neta,
				  sum( ((ventad.peso_kg * ventad.precio_neto) /1.16)* 0.16) as venta_iva,

				  sum( ((ventad.peso_kg * ventad.precio_neto))  - ((ventad.peso_kg) * (inv.valor_final_kilo_pesos)) ) as venta_utilidad				  
				  from ventas_detalles_ventadetalle as ventad
				  left join inventarios_inventario as inv 
				   on ventad.num_rollo  = inv.num_rollo 
				  group by venta_id
				  ) as suma_venta
				  on suma_venta.venta_id = ventac.id

				"""
		condicion_ventas_fecha = """
				where  ventac.fec_venta >= %s and ventac.fec_venta <=%s
				"""

		condicion_ventas_documento = """
					where   lower(ventac.num_documento) = LOWER( %s)
					order by ventac.id,ventad.id
				"""
		#import ipdb;ipdb.set_trace()
		if (clave_cliente != ""):
			condicion_ventas_fecha = condicion_ventas_fecha + " and lower(clie.codigo) = LOWER(%s) "

		condicion_ventas_fecha = condicion_ventas_fecha + " order by ventac.id,ventad.id"
		#clave_cliente = request.GET['clave_cliente']	

		condicion = condicion_ventas_fecha

		if(num_documento != ""):
			condicion = condicion_ventas_documento
			consulta = columnas_venta + columnas_detalle + columnas_inventario + union + condicion
			cursor.execute(consulta,[num_documento])
			resultado = self.dictfetchall(cursor)
			return  Response(data=resultado, status=status.HTTP_201_CREATED)

		consulta = columnas_venta + columnas_detalle + columnas_inventario + union + condicion

		if(clave_cliente != ""):
			cursor.execute(consulta,[fec_inicial,fec_final,clave_cliente])
		else:
			cursor.execute(consulta,[fec_inicial,fec_final])

		resultado = self.dictfetchall(cursor)
		return  Response(data=resultado, status=status.HTTP_201_CREATED)
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from django.db.models import Sum
from django.db import IntegrityError
from django.db import connection
from .models import ClientesPago,ClientesPagoConsultas
from .serializers import ClientesPagoSerializer


# class ClientesPagoDetalleMixin(object):
# 	queryset = ClientesPago.objects.all()
# 	serializer_class = ClientesPagoSerializer

# class ClientesPagoLista(ClientesPagoDetalleMixin, ListCreateAPIView):
# 	pass

class ClientesPagoLista(APIView):
	def get(self, request, pk=None, format=None):
		if(pk!=None):
			print(pk)

		queryset = ClientesPago.objects.all()
		serializer_class = ClientesPagoSerializer(queryset,many=True)
		return  Response(serializer_class.data)

	def post(self, request, format=None):
		serializer_class = ClientesPagoSerializer(data=request.data)
		serializer_class.is_valid()
		if serializer_class.is_valid():
			try:
				serializer_class.save()
				return Response(serializer_class.data, status=status.HTTP_201_CREATED)
			except IntegrityError as ex:
				return Response({'error': str(ex)}, status=status.HTTP_403_FORBIDDEN)
			except Exception as ex:
				return Response({'error': str(ex)}, status=status.HTTP_403_FORBIDDEN)
		return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

class DetalleCargoAbonoPorVenta(APIView):
	def get(self ,request,venta):
		queryset = ClientesPago.objects.filter(ventas=venta).order_by('id',)
		serializer_class = ClientesPagoSerializer(queryset,many=True)
		return  Response(data=serializer_class.data, status=status.HTTP_201_CREATED)

class SaldoAgrupadoPorVenta(APIView):
	def get(self ,request,venta):
		resultado = ClientesPago.objects.values('ventas').filter(ventas = venta).annotate(cargo_suma=Sum('cargo'),abono_suma=Sum('abono'),saldo=Sum('cargo')-Sum('abono'))
		qr = ClientesPagoConsultas()
		resultado = qr.saldo_agrupado_por_venta(venta)
		return  Response(data=resultado, status=status.HTTP_201_CREATED)


class SaldoAgrupadoPorVentasConAdeudo(APIView):
	def get(self ,request):
		resultado = ClientesPago.objects.values('ventas','ventas__num_documento').annotate(cargo_suma=Sum('cargo'),abono_suma=Sum('abono'),saldo=Sum('cargo')-Sum('abono')).filter(saldo__gt=0)
		return  Response(data=resultado, status=status.HTTP_201_CREATED)


class ReporteCalendarioPagos(APIView):
	def dictfetchall(self,cursor):
		"Return all rows from a cursor as a dict"
		columns = [col[0] for col in cursor.description]
		return [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]

	def get(self ,request):		
		cursor = connection.cursor()
		con_saldos = ConsultaSaldos("Detallado")

		consulta = con_saldos.consulta
		cursor.execute(consulta)		
		resultado = self.dictfetchall(cursor)
		return  Response(data=resultado, status=status.HTTP_201_CREATED)

class ReporteAcumuladoCalendarioPagos(APIView):
	def dictfetchall(self,cursor):
		"Return all rows from a cursor as a dict"
		columns = [col[0] for col in cursor.description]
		return [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]

	def get(self ,request):		
		cursor = connection.cursor()
		con_saldos = ConsultaSaldos("Acumulado")

		consulta = con_saldos.consulta
		cursor.execute(consulta)		
		resultado = self.dictfetchall(cursor)
		return  Response(data=resultado, status=status.HTTP_201_CREATED)

class ReporteLimiteCreditoClientes(APIView):
	def dictfetchall(self,cursor):
		"Return all rows from a cursor as a dict"
		columns = [col[0] for col in cursor.description]
		return [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]

	def get(self ,request, cliente):		
		cursor = connection.cursor()
		con_limite = ConsultaLimiteDeCredito(cliente)

		consulta = con_limite.consulta
		cursor.execute(consulta)		
		resultado = self.dictfetchall(cursor)
		return  Response(data=resultado, status=status.HTTP_201_CREATED)


class ConsultaSaldos(object):
	def __init__(self,tipo_reporte):
		self.tipo_reporte=tipo_reporte
		self.consulta = ""

		columnas_venta =  """
			select  ventac.id,ventac.num_documento,ventac.cliente_id,
        	to_char(ventac.fec_venta, 'DD-MM-YYYY') as fec_venta,ventac.cantidad_pago as dias, 
        	to_char(fec_venta +  ventac.cantidad_pago, 'DD-MM-YYYY')  fec_vencimiento,
         	now()::date>= fec_venta +  ventac.cantidad_pago as vencido,
        	ventac.bln_activa,clie.nombre as cliente,clie.codigo as cliente_codigo,
			saldo.cargo,saldo.abono,saldo.saldo,
			CASE WHEN now()::date= (fec_venta +  ventac.cantidad_pago) THEN 'Para hoy'
	             WHEN now()::date> (fec_venta +  ventac.cantidad_pago) THEN 'Vencido'
	             ELSE 'Por Vencer' END as Estatus
			"""
		columnas_total ="select count(ventac.id) as total"	
		
		union =""" 
			from ventas_venta as ventac 
			join clientes_cliente as clie on clie.id = ventac.cliente_id
			join(	
			select ventas_id,sum(cargo) as cargo,sum(abono) as abono,sum(cargo) - sum(abono) as saldo
			from clientes_pagos_clientespago 
			group by ventas_id
			having sum(cargo) - sum(abono)>0
			) as saldo on saldo.ventas_id = ventac.id
				"""

		condicion_ventas = """
			where ventac.bln_activa=true and saldo.saldo>0 
			order by (fec_venta +  ventac.cantidad_pago)
				"""
		condicion_total = """
			where ventac.bln_activa=true and saldo.saldo>0 
			and now()::date >= fec_venta +  ventac.cantidad_pago 
			"""
		if(self.tipo_reporte == "Detallado"):
			self.consulta = columnas_venta + union + condicion_ventas
		if(self.tipo_reporte == "Acumulado"):
			self.consulta = columnas_total + union + condicion_total


class ConsultaLimiteDeCredito(object):
	def __init__(self,id_cliente):
		self.consulta = ""
		self.cliente = id_cliente

		condicion_cliente =  " and v.cliente_id = " + self.cliente + " " if int(self.cliente) >0 else ""

		columnas =  """
			select a.cliente_id, cli.nombre,
			a.cargo,a.abono, a.cargo - a.abono as saldo,
			cli.limite_credito,
			cli.limite_credito - (a.cargo - a.abono) as limite_actual,
			cli.cp, case when (a.cargo - a.abono)>cli.limite_credito then 'Limite' else 'Normal' end as limite
			"""
	
		union ="""
				from(
					select v.cliente_id, sum(cp.cargo) as cargo, sum(cp.abono) as abono
					from clientes_pagos_clientespago as cp
					join ventas_venta as v on v.id = cp.ventas_id
					where v.bln_activa = true
			"""
		union = union  + condicion_cliente 
		
		union = union +	"""group by v.cliente_id 
		        	) as a	join clientes_cliente as cli 
					on cli.id = a.cliente_id
					where (a.cargo - a.abono)>0 
					"""
		self.consulta = columnas + union 

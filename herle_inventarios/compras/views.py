from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.db import IntegrityError
from django.db.models import Q
from django.db import connection
from compras.models import Compra
from compras.serializers import CompraSerializer,CompraSimpleSerializer,CompraConDetalleSerializer,CompraConDetalleNuevaSerializer,CompraConDetalleModificacionSerializer
import datetime
from django.utils.timezone import get_current_timezone

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



class ComprasNoValidadas(APIView):
	def get(self, request,validado='false', format=None):
		inventariado = False
		if(validado == 'true'):
			inventariado = True

		queryset = Compra.objects.filter(compra_detalles__validado=inventariado).distinct('invoice','fec_solicitud')
		serializer_class = CompraSimpleSerializer(queryset,many=True)
		return  Response(serializer_class.data)

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
		if serializer_class.is_valid():
			try:
				response = serializer_class.save()
				datos = CompraConDetalleSerializer(response)		
				return Response(datos.data, status=status.HTTP_201_CREATED)
			except IntegrityError as ex:
				return Response({'error': str(ex)}, status=status.HTTP_403_FORBIDDEN)
		return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

class CompraConDetallesActualizacion(APIView):
	
	def get_object(self, pk):
		try:
			return Compra.objects.get(pk=pk)
		except Compra.DoesNotExist:
			raise Http404

	def get(self, request, pk=None, format=None):
		if(pk!=None):
			compra = self.get_object(pk)
			serializer = CompraConDetalleNuevaSerializer(compra)
			return Response(serializer.data)

		queryset = Compra.objects.all()
		serializer_class = CompraConDetalleNuevaSerializer(queryset,many=True)
		return  Response(serializer_class.data)



	def put(self, request, pk, format=None):  
		id = self.get_object(pk)
		serializer_class = CompraConDetalleModificacionSerializer(id,data=request.data)
		serializer_class.is_valid()
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


class CompraConDetallesInventarioConsulta(APIView):
	def dictfetchall(self,cursor):
		"Return all rows from a cursor as a dict"
		columns = [col[0] for col in cursor.description]
		return [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]

	def get(self ,request):
		modulo  	= request.GET['modulo'] 
		
		#tz = get_current_timezone()
		#fec_inicial = tz.localize(date_object)
		formatmx = "%d/%m/%Y"
		formateu = "%Y%m%d"
		fec_inicial = datetime.datetime.strptime(request.GET['fec_inicial'], formatmx).strftime(formateu)
		fec_final   = datetime.datetime.strptime(request.GET['fec_final'], formatmx).strftime(formateu)
		
		cursor = connection.cursor()


		columnas_compra =  """
				select compra.id as id_compra,  compra.invoice,  to_char( compra.fec_solicitud, 'DD-MM-YYYY') as fec_solicitud,   compra.fec_aduana,   compra.fec_inventario, 
				compra.fec_real, compra.bln_activa,compra.proveedor_id,prove.codigo as proveedor_codigo,prove.nombre as proveedor_nombre,
				prove.pais_id as proveedor_pais_id,cpais.descripcion1 as proveedor_pais, 
						   """
		columnas_detalle = """ 
				detalle.id as id,detalle.id as detalle_id,   detalle.dsc_material  as detalle_dsc_material,   detalle.calibre  as detalle_calibre,   detalle.ancho  as detalle_ancho,   detalle.largo  as detalle_largo,   detalle.peso_kg  as detalle_peso_kg, 
				detalle.peso_lb  as detalle_peso_lb,   detalle.num_rollo  as detalle_num_rollo,   detalle.precio  as detalle_precio, 
				detalle.material_id  as detalle_material_id, cmat1.descripcion1 detalle_material,detalle.validado  as detalle_validado, 
						   """ 
		columnas_inventario = """ 
			  inv.id as inv_id,   inv.calibre as inv_calibre,   inv.invoice_compra as inv_invoice_compra, 
			  inv.ancho as inv_ancho,   inv.largo  as inv_largo,   inv.codigo_producto  as inv_codigo_producto,  
			  inv.num_rollo  as inv_num_rollo,   inv.peso_kg as inv_peso_kg,   inv.peso_lb as inv_peso_lb,  
			  inv.transporte as inv_transporte ,   inv.precio_libra as inv_precio_libra,   inv.factor  as inv_factor,
			  inv.precio_dolar  as inv_precio_dolar,   inv.factor_impuesto as inv_factor_impuesto,  
			  inv.con_comercializadora as inv_con_comercializadora ,   inv.factor_kilos as inv_factor_kilos,   
			  inv.valor_kilo_dolar as inv_valor_kilo_dolar,  inv.valor_tonelada_dolar as inv_valor_tonelada_dolar, 
			  inv.valor_kilo_pesos as inv_valor_kilo_pesos,   inv.valor_final_kilo_pesos as inv_valor_final_kilo_pesos, 
			  inv.material_id as inv_material_id, cmat2.descripcion1 inv_material,
			  inv.porc_comercializadora as inv_porc_comercializadora,   inv.precio_tonelada_dolar as inv_precio_tonelada_dolar,
			  inv.pais_id as inv_pais_id  """
		
		union =""" 
				  from public.compras_compra as compra
				  join compras_detalles_compradetalle as detalle on compra.id = detalle.compra_id
				  left join inventarios_inventario as inv on detalle.id = inv.compra_detalle_id
				  join proveedores_proveedor as prove on prove.id = compra.proveedor_id
				  join catalogo_detalles_catalogodetalle as cmat1 on cmat1.cdu_catalogo = detalle.material_id
				  join catalogo_detalles_catalogodetalle as cmat2 on cmat2.cdu_catalogo = inv.material_id
				  join catalogo_detalles_catalogodetalle as cpais on cpais.cdu_catalogo = prove.pais_id
				"""
		condicion_compras = """
					where compra.fec_solicitud >= %s and compra.fec_solicitud <=%s
					order by compra.id,detalle.id
				"""
		condicion_inventarios = """
					where compra.fec_real >= %s and compra.fec_real <=%s
					order by compra.id,inv.id
				"""
		condicion = condicion_compras

		if(modulo == "inventario"):
			condicion = condicion_inventarios


		consulta = columnas_compra + columnas_detalle + columnas_inventario + union + condicion

		#import ipdb;ipdb.set_trace()
		cursor.execute(consulta,[fec_inicial,fec_final])
		#resultado= cursor.fetchall()
		resultado = self.dictfetchall(cursor)
		#resultado = Existencia.objects.values('num_rollo').annotate(entradas_kd=Sum('entrada_kg'),salidas_kg=Sum('salida_kg'),existencia_kg=Sum('entrada_kg')-Sum('salida_kg'))
		return  Response(data=resultado, status=status.HTTP_201_CREATED)

from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import render
from django.db.models import Q
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from compras_detalles.models import CompraDetalle
from compras_detalles.serializers import CompraDetalleSerializer
from inventarios.models import Inventario
from existencias.models import Existencia

class CompraDetalleMixin(object):
	queryset = CompraDetalle.objects.all()
	serializer_class = CompraDetalleSerializer

class CompraDetalleLista(CompraDetalleMixin, ListCreateAPIView):
	pass

class CompraDetalleIndividual(CompraDetalleMixin,RetrieveUpdateDestroyAPIView):
	pass

class CompraDetalleDesValidar(APIView):
	def get(self, request, pk=None, format=None):
		detalleCompra = CompraDetalle.objects.get(id=pk)
		serializer_class = CompraDetalleSerializer(detalleCompra)
		return  Response(serializer_class.data)

	def delete(self, request, pk, format=None):
		# Quitar la validacion al detalle de la compra
		detalleCompra = CompraDetalle.objects.get(id=pk)
		detalleCompra.validado = False

		# Buscar el registro de inventario de ese detalle
		detalleInventario = Inventario.objects.filter(compra_detalle = detalleCompra.id)
		try:
			with transaction.atomic():
				detalleCompra.save()
				if(detalleInventario.count() > 0):
					detalleInventario = detalleInventario.first()
					# Buscar el registro de entrada de ese numero de rollo
					detalleExistenciaEntrada = Existencia.objects.filter(id_operacion=detalleInventario.id,num_rollo=detalleInventario.num_rollo,operacion='compra')
					if(detalleExistenciaEntrada.count()>0):
						detalleExistenciaEntrada = detalleExistenciaEntrada.first()
						Existencia.objects.get(pk = detalleExistenciaEntrada.id).delete()
					# Borramos el registro de entrada del inventario
					detalleInventario.delete()
				return  Response(status=status.HTTP_204_NO_CONTENT)
		except Exception as ex:
			return Response({'error': str(ex)}, status=status.HTTP_403_FORBIDDEN)

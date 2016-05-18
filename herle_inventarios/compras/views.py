from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import render
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from compras.models import Compra
from compras.serializers import CompraSerializer,CompraConDetalleSerializer

class CompraMixin(object):
	queryset = Compra.objects.all()
	serializer_class = CompraSerializer

class CompraLista(CompraMixin, ListCreateAPIView):
	pass

class CompraIndividual(CompraMixin,RetrieveUpdateDestroyAPIView):
	pass


class CompraConDetallesMixin(object):
	queryset = Compra.objects.all()
	serializer_class = CompraConDetalleSerializer


class CompraConDetallesLista(APIView):
	def get(self, request, pk=None, format=None):
		compras = Compra.objects.all()
		serializer = CompraConDetalleSerializer(compras,many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = CompraConDetalleSerializer(data=request.data)
		serializer.is_valid()
		response = serializer.save()
		datos_json = CompraConDetalleSerializer(response)

		serializer = CompraConDetalleSerializer(data=request.DATA)
		if serializer.is_valid():
			try:
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			except IntegrityError as e:
				return Response({"La clave de la empresa ya existe"}, status=status.HTTP_403_FORBIDDEN)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

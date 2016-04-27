from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from catalogos.models import Catalogo

# Create your views here.
class CatalogoLista(APIView):
	def post(self, request, format=None):
		#import ipdb;ipdb.set_trace()
		catalogo1 = Catalogo()
		catalogo1.nombre ="Proveedores"
		catalogo1.save()
		return Response(request.data,status=status.HTTP_201_CREATED)
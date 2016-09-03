from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.db import IntegrityError
from django.db.models import Q
from django.db import connection
import datetime
from django.utils.timezone import get_current_timezone


from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
 
class PermisoAdministrador(APIView):
	#authentication_classes = (TokenAuthentication,)

	GRUPO_ADMIN = 'Administrador'
	GRUPO_REVISOR = "Revisor"

	def has_permission(self, request, view):
		MENU_PERMISOS = []
		result = request.user and request.user.groups.filter(name=self.GRUPO_ADMIN)
		if result.count()>0:
			MENU_PERMISOS.append("*")
			return MENU_PERMISOS

		result = request.user and request.user.groups.filter(name=self.GRUPO_REVISOR)
		if result.count()>0:
			MENU_PERMISOS.append("Costos")
			return MENU_PERMISOS

		return MENU_PERMISOS

	def get(self, request, format=None):
		permisos = self.has_permission(request,"")
		return Response({"permisos": permisos})
 
class TacView(APIView):
	"""
	Authentication is needed for this methods
	"""
	authentication_classes = (TokenAuthentication,)
	permission_classes = (PermisoAdministrador,)

	def get(self, request, format=None):
		return Response({'detail': "I suppose you are authenticated"})
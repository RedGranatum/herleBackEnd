from django.conf.urls import patterns, url
from ventas import views

urlpatterns =[
	url(r'^ventas/$', views.VentasLista.as_view(),name="ventas_lista"),
]	

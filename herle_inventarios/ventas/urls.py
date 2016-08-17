from django.conf.urls import patterns, url
from ventas import views

urlpatterns =[
	url(r'^ventas/$', views.VentasLista.as_view(),name="ventas_lista"),
	url(r'^ventas/(?P<pk>[0-9]+)/$', views.VentasIndividual.as_view(),name="ventas_individual"),
	url(r'^ventas_con_detalles/$', views.VentaConDetallesLista.as_view(),name="ventas_detalles_lista"),
	url(r'^ventas/(?P<pk>[0-9]+)/detalles/$', views.VentasConDetallesIndividual.as_view(),name='ventas_detalles_individual'), 
    url(r'^ventas/buscar/(?P<valor_buscado>[A-Za-z0-9\s]+)/$', views.VentaBusqueda.as_view(),name='ventas_busqueda'), 
    url(r'^costos/agrupado/$', views.CostosPorNumRollo.as_view(),name="costos_agrupado"),
 
]	

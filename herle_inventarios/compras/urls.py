from django.conf.urls import patterns, url
from compras import views

urlpatterns =[
    url(r'^compras/$', views.CompraLista.as_view(),name="compras_lista"),
	url(r'^compras_con_detalles/$', views.CompraConDetallesIndividual.as_view(),name="compras_detalles_lista"),
	url(r'^compras/(?P<pk>[0-9]+)/$', views.CompraIndividual.as_view(),name='compras_individual'),
	url(r'^compras/(?P<pk>[0-9]+)/detalles/$', views.CompraConDetallesIndividual.as_view(),name='compras_detalles_individual'),
    url(r'^compras/buscar/(?P<valor_buscado>[A-Za-z0-9\s]+)/$', views.CompraBusqueda.as_view(),name='compras_busqueda'), 
	 ]	

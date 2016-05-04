from django.conf.urls import patterns, url
from clientes import views

urlpatterns =[
    url(r'^clientes/$', views.ClienteLista.as_view(),name="clientes_lista"),
	url(r'^clientes/(?P<pk>[0-9]+)/$', views.ClienteIndividual.as_view(),name='clientes_individual'),
    url(r'^clientes/buscar/(?P<valor_buscado>[A-Za-z0-9\s]+)/$', views.ClienteBusqueda.as_view(),name='clientes_busqueda'), 
	 ]	
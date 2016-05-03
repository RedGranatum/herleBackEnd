from django.conf.urls import patterns, url
from django.conf.urls import patterns, url
from proveedores import views

urlpatterns =[
    url(r'^proveedores/$', views.ProveedorLista.as_view(),name="proveedores_lista"),
	url(r'^proveedores/(?P<pk>[0-9]+)/$', views.ProveedorIndividual.as_view(),name='proveedores_individual'),
     url(r'^proveedores/buscar/(?P<valor_buscado>[A-Za-z0-9\s]+)/$', views.ProveedorBusqueda.as_view(),name='proveedores_busqueda'), 
	 ]	
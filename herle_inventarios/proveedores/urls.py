from django.conf.urls import patterns, url
from django.conf.urls import patterns, url
from proveedores import views

urlpatterns =[
    url(r'^proveedores/$', views.ProveedorLista.as_view(),name="proveedores_lista"),
	url(r'^proveedores/(?P<pk>[0-9]+)/$', views.ProveedorIndividual.as_view(),name='proveedores_individual'),
	 #url(r'^catalogos/buscar/$', views.CatalogoBusqueda.as_view(),name='catalogos_busqueda'), 
	 ]	
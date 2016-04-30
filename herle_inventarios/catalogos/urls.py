from django.conf.urls import patterns, url
from django.conf.urls import patterns, url
from catalogos import views

urlpatterns =[
    url(r'^catalogos/$', views.CatalogoLista.as_view(),name="catalogos_lista"),
	 url(r'^catalogos/(?P<pk>[0-9]+)/$', views.CatalogoIndividual.as_view(),name='catalogos_individual'),
	 url(r'^catalogos/buscar/$', views.CatalogoBusqueda.as_view(),name='catalogos_busqueda'), 
	 ]	
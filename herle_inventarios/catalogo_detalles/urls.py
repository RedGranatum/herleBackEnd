from django.conf.urls import patterns, url
from django.conf.urls import patterns, url
from catalogo_detalles import views

urlpatterns =[
	 url(r'^catalogo_detalles/$', views.CatalogoDetalleLista.as_view(),name="catalogodetalle_lista"),
	 url(r'^catalogo_detalles/(?P<pk>[0-9]+)/$', views.CatalogoDetalleIndividual.as_view(),name='catalogodetalle_individual'),
	 url(r'^catalogos/(?P<catalogos_id>[0-9]+)/catalogo_detalles/$', views.CatalogoDetalleCatalogo.as_view(),name='catalogodetalle_individual'),
	 url(r'^catalogo_detalles/(?P<cdu_default>[0-9]+)/catalogo_detalles/$', views.CatalogoDetallePorCduDefault.as_view(),name='catalogodetalle_por_cdu_default'),
	 url(r'^catalogo_detalles/buscar/$', views.CatalogoDetallesBusqueda.as_view(),name='catalogo_detalles_busqueda'), 
	 ]	
	 
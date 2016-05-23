from django.conf.urls import patterns, url
from compras_detalles import views

urlpatterns =[
    url(r'^compras_detalles/$', views.CompraDetalleLista.as_view(),name="compras_detalles_lista"),
	url(r'^compras_detalles/(?P<pk>[0-9]+)/$', views.CompraDetalleIndividual.as_view(),name='compras_detalles_individual'),
]	

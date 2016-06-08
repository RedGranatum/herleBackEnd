from django.conf.urls import patterns, url
from inventarios import views

urlpatterns =[
    url(r'^inventarios/codigo_producto/$', views.CodigoProducto.as_view(),name="inventario_codigo_producto"),
]	

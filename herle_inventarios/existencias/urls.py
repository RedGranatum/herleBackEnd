from django.conf.urls import patterns, url
from existencias import views

urlpatterns =[
   url(r'^existencias/num_rollo/(?P<num_rollo>[A-Za-z0-9\s]+)/$', views.ExistenciaRollo.as_view(),name="existencia_num_rollo"),
   url(r'^existencias/agrupadas/$', views.ExistenciaAgrupada.as_view(),name="existencia_agrupada"),
   url(r'^existencias/agrupadas/(?P<num_rollo>[A-Za-z0-9\s]+)/$', views.ExistenciaAgrupadaNumRollo.as_view(),name="existencia_agrupada_num_rollo"),

]		
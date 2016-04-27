from django.conf.urls import patterns, url
from django.conf.urls import patterns, url
from catalogos import views

urlpatterns =[
	 url(r'^catalogos/$', views.CatalogoLista.as_view(),name="catalogos_lista"),
	 ]
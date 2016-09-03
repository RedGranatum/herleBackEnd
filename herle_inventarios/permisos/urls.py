from django.conf.urls import patterns, url
from permisos import views

urlpatterns =[
 	url(r'^permiso_administrador/', views.PermisoAdministrador.as_view()),
]
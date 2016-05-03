from django.db import models

# Create your models here.
class Catalogo(models.Model):
	nombre = models.CharField(max_length=50, default='', unique=True,error_messages={'unique':"El catalogo ya existe"})

	def __str__(self):
		return self.nombre
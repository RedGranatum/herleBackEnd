from django.db import models
from decimal import *
from django.db.models import Max
from catalogos.models import Catalogo

class CatalogoDetalle(models.Model):
	cdu_catalogo = models.CharField(primary_key=True, max_length=7,default="0000000",unique=True,editable=False)
	catalogos = models.ForeignKey(Catalogo, related_name='catalogos_detalle')
	num_dcatalogo= models.IntegerField(default=0,help_text="clave consecutiva del detalle del catalogo")
	descripcion1  = models.CharField(max_length=100)
	descripcion2 = models.CharField(max_length=100, blank=True)
	monto1 = models.DecimalField(max_digits=18,decimal_places=2,default=Decimal('0.00'))
	monto2 = models.DecimalField(max_digits=18,decimal_places=2,default=Decimal('0.00'))
	cdu_default = models.CharField(max_length=7, blank=True)

	def save(self, *args, **kwargs):
		if(self.pk == '0000000'):
			lista = CatalogoDetalle.objects.filter(catalogos=self.catalogos).aggregate(ultimo=Max('num_dcatalogo'))
		
			self.num_dcatalogo = 0  if lista["ultimo"]==None else lista["ultimo"]+1

			#El cdu debe de ser 0010000
			self.cdu_catalogo= str(self.catalogos.id).zfill(3) + str(self.num_dcatalogo).zfill(4)

		
		super(CatalogoDetalle, self).save(*args, **kwargs)


	def __unicode__(self):
		return '%s: %s' % (self.cdu_catalogo, self.descripcion1)
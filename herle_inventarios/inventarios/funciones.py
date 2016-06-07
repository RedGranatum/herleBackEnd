from decimal import *
from catalogo_detalles.models import CatalogoDetalle

class CalculoCodigo(object):

	ancho 	= ""
	calibre = ""
	cdu_material = ""

	def codigoCalibre(self):
		valor_calibre =Decimal(self.calibre)
		ccalibre = CatalogoDetalle.objects.filter(catalogos=6,monto1__lte=valor_calibre,monto2__gte=valor_calibre)
		if len(ccalibre)==0:
			return ''
		return ccalibre.first().descripcion1

	def codigoAncho(self):
		valor_ancho =Decimal(self.ancho)
		cancho = CatalogoDetalle.objects.filter(catalogos=7,monto1__lte=valor_ancho,monto2__gte=valor_ancho)
		if len(cancho)==0:
			return ''
		return cancho.first().descripcion1

	def codigoMaterial(self):
		cmaterial = CatalogoDetalle.objects.filter(catalogos=5,cdu_catalogo=self.cdu_material)
		if len(cmaterial)==0:
			return ''
		return cmaterial.first().descripcion2
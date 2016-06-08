from decimal import *
from catalogo_detalles.models import CatalogoDetalle

class CalculoCodigo(object):

	ancho 	= ""
	calibre = ""
	cdu_material = ""
	largo = ""

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

	def codigoLargo(self):
		valor_largo =Decimal(self.largo)
		clargo = CatalogoDetalle.objects.filter(catalogos=8,monto1__lte=valor_largo,monto2__gte=valor_largo)
		if len(clargo)==0:
			return ''
		return clargo.first().descripcion1

	def generarCodigoProducto(self):
		salida1 = self.codigoCalibre()
		salida2 = self.codigoMaterial()
		salida3 = self.codigoAncho()
		salida4 = self.codigoLargo()
		if(salida4 != ''):
			return salida4

		if(salida1=='' or salida2=='' or salida3==''):
			return ''
		codigo = salida1 + salida2 + salida3
		return codigo

class CalculoPrecios(object):
	cdu_pais = ""
	con_comercializadora = False
	precio_libra_centavos = 0.0
	factor = 0.0 
	precio_dolar = 0.0
	factor_impuesto = 0.0

	def kiloEnDolar(self):
		valor = Decimal(self.precio_libra_centavos) * Decimal(self.factor)
		valor = round(valor,4)
		return str(valor)

	def kiloEnPeso(self):
		kilo_dolar = self.kiloEnDolar()
		valor = Decimal(kilo_dolar) * Decimal(self.precio_dolar)
		valor = round(valor,4)
		return str(valor)
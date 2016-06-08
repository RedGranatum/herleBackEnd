from decimal import *
from catalogo_detalles.models import CatalogoDetalle
import inspect, itertools 

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
	def __init__(self):
		self.__precio_libra_centavos ='0.0'
		self.__factor ='0.0'
		self.__precio_dolar = '0.0'
		self.__factor_impuesto = '0.0'
		self.__precio_tonelada_dolar ='0.0'
		self.__factor_impuesto_china = '0.0'

	cdu_pais = ""
	con_comercializadora = False

	@property
	def precio_libra_centavos(self):		
		return self.__precio_libra_centavos

	@precio_libra_centavos.setter
	def  precio_libra_centavos(self, precio_libra_centavos):	
		self.__precio_libra_centavos = self.asignarValorSiNoEsDecimal(precio_libra_centavos)


	@property
	def factor(self):
		return self.__factor

	@factor.setter
	def  factor(self, factor):	
		self.__factor = self.asignarValorSiNoEsDecimal(factor)


	@property
	def precio_dolar(self):
		return self.__precio_dolar

	@precio_dolar.setter
	def  precio_dolar(self, precio_dolar):	
		self.__precio_dolar = self.asignarValorSiNoEsDecimal(precio_dolar)


	@property
	def factor_impuesto(self):
		return self.__factor_impuesto

	@factor_impuesto.setter
	def  factor_impuesto(self, factor_impuesto):	
		self.__factor_impuesto = self.asignarValorSiNoEsDecimal(factor_impuesto)


	@property	
	def porc_comercializadora(self):
		return self.__porc_comercializadora

	@porc_comercializadora.setter
	def  porc_comercializadora(self, porc_comercializadora):	
		self.__porc_comercializadora = self.asignarValorSiNoEsEntero(porc_comercializadora)

	@property
	def precio_tonelada_dolar(self):
		return self.__precio_tonelada_dolar

	@precio_tonelada_dolar.setter
	def  precio_tonelada_dolar(self,precio_tonelada_dolar):	
		self.__precio_tonelada_dolar = self.asignarValorSiNoEsDecimal(precio_tonelada_dolar)

	@property
	def factor_impuesto_china(self):
		return self.__factor_impuesto_china

	@factor_impuesto_china.setter
	def  factor_impuesto_china(self, factor_impuesto_china):	
		self.__factor_impuesto_china = self.asignarValorSiNoEsDecimal(factor_impuesto_china)



	def asignarValorSiNoEsDecimal(self,valor):
		if(self.esDecimal(valor)==False):
			return'0.0'
		return valor;

	def asignarValorSiNoEsEntero(self,valor):
		if(valor.isdigit()==False):
			return'0'
		return valor;
	
	def esDecimal(self,valor):
		try:
			Decimal(valor)
			return True
		except:
			return False

	def kiloEnDolar(self):
		if(self.cdu_pais!="0010001"):
			return '0.0'
		valor = Decimal(self.precio_libra_centavos) *  Decimal(self.factor)
		return str(round(valor,4))

	def kiloEnPeso(self):
		if(self.cdu_pais!="0010001"):
			return '0.0'
		kilo_dolar = self.kiloEnDolar()
		valor = Decimal(kilo_dolar) * Decimal(self.precio_dolar)
		return str(round(valor,4))
	
	def ToneladaEnDolar(self):
		if(self.cdu_pais!="0010002"):
			return '0.0'
		valor = Decimal(self.precio_tonelada_dolar) * Decimal(self.precio_dolar)
		return str(round(valor,4))

	def kiloEnPesosFinal(self):
		if(self.cdu_pais=="0010002"):
			return self.kiloEnPesosChina()
		return 	self.kiloEnPesosEU()
		
	def kiloEnPesosChina(self):
		valor = Decimal(self.ToneladaEnDolar()) + (Decimal(self.ToneladaEnDolar()) / 100) * Decimal(self.factor_impuesto_china)
		return str(round(valor,4))

	def kiloEnPesosEU(self):
		valor = Decimal(self.kiloEnDolar()) * Decimal(self.kiloEnPeso())
		if(self.con_comercializadora==True):
			valor = valor * (Decimal(self.porc_comercializadora)/100)
		
		valor = valor + Decimal(self.factor_impuesto)
		return str(round(valor,4))
from decimal import *
import math
from catalogo_detalles.models import CatalogoDetalle
import inspect, itertools 

def truncar_decimales(valor, decimales):
	decimales_tmp = decimales
	if(decimales==5):
		decimales_tmp = decimales_tmp + 1
	valor1 = int(float(valor)*(10.0**decimales_tmp))
	#valor1 = round(round(float(valor)*(10.0**decimales_tmp),10),0)
	valor2 = (10.0**decimales_tmp)
	return round(valor1 / valor2,decimales)

class Conversor(object):
	def __init__(self):
		self.kilogramo =0.0
		self.libra = 0.0
		self.pais = "0010000"

	kilo_en_libra = 2.20462
	mexico = "0010000"
	eu     = "0010001"
	china  = "0010002"


	def transformarKg_Lb(self, kg):
		calculo = float(kg) * self.kilo_en_libra
		return truncar_decimales(calculo,5)

	def transformarLb_Kg(self, lb):
		calculo = ((float(lb) / self.kilo_en_libra))
		return truncar_decimales(calculo,5)

	def transformarPorPais(self):
		if(self.pais == self.mexico):
			self.libra = self.transformarKg_Lb(self.kilogramo)
		else:
			self.kilogramo = self.transformarLb_Kg(self.libra)

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
		self.__porc_comercializadora = '0'
		self.__con_comercializadora = False

	cdu_pais = ""

	@property
	def con_comercializadora(self):		
		return self.__con_comercializadora

	@con_comercializadora.setter
	def  con_comercializadora(self, con_comercializadora):	
		if(type(con_comercializadora) is str):
			con_comercializadora = con_comercializadora == 'True'
	
		self.__con_comercializadora = con_comercializadora 


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
		self.__porc_comercializadora = self.asignarValorSiNoEsDecimal(porc_comercializadora)

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
		valor = str(valor)
		if(self.esDecimal(valor)==True):
			return int(float(valor))
		if(valor.isdigit()==False):
			return'0'
		return valor;
	
	def esDecimal(self,valor):
		try:
			Decimal(valor)
			return True
		except:
			return False

	def kiloEnDolar(self,decimales=4):
		if(self.cdu_pais!="0010001"):
			return '0.0'
		valor = Decimal(self.precio_libra_centavos) *  Decimal(self.factor)
		#return str(round(valor,6))
		return str(truncar_decimales(valor,decimales))

	def kiloEnPeso(self,decimales=4):
		# Kilo en peso=4
		if(self.cdu_pais!="0010001"):
			return '0.0'
		#import ipdb;ipdb.set_trace()
		kilo_dolar = self.kiloEnDolar(8)
		#kilo_dolar = Decimal(self.precio_libra_centavos) *  Decimal(self.factor)
		valor = Decimal(kilo_dolar) * Decimal(self.precio_dolar)
		#valor = truncar_decimales(valor,4)

		if(self.con_comercializadora==True):
			porcentaje = (1 + Decimal(self.porc_comercializadora)/100)
			valor = float(valor) * float(porcentaje)

		return str(truncar_decimales(valor,decimales))
	
	def ToneladaEnDolar(self,decimales=4):
		if(self.cdu_pais!="0010002"):
			return '0.0'
		valor = Decimal(self.precio_tonelada_dolar) * Decimal(self.precio_dolar)
		return str(truncar_decimales(valor,decimales))
		#return str(round(valor,4))

	def kiloEnPesosFinal(self):
		if(self.cdu_pais=="0010001"):
			return 	self.kiloEnPesosEU()
		if(self.cdu_pais=="0010002"):
			return self.kiloEnPesosChina()
		return '0.0'

	def kiloEnPesosChina(self):
		valor =  (Decimal(self.ToneladaEnDolar(8)) / 1000) + Decimal(self.factor_impuesto_china)
		return str(truncar_decimales(valor,4))
		#return str(round(valor,4))

	def kiloEnPesosEU(self):
		valor = Decimal(self.kiloEnPeso(8))
		
		valor = valor + Decimal(self.factor_impuesto)
		return str(truncar_decimales(valor,4))
		#return str(round(valor,4))
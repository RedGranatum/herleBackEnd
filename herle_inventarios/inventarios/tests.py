from django.test import TestCase
from rest_framework.test import APIClient
from django.db import connection
from catalogos.models import Catalogo
from catalogo_detalles.models import CatalogoDetalle
from inventarios.funciones import CalculoCodigo

class ComprasModelTest(TestCase):
	def setUp(self):
		self.client = APIClient()
		cursor = connection.cursor()
		cursor.execute("ALTER SEQUENCE catalogos_catalogo_id_seq RESTART WITH 1;")
		cursor.execute("ALTER SEQUENCE compras_detalles_compradetalle_id_seq RESTART WITH 1;")
		
		self.cargar_catalogos()
		self.cargar_catalogos_detalles()

	def test_calcular_codigo_rango(self):
		self.probarCalibres('0.007','') 
		self.probarCalibres('0.008','C32') 
		self.probarCalibres('0.009','C32')
		self.probarCalibres('0.01','C32')
		self.probarCalibres('0.012','C30')
		self.probarCalibres('0.014','')
	
	def test_calcular_codigo_ancho(self):
		self.probarAnchos('34','')
		self.probarAnchos('35','3')
		self.probarAnchos('36.5','3')
		self.probarAnchos('39','3.5')
		self.probarAnchos('46.6','')

	def test_calcular_codigo_material(self):
		self.probarMateriales('0050001','P')
		self.probarMateriales('0050004','R')
		self.probarMateriales('0050000','')
		self.probarMateriales('0040001','')

	def probarCalibres(self, calibre, codigo_esperado):
		calculoCodigos = CalculoCodigo()
		calculoCodigos.calibre = calibre
		ccalibre = calculoCodigos.codigoCalibre()
		self.assertEqual(ccalibre,codigo_esperado)

	def probarAnchos(self, ancho, codigo_esperado):
		calculoCodigos = CalculoCodigo()
		calculoCodigos.ancho = ancho
		cancho = calculoCodigos.codigoAncho()
		self.assertEqual(cancho,codigo_esperado)

	def probarMateriales(self, cdu_material, codigo_esperado):
		calculoCodigos = CalculoCodigo()
		calculoCodigos.cdu_material = cdu_material
		cmaterial = calculoCodigos.codigoMaterial()
		self.assertEqual(cmaterial,codigo_esperado)

	def cargar_catalogos(self):
		self.catalogoPaises = self.crearCatalogo("Paises")
		self.catalogoEstados = self.crearCatalogo("Estados")
		self.catalogoBancos = self.crearCatalogo("Bancos")
		self.catalogoMonedas = self.crearCatalogo("Monedas")
		self.catalogoMaterial = self.crearCatalogo("Material")
		self.catalogoCalibre = self.crearCatalogo("Codigos Calibre")
		self.catalogoAncho = self.crearCatalogo("Codigos Ancho")
		self.catalogoLargo= self.crearCatalogo("Codigos Largo")
		self.catalogoParametros = self.crearCatalogo("Parametros Calculos")

	def cargar_catalogos_detalles(self):
		self.crearCatalogoCalibres("C32","0.008","0.01")
		self.crearCatalogoCalibres("C30","0.011","0.013")

		self.crearCatalogoAnchos("3","35","38.5")
		self.crearCatalogoAnchos("3.5","39","46.5")

		self.crearCatalogoMateriales("NO ESPECIFICADO","")
		self.crearCatalogoMateriales("PINTADO","P")
		self.crearCatalogoMateriales("GALVANIZADO","G")
		self.crearCatalogoMateriales("ZINTROALUM","Z")
		self.crearCatalogoMateriales("RAINBOW","R")
		
	


	def crearCatalogo(self,nombre_catalogo):
		catalogo = Catalogo()
		catalogo.nombre =nombre_catalogo
		catalogo.save()
		return catalogo

	def crearCatalogoCalibres(self,desc1,monto1,monto2):
		self.crearCatalogoDetalle(self.catalogoCalibre,desc1,'',monto1,monto2)

	def crearCatalogoAnchos(self,desc1,monto1,monto2):
		self.crearCatalogoDetalle(self.catalogoAncho,desc1,'',monto1,monto2)

	def crearCatalogoMateriales(self,desc1,desc2):
		self.crearCatalogoDetalle(self.catalogoMaterial,desc1,desc2,0.0,0.0)

	def crearCatalogoDetalle(self,tipo,desc1,desc2,monto1,monto2):
		detCat = CatalogoDetalle()
		detCat.catalogos = tipo
		detCat.descripcion1 =desc1
		detCat.descripcion2 =desc2	
		detCat.monto1 =monto1
		detCat.monto2 =monto2
		detCat.save()
		
		
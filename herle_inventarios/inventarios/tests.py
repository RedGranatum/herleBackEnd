from django.test import TestCase
from rest_framework.test import APIClient
from django.db import connection
from catalogos.models import Catalogo
from catalogo_detalles.models import CatalogoDetalle
from inventarios.funciones import CalculoCodigo,CalculoPrecios

class InventariosCodigoTest(TestCase):
	def setUp(self):
		self.client = APIClient()
		cursor = connection.cursor()
		cursor.execute("ALTER SEQUENCE catalogos_catalogo_id_seq RESTART WITH 1;")
		cursor.execute("ALTER SEQUENCE compras_detalles_compradetalle_id_seq RESTART WITH 1;")
		
		self.cargar_catalogos()
		self.cargar_catalogos_detalles()
		self.calculoCodigos = CalculoCodigo()


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

	def test_calcular_codigo_largo(self):
		self.probarLargo('10','PAQUETERIA10')
		self.probarLargo('12','PAQUETERIA12')

	def test_calcularCodigoRangoMaterialAncho(self):
		self.probarCodigoCalculo('0.008','0050001','35','0','C32P3')
		self.probarCodigoCalculo('0.012','0050004','39','1','C30R3.5')		

	def test_calcularCodigoRangoMaterialAncho_ConUnValorMal(self):
		self.probarCodigoCalculo('0.007','0050001','35','0','')
		self.probarCodigoCalculo('0.008','0040001','35','0','')
		self.probarCodigoCalculo('0.008','0050001','30','0','')

	def test_calcularCodigoRangoMaterialAnchoLargo(self):
		self.probarCodigoCalculo('0.008','0050001','35','10','PAQUETERIA10')
		self.probarCodigoCalculo('0.008','0040001','35','12','PAQUETERIA12')

	def test_obtener_codigo_producto_por_url(self):
		response = self.client.get('/inventarios/codigo_producto/?rango=0.008&cdu_material=0050001&ancho=35&largo=0', format='json')
		self.assertEqual(response.data,'C32P3')

		response = self.client.get('/inventarios/codigo_producto/?rango=0.012&cdu_material=0050004&ancho=39&largo=0', format='json')
		self.assertEqual(response.data,'C30R3.5')
		
		response = self.client.get('/inventarios/codigo_producto/?rango=0.008&cdu_material=0040001&ancho=35&largo=0', format='json')
		self.assertEqual(response.data,'')

		response = self.client.get('/inventarios/codigo_producto/?rango=0.008&cdu_material=0040001&ancho=35&largo=12', format='json')
		self.assertEqual(response.data,'PAQUETERIA12')

	def test_calculo_estados_unidos_sin_comercializadora(self):
		dicValores = {'cdu_pais':'0010001','precio_tonelada_dolar':'0','factor_impuesto_china':'0','con_comercializadora':False,'precio_libra_centavos':'0.27',
					'factor':'2.2045', 'precio_dolar':'18.03', 'factor_impuesto':'2.13', 'porc_comercializadora':'4',
					'esperado_kilo_en_dolar':'0.5952','esperado_kilo_en_pesos':'10.7315','esperado_tonelada_en_dolar':'0.0','esperado_kilo_en_pesos_final':'12.8615'}
		self.probarCalculos(dicValores)

		dicValores = {'cdu_pais':'0010001','precio_tonelada_dolar':'58','factor_impuesto_china':'2','con_comercializadora':False,'precio_libra_centavos':'0.26',
					'factor':'2.2045', 'precio_dolar':'17.03', 'factor_impuesto':'1.80', 'porc_comercializadora':'4',
					'esperado_kilo_en_dolar':'0.5732','esperado_kilo_en_pesos':'9.7616','esperado_tonelada_en_dolar':'0.0','esperado_kilo_en_pesos_final':'11.5616'}
		self.probarCalculos(dicValores)


	def test_calculo_estados_unidos_con_comercializadora(self):
		dicValores = {'cdu_pais':'0010001','precio_tonelada_dolar':'58','factor_impuesto_china':'2','con_comercializadora':True,'precio_libra_centavos':'0.27',
					'factor':'2.2045', 'precio_dolar':'18.03', 'factor_impuesto':'2.13', 'porc_comercializadora':'4',
					'esperado_kilo_en_dolar':'0.5952','esperado_kilo_en_pesos':'10.7315','esperado_tonelada_en_dolar':'0.0','esperado_kilo_en_pesos_final': '2.5593'}
		self.probarCalculos(dicValores)

		dicValores = {'cdu_pais':'0010001','precio_tonelada_dolar':'0','factor_impuesto_china':'0','con_comercializadora':True,'precio_libra_centavos':'0.26',
					'factor':'2.2045', 'precio_dolar':'17.03', 'factor_impuesto':'1.80', 'porc_comercializadora':'3',
					'esperado_kilo_en_dolar':'0.5732','esperado_kilo_en_pesos':'9.7616','esperado_tonelada_en_dolar':'0.0','esperado_kilo_en_pesos_final': '2.0928'}
		self.probarCalculos(dicValores)

	def test_calculo_china(self):
		dicValores = {'cdu_pais':'0010002','precio_tonelada_dolar':'580','factor_impuesto_china':'3.45','con_comercializadora':True,'precio_libra_centavos':'0.26',
					 'factor':'2.2045','precio_dolar':'18.03','factor_impuesto':'2.13', 'porc_comercializadora':'4',
					 'esperado_kilo_en_dolar':'0.0','esperado_kilo_en_pesos':'0.0','esperado_tonelada_en_dolar':'10457.4000','esperado_kilo_en_pesos_final': '13.9074'}
		self.probarCalculos(dicValores)

		dicValores = {'cdu_pais':'0010002','precio_tonelada_dolar':'58','factor_impuesto_china':'2','con_comercializadora':False,'precio_libra_centavos':'0.0',
					 'factor':'0.0','precio_dolar':'17.03','factor_impuesto':'0', 'porc_comercializadora':'0.0',
					 'esperado_kilo_en_dolar':'0.0','esperado_kilo_en_pesos':'0.0','esperado_tonelada_en_dolar':'987.7400','esperado_kilo_en_pesos_final': '2.9877'}
		self.probarCalculos(dicValores)

	def test_si_se_pasan_caracteres_a_valores_decimale_devolver_cero(self):
		calculo = CalculoPrecios()
		calculo.precio_libra_centavos ='A'
		calculo.factor = 'B'
		calculo.precio_dolar =''
		calculo.factor_impuesto ='C02.1'
		calculo.porc_comercializadora = '2.2.3'
		calculo.precio_tonelada_dolar = '2.2.3'
		calculo.factor_impuesto_china = '2.2.3'

		self.assertEqual(calculo.precio_libra_centavos, '0.0')
		self.assertEqual(calculo.factor, '0.0')
		self.assertEqual(calculo.precio_dolar, '0.0')
		self.assertEqual(calculo.factor_impuesto, '0.0')
		self.assertEqual(calculo.porc_comercializadora, '0')
		self.assertEqual(calculo.precio_tonelada_dolar, '0.0')
		self.assertEqual(calculo.factor_impuesto_china, '0.0')


	def test_calculos_por_url(self):
		ruta =("/inventarios/calculo_precios/?cdu_pais=0010001&precio_tonelada_dolar=0"
				"&factor_impuesto_china=0&con_comercializadora=False&precio_libra_centavos=0.27"
				"&factor=2.2045&precio_dolar=18.03&factor_impuesto=2.13&porc_comercializadora=4")
		
		response = self.client.get(ruta, format='json')
		self.assertEqual( response.data['kilo_en_dolar'],'0.5952')
		self.assertEqual( response.data['kilo_en_pesos'],'10.7315')
		self.assertEqual( response.data['tonelada_en_dolar'],'0.0')
		self.assertEqual( response.data['kilo_en_pesos_final'],'12.8615')

		ruta = ("/inventarios/calculo_precios/?cdu_pais=0010002&precio_tonelada_dolar=58"
				"&factor_impuesto_china=2&con_comercializadora=False&precio_libra_centavos=0.0"
				"&factor=0.0&precio_dolar=17.03&factor_impuesto=0&porc_comercializadora=0.0")
		response = self.client.get(ruta, format='json')
		self.assertEqual( response.data['kilo_en_dolar'],'0.0')
		self.assertEqual( response.data['kilo_en_pesos'],'0.0')
		self.assertEqual( response.data['tonelada_en_dolar'],'987.7400')
		self.assertEqual( response.data['kilo_en_pesos_final'],'2.9877')	

		ruta =("/inventarios/calculo_precios/?cdu_pais=0010000&precio_tonelada_dolar=0"
				"&factor_impuesto_china=0&con_comercializadora=False&precio_libra_centavos=0.27"
				"&factor=2.2045&precio_dolar=18.03&factor_impuesto=2.13&porc_comercializadora=4")
		
		response = self.client.get(ruta, format='json')
		self.assertEqual( response.data['kilo_en_dolar'],'0.0')
		self.assertEqual( response.data['kilo_en_pesos'],'0.0')
		self.assertEqual( response.data['tonelada_en_dolar'],'0.0')
		self.assertEqual( response.data['kilo_en_pesos_final'],'0.0')
	

	def probarCalculos(self,dict_valores):
		calculo = CalculoPrecios()
		calculo.cdu_pais = dict_valores['cdu_pais']
		calculo.con_comercializadora  = dict_valores['con_comercializadora']
		calculo.precio_libra_centavos = dict_valores['precio_libra_centavos']
		calculo.factor = dict_valores['factor']
		calculo.precio_dolar = dict_valores['precio_dolar']
		calculo.factor_impuesto = dict_valores['factor_impuesto']
		calculo.porc_comercializadora = dict_valores['porc_comercializadora']

		calculo.precio_tonelada_dolar  = dict_valores['precio_tonelada_dolar']
		calculo.factor_impuesto_china = dict_valores['factor_impuesto_china']
		kilo_en_dolar = calculo.kiloEnDolar()
		kilo_en_pesos = calculo.kiloEnPeso()
		tonelada_en_dolar = calculo.ToneladaEnDolar()
		kilo_en_pesos_final = calculo.kiloEnPesosFinal()

		self.assertEqual(kilo_en_dolar,dict_valores['esperado_kilo_en_dolar'])
		self.assertEqual(kilo_en_pesos,dict_valores['esperado_kilo_en_pesos'])	
		self.assertEqual(tonelada_en_dolar,dict_valores['esperado_tonelada_en_dolar']) 	
		self.assertEqual(kilo_en_pesos_final,dict_valores['esperado_kilo_en_pesos_final'])	

	def probarCalibres(self, calibre, codigo_esperado):
		self.calculoCodigos.calibre = calibre
		ccalibre = self.calculoCodigos.codigoCalibre()
		self.assertEqual(ccalibre,codigo_esperado)

	def probarAnchos(self, ancho, codigo_esperado):
		self.calculoCodigos.ancho = ancho
		cancho = self.calculoCodigos.codigoAncho()
		self.assertEqual(cancho,codigo_esperado)

	def probarMateriales(self, cdu_material, codigo_esperado):
		self.calculoCodigos.cdu_material = cdu_material
		cmaterial = self.calculoCodigos.codigoMaterial()
		self.assertEqual(cmaterial,codigo_esperado)

	def probarLargo(self, largo, codigo_esperado):
		self.calculoCodigos.largo = largo
		clargo = self.calculoCodigos.codigoLargo()
		self.assertEqual(clargo,codigo_esperado)

	def probarCodigoCalculo(self,calibre,cdu_material,ancho,largo,codigo_esperado):
		self.calculoCodigos.calibre = calibre
		self.calculoCodigos.cdu_material = cdu_material
		self.calculoCodigos.ancho = ancho
		self.calculoCodigos.largo = largo
		codigo = self.calculoCodigos.generarCodigoProducto()
		self.assertEqual(codigo,codigo_esperado)

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
		self.crearCatalogoPaises("Mexico")
		self.crearCatalogoPaises("China")
		self.crearCatalogoPaises("EEUU")


		self.crearCatalogoCalibres("C32","0.008","0.01")
		self.crearCatalogoCalibres("C30","0.011","0.013")

		self.crearCatalogoAnchos("3","35","38.5")
		self.crearCatalogoAnchos("3.5","39","46.5")

		self.crearCatalogoMateriales("NO ESPECIFICADO","")
		self.crearCatalogoMateriales("PINTADO","P")
		self.crearCatalogoMateriales("GALVANIZADO","G")
		self.crearCatalogoMateriales("ZINTROALUM","Z")
		self.crearCatalogoMateriales("RAINBOW","R")

		self.crearCatalogoLargos("PAQUETERIA10","10","10")
		self.crearCatalogoLargos("PAQUETERIA12","12","12")



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

	def crearCatalogoLargos(self,desc1,monto1,monto2):
		self.crearCatalogoDetalle(self.catalogoLargo,desc1,'',monto1,monto2)

	def crearCatalogoPaises(self,desc1):
		self.crearCatalogoDetalle(self.catalogoPaises,desc1,'',0.0,0.0)


	def crearCatalogoDetalle(self,tipo,desc1,desc2,monto1,monto2):
		detCat = CatalogoDetalle()
		detCat.catalogos = tipo
		detCat.descripcion1 =desc1
		detCat.descripcion2 =desc2	
		detCat.monto1 =monto1
		detCat.monto2 =monto2
		detCat.save()
		
		
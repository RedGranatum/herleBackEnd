from django.test 		      import TestCase
from rest_framework 		  import filters,generics,status
from rest_framework.test 	  import APIClient
from django.db 				  import connection
from catalogos.models 		  import Catalogo
from catalogo_detalles.models import CatalogoDetalle
from proveedores.models		  import Proveedor
from compras.models 		  import Compra
from compras_detalles.models  import CompraDetalle
from inventarios.funciones    import CalculoCodigo,CalculoPrecios,Conversor
from inventarios.models       import Inventario
from inventarios.serializers  import InventarioSerializer

class InventariosCodigoTest(TestCase):
	def setUp(self):
		self.client = APIClient()
		cursor = connection.cursor()
		cursor.execute("ALTER SEQUENCE catalogos_catalogo_id_seq RESTART WITH 1;")
		cursor.execute("ALTER SEQUENCE proveedores_proveedor_id_seq RESTART WITH 1;")
		cursor.execute("ALTER SEQUENCE compras_compra_id_seq RESTART WITH 1;")
		cursor.execute("ALTER SEQUENCE compras_detalles_compradetalle_id_seq RESTART WITH 1;")
		
		self.cargar_catalogos()
		self.cargar_catalogos_detalles()
		self.calculoCodigos = CalculoCodigo()
		self.cargar_proveedores()
		self.cargarCompraConDetalle()

	def test_transforma_kilo_a_libra(self):
		conversor = Conversor();
		lb = conversor.transformarKg_Lb(1)
		self.assertEqual(lb, 2.20462)

		lb = conversor.transformarKg_Lb(1.5)
		self.assertEqual(lb, 3.30693)

	def test_transforma_libra_a_kilo(self):
		conversor = Conversor();
		kg = conversor.transformarLb_Kg(2.20462)
		self.assertEqual(kg, 1)

		kg = conversor.transformarLb_Kg(3.30693)
		self.assertEqual(kg,1.5 )

	def test_mexico_kg(self):
		conversor = Conversor();
		conversor.pais = "0010000"
		conversor.kilogramo = 1
		conversor.libra = 1
		conversor.transformarPorPais()
		self.assertEqual(conversor.kilogramo , 1)
		self.assertEqual(conversor.libra , 2.20462)

	def test_eu_kg(self):
		conversor = Conversor();
		conversor.pais = "0010001"
		conversor.kilogramo = 1
		conversor.libra = 1
		conversor.transformarPorPais()
		self.assertEqual(conversor.libra , 1)
		self.assertEqual(conversor.kilogramo , 0.45359)

	def test_china_kg(self):
		conversor = Conversor();
		conversor.pais = "0010002"
		conversor.kilogramo = 1.23
		conversor.libra = 12
		conversor.transformarPorPais()
		self.assertEqual(conversor.libra , 12)
		self.assertEqual(conversor.kilogramo , 5.44311)
	
	def test_obtener_conversion_kg_lb_mexico(self):
		response = self.client.get('/inventarios/conversor/?pais=0010000&libra=1&kilogramo=1', format='json')
		self.assertEqual(response.data['kilogramo'],'1')
		self.assertEqual(response.data['libra'],'2.20462')

	def test_obtener_conversion_kg_lb_mexico(self):
		response = self.client.get('/inventarios/conversor/?pais=0010001&libra=1&kilogramo=1', format='json')
		self.assertEqual(response.data['libra'],'1')
		self.assertEqual(response.data['kilogramo'],'0.45359')
	
	def test_obtener_conversion_kg_lb_china(self):
		response = self.client.get('/inventarios/conversor/?pais=0010001&libra=2&kilogramo=2', format='json')
		self.assertEqual(response.data['libra'],'2')
		self.assertEqual(response.data['kilogramo'],'0.90719')
	
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
					'factor':'2.2045', 'precio_dolar':'17.03', 'factor_impuesto':'1.80', 'porc_comercializadora':'3.0',
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
		self.assertEqual(calculo.porc_comercializadora, '0.0')
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
	
	def test_crear_registro_inventario(self):		
		compCab  = Compra.objects.all().get(pk=1)
		compDet1 = CompraDetalle.objects.all().get(pk=1)
		cpais    = CatalogoDetalle.objects.all().get(cdu_catalogo='0010001') 
		self.assertEqual(compDet1.id,1)

		inventario1 = Inventario()
		inventario1.compra_detalle 			= compDet1
		inventario1.invoice_compra 		    = 'ASSS'
		inventario1.material 			    = compDet1.material
		inventario1.calibre  				= '0.008'
		inventario1.ancho 				    = '35'
		inventario1.largo    				= '1'
		inventario1.num_rollo			    = 'A123'
		inventario1.peso_kg   				= 132.0
		inventario1.peso_lb  			    = 0.0
		inventario1.transporte 				= 'ESTAFETA'
		inventario1.pais	                = cpais
		inventario1.precio_libra 			= '0.27'
		inventario1.factor       			= '2.2045'
		inventario1.precio_dolar			= '18.03'
		inventario1.precio_tonelada_dolar	= '58'
		inventario1.factor_impuesto 		= '2.13'
		inventario1.con_comercializadora 	= True
		inventario1.porc_comercializadora   = '4'

		inventario1.descripcion = 'Sin descripcion'
		inventario1.comentarios = 'Todo esta listo'
		inventario1.save()

		self.assertEqual(inventario1.codigo_producto,'C32R3')

		self.assertEqual(inventario1.valor_kilo_dolar,'0.5952')
		self.assertEqual(inventario1.valor_kilo_pesos,'10.7315')
		self.assertEqual(inventario1.valor_tonelada_dolar,'0.0')		
		self.assertEqual(inventario1.valor_final_kilo_pesos,'2.5593')
	
	def test_serializer_inventarios(self):
		response = self.client.get('/inventarios/', format='json')
		self.assertEqual(len(response.data),0)

		data = {"compra_detalle":"1","invoice_compra":"ASSS","material":"0050004","calibre":"0.008",
				"ancho":"35","largo":"1","num_rollo":"A123","peso_kg":"132.0","peso_lb":"1.32","transporte":"ESTAFETA",
				"pais":"0010000","precio_libra":"0.27","factor":"2.2045","precio_dolar":"18.03",
				"precio_tonelada_dolar":"58","factor_impuesto":"2.13","con_comercializadora":"True",
				"porc_comercializadora":"4","descripcion":"Sin descripcion"	,"comentarios":"Todo esta listo"}
	
		serializer =InventarioSerializer(data=data)
		self.assertTrue(serializer.is_valid())
		serializer.save()
		existen = Inventario.objects.all()
		self.assertEqual(existen.count(),1)
		
		response = self.client.get('/inventarios/', format='json')
		self.assertEqual(len(response.data),1)

		self.assertEqual (response.data[0]['peso_kg'],'132.00000')
		self.assertEqual (response.data[0]['peso_lb'],'291.00984')

		# codigo_producto = response.data[0]['codigo_producto']
		# valor_kilo_dolar = response.data[0]['valor_kilo_dolar']
		# valor_kilo_pesos = response.data[0]['valor_kilo_pesos']
		# valor_tonelada_dolar = response.data[0]['valor_tonelada_dolar']
		# valor_final_kilo_pesos = response.data[0]['valor_final_kilo_pesos']

		# self.assertEqual (codigo_producto,'C32R3')
		# self.assertEqual(valor_kilo_dolar,'0.5952')
		# self.assertEqual(valor_kilo_pesos,'10.7315')
		# self.assertEqual(valor_tonelada_dolar,'0.0000')		
		# self.assertEqual(valor_final_kilo_pesos,'2.5593')	

	def test_enviar_datos_inventario_desde_desde_la_ruta(self):
		response = self.client.get('/compras_detalles/1/', format='json')
		self.assertEqual(response.data['validado'],False)

		response = self.client.get('/inventarios/', format='json')
		self.assertEqual(len(response.data),0)

		data = {"compra_detalle":"1","invoice_compra":"ASSS","material":"0050004","calibre":"0.008",
				"ancho":"35","largo":"1","num_rollo":"A123","peso_kg":"1132.0","peso_lb":"32.33","transporte":"ESTAFETA",
				"pais":"0010001","precio_libra":"0.27","factor":"2.2045","precio_dolar":"18.03",
				"precio_tonelada_dolar":"58","factor_impuesto":"2.13","con_comercializadora":"True",
				"porc_comercializadora":"4","descripcion":"Sin descripcion"	,"comentarios":"Todo esta listo"}
		
		response = self.client.post('/inventarios/',data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

		self.assertEqual(response.data["peso_lb"],"32.33000")
		self.assertEqual(response.data["peso_kg"],"14.66466")


		self.assertEqual(response.data["codigo_producto"],"C32R3")

		self.assertEqual(response.data["valor_kilo_dolar"],"0.5952")
		self.assertEqual(response.data["valor_kilo_pesos"],"10.7315")
		self.assertEqual(response.data["valor_tonelada_dolar"],"0.0000")
		self.assertEqual(response.data["valor_final_kilo_pesos"],"2.5593")

		response = self.client.get('/compras_detalles/1/', format='json')
		self.assertEqual(response.data['validado'],True)

		# Volver validar la misma compra
		data = {"compra_detalle":"1","invoice_compra":"ASSS","material":"0050004","calibre":"0.008",
				"ancho":"35","largo":"1","num_rollo":"A1223","peso_kg":"132.0","peso_lb":"0.0","transporte":"ESTAFETA",
				"pais":"0010001","precio_libra":"0.27","factor":"2.2045","precio_dolar":"18.03",
				"precio_tonelada_dolar":"58","factor_impuesto":"2.13","con_comercializadora":"True",
				"porc_comercializadora":"4","descripcion":"Sin descripcion"	,"comentarios":"Todo esta listo"}
		
		response = self.client.post('/inventarios/',data, format='json')
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
		self.assertEqual(response.data,  {'error': "['Este detalle de compra ya habia sido validado']"} )

		data = {"compra_detalle":"1","invoice_compra":"ASSS","material":"0050004","calibre":"0.008",
		"ancho":"35","largo":"1","num_rollo":"A123","peso_kg":"132.0","peso_lb":"0.0","transporte":"ESTAFETA",
		"pais":"","precio_libra":"0.27","factor":"2.2045","precio_dolar":"18.03",
		"precio_tonelada_dolar":"58","factor_impuesto":"2.13","con_comercializadora":"True",
		"porc_comercializadora":"4","descripcion":"Sin descripcion"	,"comentarios":"Todo esta listo"}
		
		response = self.client.post('/inventarios/',data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)		
		error = {'num_rollo': ['El numero de rollo ya existe'], 'pais': ['Este campo no puede ser nulo.']}
		self.assertEqual(response.data, error)

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

		self.crearCatalogoMoneda("Pesos")
		self.crearCatalogoMoneda("Dolar")		

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

	def crearCatalogoMoneda(self,desc1):
		self.crearCatalogoDetalle(self.catalogoMonedas,desc1,'',0.0,0.0)

	def crearCatalogoDetalle(self,tipo,desc1,desc2,monto1,monto2):
		detCat = CatalogoDetalle()
		detCat.catalogos = tipo
		detCat.descripcion1 =desc1
		detCat.descripcion2 =desc2	
		detCat.monto1 =monto1
		detCat.monto2 =monto2
		detCat.save()
	
	def cargar_proveedores(self):
		self.proveedor1 = Proveedor()
		self.proveedor1.codigo ="1A"
		self.proveedor1.nombre ="nombre proveedor"
		self.proveedor1.calle  ="calle del proveedor"
		self.proveedor1.numero = "1a interior 3"
		self.proveedor1.colonia ="nueva colonia"
		self.proveedor1.cp = "22222"
		self.proveedor1.pais_cdu_catalogo = "0010001"
		self.proveedor1.estado_cdu_catalogo = 2
		self.proveedor1.rfc = "dasdsa222"
		self.proveedor1.telefono ="23232 ext 2"
		self.proveedor1.email ="dasdsa@dad.com"
		self.proveedor1.comentarios ="si hay comentarios"
		self.proveedor1.save()

	def cargarCompraConDetalle(self):
		data = {
		"invoice" :"KIJ77","proveedor":"1",
		"fec_solicitud" :"01/02/2016","fec_aduana" : "01/03/2016",
		"fec_inventario" : "01/04/2016","fec_real"  : "01/05/2016",
		"casa_cambio": "banxico","precio_dolar" : "17.12",
		"tipo_moneda" : "0040001","transporte" : "por avion",
		"bln_activa" : True,"descripcion" :"la compra llegara pronto",
		"comentarios":"estamos esperando la llegada del producto",
		"compra_detalles" : [
			{"material":"0050004","dsc_material":"Material 222","calibre": "0.008","ancho": "35",
			"largo": "1","peso_kg":"23.12","peso_lb":"0","num_rollo":"ACC22MR","precio":"123.65"},
			],
		}
		response = self.client.post('/compras_con_detalles/',data, format='json')
from django.test import TestCase
from django.db import connection
from datetime import datetime
from rest_framework.test import APIClient
from rest_framework import filters,generics,status
from catalogos.models import Catalogo
from catalogo_detalles.models import CatalogoDetalle
from compras.models import Compra
from compras_detalles.models import CompraDetalle
from proveedores.models import Proveedor
from compras.serializers import CompraSerializer,CompraConDetalleSerializer
from compras_detalles.serializers import CompraDetalleSerializer


class ComprasModelTest(TestCase):
	def setUp(self):
		self.client = APIClient()
		cursor = connection.cursor()
		cursor.execute("ALTER SEQUENCE catalogos_catalogo_id_seq RESTART WITH 1;")
		cursor.execute("ALTER SEQUENCE proveedores_proveedor_id_seq RESTART WITH 1;")
		cursor.execute("ALTER SEQUENCE compras_compra_id_seq RESTART WITH 1;")
		
		self.cargar_catalogos()
		self.cargar_catalogos_detalles()
		self.cargar_proveedores()

	def test_crear_compra(self):
		compra1 = Compra()
		compra1.invoice ="AA1"
		compra1.proveedor = self.proveedor1
		compra1.fec_solicitud = '2015-12-12'
		compra1.fec_aduana = '2015-12-12'
		compra1.fec_inventario = '2015-12-12'
		compra1.fec_real  = '2015-12-12'
		compra1.casa_cambio = 'banxico'
		compra1.precio_dolar = 17.12
		compra1.tipo_moneda = self.detMoneda1
		compra1.transporte = 'por avion'
		compra1.bln_activa = 1
		compra1.descripcion ="la compra llegara pronto"
		compra1.comentarios ="estamos esperando la llegada del producto"
		compra1.save()
		compra_guardada = Compra.objects.all()[0]
		self.assertEqual(compra_guardada.invoice,"AA1")

	def test_serializer_compras(self):
		data = {"invoice":"BB2","proveedor":1,"fec_solicitud":"21/12/2014","fec_aduana":"22/11/2014",
				"fec_inventario":"20/10/2014","fec_real":"19/12/2014","casa_cambio":"bolsa de valores",
				"precio_dolar":17.12,"tipo_moneda":"0040000","transporte":"colectivo","bln_activa":True,
				"descripcion":"la compra","comentarios":"llegara pronto"}
	
		serializer = CompraSerializer(data=data)
		#import ipdb;ipdb.set_trace() 
		self.assertTrue(serializer.is_valid())
		serializer.save()
		exiten = Compra.objects.all()
		self.assertEqual(exiten.count(),1)

	def test_obtener_todas_las_compras_guardadas(self):
		response = self.client.get('/compras/', format='json')
		self.assertEqual(len(response.data),0)

		self.cargar_compra()
		
		response = self.client.get('/compras/', format='json')
		self.assertEqual(len(response.data),1)

	def test_enviar_datos_desde_desde_la_ruta(self):
		response = self.client.get('/compras/', format='json')
		self.assertEqual(len(response.data),0)
		data = {"invoice":"BB2","proveedor":1,"fec_solicitud":"21/12/2014","fec_aduana":"22/11/2014",
				"fec_inventario":"20/10/2014","fec_real":"19/12/2014","casa_cambio":"bolsa de valores",
				"precio_dolar":17.12,"tipo_moneda":"0040000","transporte":"colectivo","bln_activa":True,
				"descripcion":"la compra","comentarios":"llegara pronto"}
	
		response = self.client.post('/compras/',data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response.data["invoice"],"BB2")
		self.assertEqual(response.data["precio_dolar"],'17.12')
		self.assertEqual(response.data["fec_real"],"19/12/2014")

		response = self.client.get('/compras/', format='json')
		self.assertEqual(len(response.data),1)

	def test_obtener_compra_por_pk(self):
		self.cargar_compra()
		response = self.client.get('/compras/1/', format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['invoice'],'AA1')

	def test_obtener_proveedor_por_pk_que_no_existe(self):
	 	self.cargar_compra()
	 	response = self.client.get('/compras/10/', format='json')
	 	self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_modificar_invoice_compra(self):
		self.cargar_compra()

		response = self.client.get('/compras/1/', format='json')
		self.assertEqual(response.data['invoice'],'AA1')

		data = {"invoice":"BB2","proveedor":1,"fec_solicitud":"21/12/2014","fec_aduana":"22/11/2014",
				"fec_inventario":"20/10/2014","fec_real":"19/12/2014","casa_cambio":"bolsa de valores",
				"precio_dolar":17.12,"tipo_moneda":"0040000","transporte":"colectivo","bln_activa":True,
				"descripcion":"la compra","comentarios":"llegara pronto"}
	
		request =self.client.put('/compras/1/', data , format='json')

		response = self.client.get('/compras/1/', format='json')
		self.assertEqual(response.data['invoice'],'BB2')

	def test_eliminar_compra(self):
		self.cargar_compra()

		response = self.client.get('/compras/1/', format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)

		self.client.delete('/compras/1/', format='json')
		
		response = self.client.get('/compras/1/', format='json')
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_buscar_invoice(self):
		self.cargar_compra()
		data = {"invoice":"BB2","proveedor":1,"fec_solicitud":"21/12/2014","fec_aduana":"22/11/2014",
				"fec_inventario":"20/10/2014","fec_real":"19/12/2014","casa_cambio":"bolsa de valores",
				"precio_dolar":17.12,"tipo_moneda":"0040000","transporte":"colectivo","bln_activa":True,
				"descripcion":"la compra","comentarios":"llegara pronto"}

		response = self.client.post('/compras/',data, format='json')

		data = {"invoice":"BB3","proveedor":1,"fec_solicitud":"21/12/2014","fec_aduana":"22/11/2014",
				"fec_inventario":"20/10/2014","fec_real":"19/12/2014","casa_cambio":"bolsa de valores",
				"precio_dolar":17.12,"tipo_moneda":"0040000","transporte":"colectivo","bln_activa":True,
				"descripcion":"la compra","comentarios":"llegara pronto"}

		response = self.client.post('/compras/',data, format='json')

		response = self.client.get('/compras/buscar/AA/', format='json')
		self.assertEqual(len(response.data), 1)

		response = self.client.get('/compras/buscar/BB/', format='json')
		self.assertEqual(len(response.data), 2)

	def test_serializer_compra_con_detalle_incluido(self):
		self.cargar_compra()
		self.carga_detalles_compra()
		comp =  Compra.objects.all().get(pk=1)
		#comps = CompraDetalle.objects.filter(compra__id =1)
		serializer = CompraConDetalleSerializer(instance=comp)
		#import ipdb;ipdb.set_trace()
		datos = serializer.data
		#datos_esperados ={'fec_solicitud': '2015-12-13', 'proveedor': 1, 'transporte': 'por avion', 'bln_activa': True, 'comentarios': 'estamos esperando la llegada del producto', 'precio_dolar': '17.12', 'id': 1, 'invoice': 'AA1', 'casa_cambio': 'banxico', 'fec_inventario': '2015-12-12', 'tipo_moneda': '0040000', 'fec_aduana': '2015-12-12', 'descripcion': 'la compra llegara pronto', 'fec_real': '2015-12-12', 'compra_detalles': ['OrderedDict'([('id', 2), ('compra', 1), ('material', '0050001'), ('dsc_material', 'Material 3'), ('calibre', '3.200'), ('ancho', '2.40'), ('largo', 7), ('peso_kg', '18.19'), ('peso_lb', '10.20'), ('num_rollo', 'BBKS'), ('precio', '28.99')]), 'OrderedDict'([('id', 1), ('compra', 1), ('material', '0050001'), ('dsc_material', 'Material 2'), ('calibre', '1.200'), ('ancho', '3.70'), ('largo', 12), ('peso_kg', '23.12'), ('peso_lb', '30.20'), ('num_rollo', 'ACC22MR'), ('precio', '123.65')])]}
		#self.assertEqual(datos,datos_esperados)

	def test_obtener_compras_con_detalles_desde_desde_la_ruta(self):
		self.cargar_compra()
		self.carga_detalles_compra()
		response = self.client.get('/compras/1/detalles/', format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)		
		self.assertEqual(len(response.data),15)

		response = self.client.get('/compras/2/detalles/', format='json')
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
		self.assertEqual(len(response.data),1)

	# def test_guardar_compras_con_detalles_desde_desde_la_ruta(self):
	# 	data = {
	# 		"invoice" :"KIJ773","proveedor":"1",
	# 		"fec_solicitud" :"01/02/2016","fec_aduana" : "01/03/2016",
	# 		"fec_inventario" : "01/04/2016","fec_real"  : "01/05/2016",
	# 		"casa_cambio": "banxico","precio_dolar" : "17.12",
	# 		"tipo_moneda" : "0040001","transporte" : "por avion",
	# 		"bln_activa" : True,"descripcion" :"la compra llegara pronto",
	# 		"comentarios":"estamos esperando la llegada del producto",
	# 	 	"compra_detalles" : [
	# 	 		{"material":"0050001","dsc_material":"Material 222","calibre": "1.2","ancho": "3.7",
	# 			"largo": "12","peso_kg":"23.12","peso_lb":"0","num_rollo":"ACC22MR","precio":"123.65"}	
	# 	 	],
	# 	}
	# 	serializer = CompraConDetalleSerializer(data=data)
	# 	serializer.is_valid()
	# 	response = serializer.save()

	# 	datos_json = CompraConDetalleSerializer(response)
	# 	self.assertEqual(len(datos_json.data),15)



	def cargar_compra(self):
		self.compra1 = Compra()
		self.compra1.invoice ="AA1"
		self.compra1.proveedor = self.proveedor1
		vfec_sol = datetime.strptime("13/12/2015", '%d/%m/%Y').strftime('%Y-%m-%d') 	
		self.compra1.fec_solicitud =vfec_sol

		self.compra1.fec_aduana = '2015-12-12'
		self.compra1.fec_inventario = '2015-12-12'
		self.compra1.fec_real  = '2015-12-12'
		self.compra1.casa_cambio = 'banxico'
		self.compra1.precio_dolar = 17.12
		self.compra1.tipo_moneda = self.detMoneda1
		self.compra1.transporte = 'por avion'
		self.compra1.bln_activa = 1
		self.compra1.descripcion ="la compra llegara pronto"
		self.compra1.comentarios ="estamos esperando la llegada del producto"
		self.compra1.save()

	def carga_detalles_compra(self):
		data = {"compra":"1","material":"0050001","dsc_material":"Material 2","calibre": "1.2","ancho": "3.7",
				"largo": "12","peso_kg":"23.12","peso_lb":"30.2","num_rollo":"ACC22MR","precio":"123.65"}
	
		serializer = CompraDetalleSerializer(data=data)
		self.assertTrue(serializer.is_valid())
		serializer.save()

		data = {"compra":"1","material":"0050001","dsc_material":"Material 3","calibre": "3.2","ancho": "2.4",
				"largo": "7","peso_kg":"18.19","peso_lb":"10.2","num_rollo":"BBKS","precio":"28.99"}
		serializer = CompraDetalleSerializer(data=data)
		self.assertTrue(serializer.is_valid())
		serializer.save()
		
	def cargar_proveedores(self):
		self.proveedor1 = Proveedor()
		self.proveedor1.codigo ="1A"
		self.proveedor1.nombre ="nombre proveedor"
		self.proveedor1.calle  ="calle del proveedor"
		self.proveedor1.numero = "1a interior 3"
		self.proveedor1.colonia ="nueva colonia"
		self.proveedor1.cp = "22222"
		self.proveedor1.pais_cdu_catalogo = 1
		self.proveedor1.estado_cdu_catalogo = 2
		self.proveedor1.rfc = "dasdsa222"
		self.proveedor1.telefono ="23232 ext 2"
		self.proveedor1.email ="dasdsa@dad.com"
		self.proveedor1.comentarios ="si hay comentarios"
		self.proveedor1.save()
	
	def cargar_catalogos(self):
		self.catalogoPaises = Catalogo()
		self.catalogoPaises.nombre ="Paises"
		self.catalogoPaises.save()

		self.catalogoEstados = Catalogo()
		self.catalogoEstados.nombre ="Estados"
		self.catalogoEstados.save()

		self.catalogoEstados = Catalogo()
		self.catalogoEstados.nombre ="Bancos"
		self.catalogoEstados.save()

		self.catalogoMonedas = Catalogo()
		self.catalogoMonedas.nombre ="Monedas"
		self.catalogoMonedas.save()

		self.catalogoMaterial = Catalogo()
		self.catalogoMaterial.nombre ="Material"
		self.catalogoMaterial.save()


	def cargar_catalogos_detalles(self):
		self.detMoneda1 = CatalogoDetalle()
		self.detMoneda1.catalogos = self.catalogoMonedas
		self.detMoneda1.descripcion1 ="Pesos"
		self.detMoneda1.save()
		
		self.detMoneda2 = CatalogoDetalle()
		self.detMoneda2.catalogos = self.catalogoMonedas
		self.detMoneda2.descripcion1 ="Dolar"
		self.detMoneda2.save()

		self.detMaterial1 = CatalogoDetalle()
		self.detMaterial1.catalogos = self.catalogoMaterial
		self.detMaterial1.descripcion1 ="Material 1"
		self.detMaterial1.save()
		
		self.detMaterial2 = CatalogoDetalle()
		self.detMaterial2.catalogos = self.catalogoMaterial
		self.detMaterial2.descripcion1 ="Material 2"
		self.detMaterial2.save()

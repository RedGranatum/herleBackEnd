from django.test import TestCase
from django.db import connection
from rest_framework.test import APIClient
from rest_framework import filters,generics,status
from catalogos.models import Catalogo
from catalogo_detalles.models import CatalogoDetalle
from compras.models import Compra
from proveedores.models import Proveedor
from compras.serializers import CompraSerializer

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
		data = {"invoice":"BB2","proveedor":1,"fec_solicitud":"2014-12-21","fec_aduana":"2014-11-22",
				"fec_inventario":"2014-10-20","fec_real":"2014-12-19","casa_cambio":"bolsa de valores",
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
		data = {"invoice":"BB2","proveedor":1,"fec_solicitud":"2014-12-21","fec_aduana":"2014-11-22",
				"fec_inventario":"2014-10-20","fec_real":"2014-12-19","casa_cambio":"bolsa de valores",
				"precio_dolar":17.12,"tipo_moneda":"0040000","transporte":"colectivo","bln_activa":True,
				"descripcion":"la compra","comentarios":"llegara pronto"}
	
		response = self.client.post('/compras/',data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response.data["invoice"],"BB2")
		self.assertEqual(response.data["precio_dolar"],'17.12')
		self.assertEqual(response.data["fec_real"],"2014-12-19")

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

		data = {"invoice":"BB2","proveedor":1,"fec_solicitud":"2014-12-21","fec_aduana":"2014-11-22",
				"fec_inventario":"2014-10-20","fec_real":"2014-12-19","casa_cambio":"bolsa de valores",
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
		data = {"invoice":"BB2","proveedor":1,"fec_solicitud":"2014-12-21","fec_aduana":"2014-11-22",
				"fec_inventario":"2014-10-20","fec_real":"2014-12-19","casa_cambio":"bolsa de valores",
				"precio_dolar":17.12,"tipo_moneda":"0040000","transporte":"colectivo","bln_activa":True,
				"descripcion":"la compra","comentarios":"llegara pronto"}

		response = self.client.post('/compras/',data, format='json')

		data = {"invoice":"BB3","proveedor":1,"fec_solicitud":"2014-12-21","fec_aduana":"2014-11-22",
				"fec_inventario":"2014-10-20","fec_real":"2014-12-19","casa_cambio":"bolsa de valores",
				"precio_dolar":17.12,"tipo_moneda":"0040000","transporte":"colectivo","bln_activa":True,
				"descripcion":"la compra","comentarios":"llegara pronto"}

		response = self.client.post('/compras/',data, format='json')

		response = self.client.get('/compras/buscar/AA/', format='json')
		self.assertEqual(len(response.data), 1)

		response = self.client.get('/compras/buscar/BB/', format='json')
		self.assertEqual(len(response.data), 2)

	def cargar_compra(self):
		self.compra1 = Compra()
		self.compra1.invoice ="AA1"
		self.compra1.proveedor = self.proveedor1
		self.compra1.fec_solicitud = '2015-12-12'
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


	def cargar_catalogos_detalles(self):
		self.detMoneda1 = CatalogoDetalle()
		self.detMoneda1.catalogos = self.catalogoMonedas
		self.detMoneda1.descripcion1 ="Pesos"
		self.detMoneda1.save()
		
		self.detMoneda2 = CatalogoDetalle()
		self.detMoneda2.catalogos = self.catalogoMonedas
		self.detMoneda2.descripcion1 ="Dolar"
		self.detMoneda2.save()


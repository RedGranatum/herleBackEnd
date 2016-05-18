from django.test import TestCase
from django.db import connection
from compras_detalles.models import CompraDetalle
from catalogos.models import Catalogo
from catalogo_detalles.models import CatalogoDetalle
from compras.models import Compra
from compras_detalles.serializers import CompraDetalleSerializer

class ComprasDetalleModelTest(TestCase):
	def setUp(self):
		cursor = connection.cursor()
		cursor.execute("ALTER SEQUENCE catalogos_catalogo_id_seq RESTART WITH 1;")
		
		self.cargar_catalogos()
		self.cargar_catalogos_detalles()
		self.cargar_compra()
		
	def test_serializer_compras_detalle(self):


		data = {"compra":"1","material":"0050001","dsc_material":"Material 2","calibre": "1.2","ancho": "3.7",
				"largo": "12","peso_kg":"23.12","peso_lb":"0","num_rollo":"ACC22MR","precio":"123.65"}
	
		serializer = CompraDetalleSerializer(data=data)
		self.assertTrue(serializer.is_valid())
		serializer.save()
		exiten = CompraDetalle.objects.all()
		self.assertEqual(exiten.count(),1)

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
		self.detMaterial1 = CatalogoDetalle()
		self.detMaterial1.catalogos = self.catalogoMaterial
		self.detMaterial1.descripcion1 ="Material 1"
		self.detMaterial1.save()
		
		self.detMaterial2 = CatalogoDetalle()
		self.detMaterial2.catalogos = self.catalogoMaterial
		self.detMaterial2.descripcion1 ="Material 2"
		self.detMaterial2.save()

	def cargar_compra(self):
		self.compra1 = Compra()
		self.compra1.invoice ="AA1"
		self.compra1.proveedor_id = 1
		self.compra1.fec_solicitud ='2015-12-01'
		self.compra1.fec_aduana = '2015-12-12'
		self.compra1.fec_inventario = '2015-12-12'
		self.compra1.fec_real  = '2015-12-12'
		self.compra1.casa_cambio = 'banxico'
		self.compra1.precio_dolar = 17.12
		self.compra1.tipo_moneda_cdu_catalogo = "11"
		self.compra1.transporte = 'por avion'
		self.compra1.bln_activa = 1
		self.compra1.descripcion ="la compra llegara pronto"
		self.compra1.comentarios ="estamos esperando la llegada del producto"
		self.compra1.save()
	

		
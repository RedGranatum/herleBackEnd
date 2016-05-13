from django.test import TestCase
from django.db import connection
from rest_framework import status
from rest_framework.test import APIClient
from catalogos.models import Catalogo
from catalogo_detalles.models import CatalogoDetalle
from .models import Cliente
from .serializers import ClienteSerializer

class ClientesModelTest(TestCase):
	def setUp(self):
		self.client = APIClient()
		cursor = connection.cursor()
		cursor.execute("ALTER SEQUENCE catalogos_catalogo_id_seq RESTART WITH 1;")
		cursor.execute("ALTER SEQUENCE clientes_cliente_id_seq RESTART WITH 1;")

		self.cargar_catalogos()
		self.cargar_catalogos_detalles()

	def test_crear_clientes(self):
		cliente1 = Cliente()
		cliente1.codigo ="2A"
		cliente1.nombre ="nombre cliente"
		cliente1.calle ="calle del cliente"
		cliente1.numero = "interior 4"
		cliente1.cp ="61000"
		cliente1.pais = self.detPaises1
		cliente1.estado = self.detEstado1
		cliente1.rfc = "dsads"
		cliente1.colonia ="nueva colonia"
		cliente1.telefono ="23232"
		cliente1.email = "dsad@dsads.com"
		cliente1.banco = self.detBanco1 
		cliente1.comentarios ="sin comentarios"
		cliente1.save()
		detalles_guardados = Cliente.objects.all()[0]
		self.assertEqual(detalles_guardados.codigo,"2A")
		self.assertEqual(detalles_guardados.nombre,"nombre cliente")

	def test_serializer_clientes(self):
		self.cargar_clientes()
		existen =Cliente.objects.all()
		self.assertEqual(existen.count(), 1)

	def test_obtener_todos_los_clientes_guardados(self):
		response = self.client.get('/clientes/', format='json')
		self.assertEqual(len(response.data),0)

		self.cargar_clientes()
		
		response = self.client.get('/clientes/', format='json')
		self.assertEqual(len(response.data),1)

	def test_enviar_datos_desde_desde_la_ruta(self):
		response = self.client.get('/clientes/', format='json')
		self.assertEqual(len(response.data),0)

		data = {"codigo": "C1","nombre":"El cliente","calle":"conocida","numero":"1","cp":"232","pais":"0010000","estado":"0020000","rfc":"aaa","telefono":"232","email":"","banco": "0030000","comentarios":"no hay en el cliente"}	
		response = self.client.post('/clientes/',data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response.data["codigo"],"C1")
		self.assertEqual(response.data["nombre"],"El cliente")
		self.assertEqual(response.data["banco"],"0030000")

		response = self.client.get('/clientes/', format='json')
		self.assertEqual(len(response.data),1)

	def test_obtener_cliente_por_pk(self):
		self.cargar_clientes()
		response = self.client.get('/clientes/1/', format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['nombre'],'El cliente')

	def test_obtener_cliente_por_pk_que_no_existe(self):
		self.cargar_clientes()
		response = self.client.get('/clientes/11/', format='json')
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_modificar_nombre_cliente(self):
		self.cargar_clientes()

		response = self.client.get('/clientes/1/', format='json')
		self.assertEqual(response.data['nombre'],'El cliente')

		data = {"codigo": "C1","nombre":"El cliente se modifico","calle":"conocida","numero":"1","cp":"232","pais":"0010000","estado":"0020000","rfc":"aaa","telefono":"232","email":"","banco": "0030000","comentarios":"no hay en el cliente"}
		request =self.client.put('/clientes/1/', data , format='json')

		response = self.client.get('/clientes/1/', format='json')
		self.assertEqual(response.data['nombre'],'El cliente se modifico')

	def test_eliminar_cliente(self):
		self.cargar_clientes()

		response = self.client.get('/clientes/1/', format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)

		self.client.delete('/clientes/1/', format='json')
		
		response = self.client.get('/clientes/1/', format='json')
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_buscar_cliente_por_codigo_nombre_o_rfc(self):
		self.cargar_clientes()
		data = {"codigo": "E1","nombre":"El Agua","calle":"conocida","numero":"1","cp":"232","pais":"0010000","estado":"0020000","rfc":"rasa","telefono":"232","email":"","comentarios":"no hay"}
		response = self.client.post('/clientes/',data, format='json')

		data = {"codigo": "E2","nombre":"El Agua del oriente","calle":"conocida","numero":"1","cp":"232","pais":"0010000","estado":"0020000","rfc":"dsa","telefono":"232","email":"","comentarios":"no hay"}
		response = self.client.post('/clientes/',data, format='json')

		data = {"codigo": "Nuev23","nombre":"El pescadito dsa","calle":"conocida","numero":"1","cp":"232","pais":"0010000","estado":"0020000","rfc":"cccc2","telefono":"232","email":"","comentarios":"no hay"}
		response = self.client.post('/clientes/',data, format='json')

		data = {"codigo": "A33dsa","nombre":"Nueva vida","calle":"conocida","numero":"1","cp":"232","pais":"0010000","estado":"0020000","rfc":"223ds","telefono":"232","email":"","comentarios":"no hay"}
		response = self.client.post('/clientes/',data, format='json')

		response = self.client.get('/clientes/buscar/clie/', format='json')
		self.assertEqual(len(response.data), 1)

		response = self.client.get('/clientes/buscar/agua/', format='json')
		#import ipdb;ipdb.set_trace()
		self.assertEqual(len(response.data), 2)

		response = self.client.get('/clientes/buscar/nuev/', format='json')
		self.assertEqual(len(response.data), 2)

		response = self.client.get('/clientes/buscar/dsa/', format='json')
		self.assertEqual(len(response.data), 3)



	def cargar_clientes(self):
		data = {"codigo": "C1","nombre":"El cliente","calle":"conocida","numero":"1","cp":"232","pais":"0010000","estado":"0020000","rfc":"aaa","telefono":"232","email":"","banco": "0030000","comentarios":"no hay en el cliente"}
		serializer = ClienteSerializer(data=data)
		self.assertTrue(serializer.is_valid())
		serializer.save()

	def cargar_catalogos(self):
		self.catalogoPaises = Catalogo()
		self.catalogoPaises.nombre ="Paises"
		self.catalogoPaises.save()

		self.catalogoEstados = Catalogo()
		self.catalogoEstados.nombre ="Estados"
		self.catalogoEstados.save()

		self.catalogoBancos = Catalogo()
		self.catalogoBancos.nombre ="Bancos"
		self.catalogoBancos.save()



	def cargar_catalogos_detalles(self):
		self.detPaises1 = CatalogoDetalle()
		self.detPaises1.catalogos = self.catalogoPaises
		self.detPaises1.descripcion1 ="Mexico"
		self.detPaises1.save()

		self.detPaises2 = CatalogoDetalle()
		self.detPaises2.catalogos = self.catalogoPaises
		self.detPaises2.descripcion1 ="China"
		self.detPaises2.save()	

		self.detEstado1 = CatalogoDetalle()
		self.detEstado1.catalogos = self.catalogoEstados
		self.detEstado1.descripcion1 ="Puebla"
		self.detEstado1.save()	


		self.detEstado2 = CatalogoDetalle()
		self.detEstado2.catalogos = self.catalogoEstados
		self.detEstado2.descripcion1 ="lugar de china"
		self.detEstado2.save()


		self.detBanco1 = CatalogoDetalle()
		self.detBanco1.catalogos = self.catalogoBancos
		self.detBanco1.descripcion1 ="Bancomer"
		self.detBanco1.save()
			
from django.db import connection
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from catalogos.models import Catalogo
from catalogos.serializers import CatalogoSerializer
# Create your tests here.

class CatalogoModelTest(TestCase):
	def setUp(self): 
		self.client = APIClient()
		user = User.objects.create_user(username='usuario1')
		self.client.force_authenticate(user=user)

		cursor = connection.cursor()
		cursor.execute("ALTER SEQUENCE catalogos_catalogo_id_seq RESTART WITH 1;")

	def test_guardar_obtener_catalogos(self):
		catalogo1 = Catalogo()
		catalogo1.nombre ="Proveedores"
		catalogo1.save()

		catalogo2 = Catalogo()
		catalogo2.nombre ="Clientes"
		catalogo2.save()

		catalogos_guardados = Catalogo.objects.all()
		self.assertEqual(catalogos_guardados.count(), 2)
		c1 = catalogos_guardados[0]
		c2 = catalogos_guardados[1]
		self.assertEqual(c1.nombre,"Proveedores")
		self.assertEqual(c2.nombre,"Clientes")

	def test_serializer_catalogo(self):
		self.assertEqual(Catalogo.objects.count(), 0)
		serializer = CatalogoSerializer(data={'nombre': 'Proveedores'})
		self.assertTrue(serializer.is_valid())
		serializer.save()
		self.assertEqual(Catalogo.objects.count(), 1)
		self.assertEqual(serializer.data,{'nombre': 'Proveedores', 'id': 1})

	def test_enviar_datos_desde_desde_la_ruta(self):
		response = self.client.post('/catalogos/', {'nombre': 'Proveedores'}, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Catalogo.objects.count(), 1)
		self.assertEqual(response.data, {'nombre': 'Proveedores', 'id': 1})

		response = self.client.post('/catalogos/', {'nombre': 'Clientes'}, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Catalogo.objects.count(), 2)
		self.assertEqual(response.data, {'nombre': 'Clientes', 'id': 2})	

	def test_nombre_de_catalogo_es_unico(self):
		response = self.client.post('/catalogos/', {'nombre': 'Proveedores'}, format='json')
		response = self.client.post('/catalogos/', {'nombre': 'Proveedores'}, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response.data,{'nombre': ['El catalogo ya existe']})
		self.assertEqual(Catalogo.objects.count(), 1)

	def test_nombre_de_catalogo_no_debe_tener_espacios(self):
		response = self.client.post('/catalogos/', {'nombre': '      Proveedores       '}, format='json')
		self.assertEqual(response.data['nombre'],'Proveedores')		

	def test_obtener_todos_los_catalogos_guardados(self):
		self.cargar_catalogos()
		response = self.client.get('/catalogos/', format='json')
		self.assertEqual(len(response.data),2)

	def test_obtener_catalogo_por_pk(self):
		self.cargar_catalogos()
		response = self.client.get('/catalogos/2/', format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['nombre'],'Clientes')

	def test_obtener_catalogo_por_pk_que_no_existe(self):
		self.cargar_catalogos()
		response = self.client.get('/catalogos/3/', format='json')
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_modificar_nombre_catalogo(self):
		self.cargar_catalogos()
		self.client.put('/catalogos/2/', {'nombre': 'Cliente'}, format='json')
		response = self.client.get('/catalogos/2/', format='json')
		self.assertEqual(response.data, {'id': 2, 'nombre': 'Cliente'})

	def test_eliminar_catalogo(self):
		self.cargar_catalogos()
		self.client.delete('/catalogos/2/', format='json')
		response = self.client.get('/catalogos/2/', format='json')
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
	
	def test_buscar_catalogo_que_contenga_en_el_nombre_un_valor(self):
		self.cargar_catalogos()
		self.client.post('/catalogos/', {'nombre': 'Clientes2'}, format='json')
		self.client.post('/catalogos/', {'nombre': 'Pacientes'}, format='json')
		self.client.post('/catalogos/', {'nombre': 'Pais'}, format='json')
		self.client.post('/catalogos/', {'nombre': 'Parientes'}, format='json')
		response = self.client.get('/catalogos/buscar/?valor_buscado=entes', format='json')
		#import ipdb;ipdb.set_trace()
		self.assertEqual(len(response.data),4)

	def cargar_catalogos(self):
		self.client.post('/catalogos/', {'nombre': 'Proveedores'}, format='json')
		self.client.post('/catalogos/', {'nombre': 'Clientes'}, format='json')
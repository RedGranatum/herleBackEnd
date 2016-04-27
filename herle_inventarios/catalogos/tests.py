from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from catalogos.models import Catalogo
from catalogos.serializers import CatalogoSerializer
# Create your tests here.

class CatalogoModelTest(TestCase):
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

	def test_api_rest_guardar_catalogo(self):
			client = APIClient()
			response = client.post('/catalogos/', {'nombre': 'Proveedores'}, format='json')
			self.assertEqual(response.status_code, status.HTTP_201_CREATED)
			self.assertEqual(Catalogo.objects.count(), 1)
			self.assertEqual(Catalogo.objects.get().nombre, 'Proveedores')

			#response = client.post('/catalogos/', {'nombre': 'Clientes'}, format='json')
			#self.assertEqual(response,"")
			#self.assertEqual(Catalogo.objects.count(), 2)
			#self.assertEqual(Catalogo.objects.get(nombre='Clientes').nombre, 'Clientes')
	def test_serializer_catalogo(self):
		python_dict = {"nombre": "Proveedores"}
		serializer = CatalogoSerializer(data={'nombre': 'Proveedores'})
		self.assertTrue(serializer.is_valid())
		self.assertEqual(serializer.data,python_dict)



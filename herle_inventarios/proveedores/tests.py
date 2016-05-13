from django.db import connection
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from catalogos.models import Catalogo
from catalogo_detalles.models import CatalogoDetalle
from proveedores.models import Proveedor
from proveedores.serializers import ProveedorSerializer

class ProovedoresModelTest(TestCase):
	def setUp(self): 
		self.client = APIClient()
		cursor = connection.cursor()
		cursor.execute("ALTER SEQUENCE catalogos_catalogo_id_seq RESTART WITH 1;")
		cursor.execute("ALTER SEQUENCE proveedores_proveedor_id_seq RESTART WITH 1;")
		
		self.cargar_catalogos()
		self.cargar_catalogos_detalles()


	
	def test_crear_proveedores(self):
		proveedor1 = Proveedor()
		proveedor1.codigo ="1A"
		proveedor1.nombre ="nombre proveedor"
		proveedor1.calle  ="calle del proveedor"
		proveedor1.numero = "1a interior 3"
		proveedor1.colonia ="nueva colonia"
		proveedor1.cp = "22222"
		proveedor1.pais = self.detPaises1
		proveedor1.estado = self.detEstado1 
		proveedor1.rfc = "dasdsa222"
		proveedor1.telefono ="23232 ext 2"
		proveedor1.email ="dasdsa@dad.com"
		proveedor1.comentarios ="si hay comentarios"
		proveedor1.save()		
		detalles_guardados = Proveedor.objects.all()[0]
		self.assertEqual(detalles_guardados.codigo,"1A")
		self.assertEqual(detalles_guardados.nombre,"nombre proveedor")

	def test_serializer_proveedores(self):
		numero_cat= CatalogoDetalle.objects.all()
		data = {"codigo": "A1","nombre":"El proveedor","calle":"conocida","numero":"1","cp":"232","pais":"0010000","estado":"0020000","rfc":"aaa","telefono":"232","email":"","comentarios":"no hay"}
		serializer = ProveedorSerializer(data=data)
		self.assertTrue(serializer.is_valid())
		serializer.save()
		existen =Proveedor.objects.all()
		#import ipdb;ipdb.set_trace()
		self.assertEqual(existen.count(), 1)


#	def test_serializer_proveedores_con_pais_incorrecto(self):
#		numero_cat= CatalogoDetalle.objects.all()
#		data = {"codigo": "A1","nombre":"El proveedor","calle":"conocida","numero":"1","cp":"232","pais":"0020000","estado":"0010000","rfc":"aaa","telefono":"232","email":"","comentarios":"no hay"}
#		serializer = ProveedorDetalleSerializer(data=data)
#		self.assertFalse(serializer.is_valid())
#		self.assertEqual(serializer.errors,"")
	
	def test_obtener_todos_los_proveedores_guardados(self):
		response = self.client.get('/proveedores/', format='json')
		self.assertEqual(len(response.data),0)

		self.cargar_proveedores()
		
		response = self.client.get('/proveedores/', format='json')
		self.assertEqual(len(response.data),1)

	def test_enviar_datos_desde_desde_la_ruta(self):
		response = self.client.get('/proveedores/', format='json')
		self.assertEqual(len(response.data),0)

		data = {"codigo": "A1","nombre":"El proveedor","calle":"conocida","numero":"1","cp":"232","pais":"0010000","estado":"0020000","rfc":"aaa","telefono":"232","email":"","comentarios":"no hay"}
		response = self.client.post('/proveedores/',data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response.data["codigo"],"A1")
		self.assertEqual(response.data["nombre"],"El proveedor")
		self.assertEqual(response.data["pais"],"0010000")

		response = self.client.get('/proveedores/', format='json')
		self.assertEqual(len(response.data),1)

	def test_obtener_proveedor_por_pk(self):
		self.cargar_proveedores()
		response = self.client.get('/proveedores/1/', format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['nombre'],'El proveedor')

	def test_obtener_proveedor_por_pk_que_no_existe(self):
		self.cargar_proveedores()
		response = self.client.get('/proveedores/10/', format='json')
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_modificar_nombre_proveedor(self):
		self.cargar_proveedores()

		response = self.client.get('/proveedores/1/', format='json')
		self.assertEqual(response.data['nombre'],'El proveedor')

		data = {"codigo": "A1","nombre":"El proveedor modificado","calle":"conocida","numero":"1","cp":"232","pais":"0010000","estado":"0020000","rfc":"aaa","telefono":"232","email":"","comentarios":"no hay"}
		request =self.client.put('/proveedores/1/', data , format='json')

		response = self.client.get('/proveedores/1/', format='json')
		self.assertEqual(response.data['nombre'],'El proveedor modificado')

	def test_eliminar_proveedor(self):
		self.cargar_proveedores()

		response = self.client.get('/proveedores/1/', format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)

		self.client.delete('/proveedores/1/', format='json')
		
		response = self.client.get('/proveedores/1/', format='json')
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_buscar_proveedor_por_codigo_nombre_o_rfc(self):
		self.cargar_proveedores()
		data = {"codigo": "E1","nombre":"El Agua","calle":"conocida","numero":"1","cp":"232","pais":"0010000","estado":"0020000","rfc":"rasa","telefono":"232","email":"","comentarios":"no hay"}
		response = self.client.post('/proveedores/',data, format='json')

		data = {"codigo": "E2","nombre":"El Agua del oriente","calle":"conocida","numero":"1","cp":"232","pais":"0010000","estado":"0020000","rfc":"dsa","telefono":"232","email":"","comentarios":"no hay"}
		response = self.client.post('/proveedores/',data, format='json')

		data = {"codigo": "Nuev23","nombre":"El pescadito dsa","calle":"conocida","numero":"1","cp":"232","pais":"0010000","estado":"0020000","rfc":"cccc2","telefono":"232","email":"","comentarios":"no hay"}
		response = self.client.post('/proveedores/',data, format='json')

		data = {"codigo": "A33dsa","nombre":"Nueva vida","calle":"conocida","numero":"1","cp":"232","pais":"0010000","estado":"0020000","rfc":"223ds","telefono":"232","email":"","comentarios":"no hay"}
		response = self.client.post('/proveedores/',data, format='json')

		response = self.client.get('/proveedores/buscar/proveedor/', format='json')
		self.assertEqual(len(response.data), 1)

		response = self.client.get('/proveedores/buscar/agua/', format='json')
		#import ipdb;ipdb.set_trace()
		self.assertEqual(len(response.data), 2)

		response = self.client.get('/proveedores/buscar/nuev/', format='json')
		self.assertEqual(len(response.data), 2)

		response = self.client.get('/proveedores/buscar/dsa/', format='json')
		self.assertEqual(len(response.data), 3)

	def cargar_proveedores(self):
		data = {"codigo": "A1","nombre":"El proveedor","calle":"conocida","numero":"1","cp":"232","pais":"0010000","estado":"0020000","rfc":"aaa","telefono":"232","email":"","comentarios":"no hay"}
		serializer = ProveedorSerializer(data=data)
		self.assertTrue(serializer.is_valid())
		serializer.save()
		existen =Proveedor.objects.all()

	def cargar_catalogos(self):
		self.catalogoPaises = Catalogo()
		self.catalogoPaises.nombre ="Paises"
		self.catalogoPaises.save()

		self.catalogoEstados = Catalogo()
		self.catalogoEstados.nombre ="Estados"
		self.catalogoEstados.save()


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
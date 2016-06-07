from django.db import connection
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from catalogos.models import Catalogo
from catalogo_detalles.models import CatalogoDetalle
from catalogo_detalles.serializers import CatalogoDetalleSerializer

class CatalogoDetalleModelTest(TestCase):
	def setUp(self): 
		self.client = APIClient()
		cursor = connection.cursor()
		cursor.execute("ALTER SEQUENCE catalogos_catalogo_id_seq RESTART WITH 1;")
		self.cargar_catalogos()

	def test_detalle_sin_catalogo_dado_de_alta(self):
		catalogo_det1 = CatalogoDetalle()
		catalogo_det1.catalogos = self.catalogo1
		catalogo_det1.descripcion1 ="detalle"
		catalogo_det1.save()		
		detalles_guardados = CatalogoDetalle.objects.all()[0]
		self.assertEqual(detalles_guardados.descripcion1,'detalle')
		self.assertEqual(detalles_guardados.cdu_catalogo,'0010000')

		catalogo_det1 = CatalogoDetalle()
		catalogo_det1.catalogos = self.catalogo1
		catalogo_det1.descripcion1 ="detalle2"
		catalogo_det1.save()		
		detalles_guardados = CatalogoDetalle.objects.all()[1]
		self.assertEqual(detalles_guardados.cdu_catalogo,'0010001')

	def test_serializer_catalogo(self):
		self.cargar_catalogos_detalles()
		serializer = CatalogoDetalleSerializer(data={"num_dcatalogo":0,"descripcion1":"detalle","descripcion2":"","monto1":"0.00","monto2":"0.00","cdu_default":"","catalogos":1})
		self.assertTrue(serializer.is_valid())
		serializer.save()
		existen =CatalogoDetalle.objects.all()
		self.assertEqual(existen.count(), 4)

	def test_obtener_todos_los_catalogos_detalles_guardados(self):
		self.cargar_catalogos_detalles()
		response = self.client.get('/catalogo_detalles/', format='json')
		self.assertEqual(len(response.data),3)

	def test_enviar_datos_desde_desde_la_ruta(self):
		self.cargar_catalogos_detalles()
		data ={"num_dcatalogo":0,"descripcion1":"detalle","descripcion2":"","monto1":"0.00","monto2":"0.00","cdu_default":"","catalogos":1}
		response = self.client.post('/catalogo_detalles/',data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		#import ipdb;ipdb.set_trace()
		self.assertEqual(response.data["cdu_catalogo"],'0010002')
		self.assertEqual(response.data["catalogos"],1)
		self.assertEqual(response.data["num_dcatalogo"],2)

	def test_siempre_genera_un_nueva_clave(self):
		self.cargar_catalogos_detalles()
		data ={"cdu_catalogo":"","num_dcatalogo":0,"descripcion1":"detalle","descripcion2":"","monto1":"0.00","monto2":"0.00","cdu_default":"","catalogos":1}
		response = self.client.post('/catalogo_detalles/',data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		response = self.client.post('/catalogo_detalles/',data, format='json')

		self.assertEqual(response.data["cdu_catalogo"],'0010003')
		self.assertEqual(response.data["catalogos"],1)
		self.assertEqual(response.data["num_dcatalogo"],3)


	def test_obtener_catalogodetalle_por_pk(self):
		self.cargar_catalogos_detalles()
		response = self.client.get('/catalogo_detalles/0010000/', format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['descripcion1'],'detalle')

	def test_obtener_catalogodetalle_por_pk_que_no_existe(self):
		self.cargar_catalogos_detalles()
		response = self.client.get('/catalogo_detalles/0010002/', format='json')
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_modificar_nombre_catalogodetalle(self):
		self.cargar_catalogos_detalles()
		data ={"cdu_catalogo":"","num_dcatalogo":0,"descripcion1":"detalle modificado","descripcion2":"","monto1":"0.00","monto2":"0.00","cdu_default":"","catalogos":1}
		
		request =self.client.put('/catalogo_detalles/0010000/', data , format='json')
		#import ipdb;ipdb.set_trace()
		response = self.client.get('/catalogo_detalles/0010000/', format='json')
		self.assertEqual(response.data['descripcion1'],'detalle modificado')


	def test_eliminar_catalogo(self):
		self.cargar_catalogos_detalles()
		self.client.delete('/catalogo_detalles/0010000/', format='json')
		response = self.client.get('/catalogo_detalles/0010000/', format='json')
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_obtener_detalles_de_un_cdu_catalogo(self):
		self.cargar_catalogos_detalles()
		response = self.client.get('/catalogos/1/catalogo_detalles/', format='json')
		#import ipdb;ipdb.set_trace()
		self.assertEqual(len(response.data),2)

		response = self.client.get('/catalogos/2/catalogo_detalles/', format='json')
		self.assertEqual(len(response.data),1)

	def test_obtener_detalles_de_un_detalle_por_medio_del_cdu_default(self):
		self.cargar_catalogos_detalles();
		response = self.client.get('/catalogo_detalles/0020000/catalogo_detalles/', format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data),0)

		data ={"cdu_catalogo":"","num_dcatalogo":0,"descripcion1":"detalle","descripcion2":"","monto1":"0.00","monto2":"0.00","cdu_default":"0020000","catalogos":1}
		self.client.post('/catalogo_detalles/',data, format='json')
		self.client.post('/catalogo_detalles/',data, format='json')

		response = self.client.get('/catalogo_detalles/0020000/catalogo_detalles/', format='json')
		self.assertEqual(len(response.data),2)
	
	def test_buscar_detalle_por_descripcion(self):
		self.cargar_catalogos_detalles();
		response = self.client.get('/catalogo_detalles/buscar/?valor_buscado=deta', format='json')
		self.assertEqual(len(response.data),2)

		data ={"cdu_catalogo":"","num_dcatalogo":0,"descripcion1":"Numero detallista","descripcion2":"","monto1":"0.00","monto2":"0.00","cdu_default":"","catalogos":2}
		self.client.post('/catalogo_detalles/',data, format='json')
		response = self.client.get('/catalogo_detalles/buscar/?valor_buscado=deta', format='json')
		self.assertEqual(len(response.data),3)	
	


	def cargar_catalogos(self):
		self.catalogo1 = Catalogo()
		self.catalogo1.nombre ="Catalogo0"
		self.catalogo1.save()

		self.catalogo2 = Catalogo()
		self.catalogo2.nombre ="Catalogo1"
		self.catalogo2.save()


	def cargar_catalogos_detalles(self):
		catalogo_det1 = CatalogoDetalle()
		catalogo_det1.catalogos = self.catalogo1
		catalogo_det1.descripcion1 ="detalle"
		catalogo_det1.save()

		catalogo_det2 = CatalogoDetalle()
		catalogo_det2.catalogos = self.catalogo1
		catalogo_det2.descripcion1 ="detalle2"
		catalogo_det2.save()	

		catalogo_det3 = CatalogoDetalle()
		catalogo_det3.catalogos = self.catalogo2
		catalogo_det3.descripcion1 ="otro catalogo"
		catalogo_det3.save()	

	
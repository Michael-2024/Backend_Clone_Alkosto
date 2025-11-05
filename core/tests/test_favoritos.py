"""
Pruebas Unitarias - Módulo de Favoritos
RF10 - Añadir a favoritos
RF12 - Ver favoritos
"""

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from core.models import Producto, Categoria, Marca, Usuario, Favorito
from rest_framework.authtoken.models import Token
from decimal import Decimal
from django.utils.text import slugify


class AgregarFavoritoTestCase(APITestCase):
    """
    RF10 - Añadir a favoritos
    Casos de prueba para agregar productos a favoritos
    """
    
    def setUp(self):
        """Configuración inicial"""
        self.client = APIClient()
        self.favoritos_url = '/api/favoritos/'
        
        # Crear usuario y autenticar
        self.usuario = Usuario.objects.create_user(
            email='favoritos@test.com',
            nombre='Usuario',
            apellido='Test',
            password='Test123!'
        )
        self.token = Token.objects.create(user=self.usuario)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Crear categoría y marca
        self.categoria = Categoria.objects.create(
            nombre='Tecnología',
            slug=slugify('Tecnología'),
            descripcion='Productos tecnológicos'
        )
        self.marca = Marca.objects.create(
            nombre='Samsung',
            descripcion='Marca Samsung'
        )
        
        # Crear productos de prueba
        self.producto1 = Producto.objects.create(
            nombre='Samsung Galaxy S21',
            descripcion='Smartphone de alta gama',
            precio=Decimal('2500000.00'),
            stock=10,
            sku='SGAL-S21-001',
            id_categoria=self.categoria,
            id_marca=self.marca
        )
        
        self.producto2 = Producto.objects.create(
            nombre='Samsung TV 55"',
            descripcion='Smart TV 4K',
            precio=Decimal('3000000.00'),
            stock=5,
            sku='STV-55-001',
            id_categoria=self.categoria,
            id_marca=self.marca
        )
    
    def test_agregar_favorito_exitoso(self):
        """
        CP37: Agregar producto a favoritos exitosamente
        Entrada: producto_id válido, usuario autenticado
        Salida Esperada: Status 201, favorito creado
        """
        payload = {
            'producto': self.producto1.id_producto
        }
        
        response = self.client.post(
            self.favoritos_url,
            payload,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar que el favorito existe en la BD
        favorito_exists = Favorito.objects.filter(
            usuario=self.usuario,
            producto=self.producto1
        ).exists()
        self.assertTrue(favorito_exists)
    
    def test_agregar_favorito_sin_autenticacion(self):
        """
        CP38: Intentar agregar favorito sin autenticación
        Entrada: Request sin token
        Salida Esperada: Error 401, no autenticado
        """
        self.client.credentials()  # Eliminar credenciales
        
        payload = {
            'producto': self.producto1.id_producto
        }
        
        response = self.client.post(
            self.favoritos_url,
            payload,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_agregar_favorito_duplicado(self):
        """
        CP39: Intentar agregar el mismo producto dos veces
        Entrada: Producto ya en favoritos
        Salida Esperada: Error 400 o mensaje indicando que ya existe
        """
        # Crear favorito inicial
        Favorito.objects.create(
            usuario=self.usuario,
            producto=self.producto1
        )
        
        payload = {
            'producto': self.producto1.id_producto
        }
        
        response = self.client.post(
            self.favoritos_url,
            payload,
            format='json'
        )
        
        # Debe retornar error o mensaje de duplicado
        self.assertIn(
            response.status_code,
            [status.HTTP_400_BAD_REQUEST, status.HTTP_200_OK]
        )
    
    def test_agregar_favorito_producto_inexistente(self):
        """
        CP40: Agregar favorito con producto inexistente
        Entrada: producto_id que no existe
        Salida Esperada: Error 400 o 404
        """
        payload = {
            'producto': 99999
        }
        
        response = self.client.post(
            self.favoritos_url,
            payload,
            format='json'
        )
        
        self.assertIn(
            response.status_code,
            [status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND]
        )
    
    def test_agregar_multiples_favoritos(self):
        """
        CP41: Agregar múltiples productos a favoritos
        Entrada: Varios productos diferentes
        Salida Esperada: Todos agregados exitosamente
        """
        # Agregar primer producto
        response1 = self.client.post(
            self.favoritos_url,
            {'producto': self.producto1.id_producto},
            format='json'
        )
        
        # Agregar segundo producto
        response2 = self.client.post(
            self.favoritos_url,
            {'producto': self.producto2.id_producto},
            format='json'
        )
        
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        
        # Verificar que ambos existen
        count = Favorito.objects.filter(usuario=self.usuario).count()
        self.assertEqual(count, 2)


class ListarFavoritosTestCase(APITestCase):
    """
    RF12 - Ver favoritos
    Casos de prueba para listar productos favoritos
    """
    
    def setUp(self):
        """Configuración inicial"""
        self.client = APIClient()
        self.favoritos_url = '/api/favoritos/'
        
        # Crear usuario y autenticar
        self.usuario = Usuario.objects.create_user(
            email='ver_favoritos@test.com',
            nombre='Usuario',
            apellido='Test',
            password='Test123!'
        )
        self.token = Token.objects.create(user=self.usuario)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Crear categoría y marca
        categoria = Categoria.objects.create(
            nombre='Tecnología',
            slug=slugify('Tecnología')
        )
        marca = Marca.objects.create(nombre='Samsung')
        
        # Crear productos
        self.producto1 = Producto.objects.create(
            nombre='Producto Favorito 1',
            precio=Decimal('1000000.00'),
            stock=10,
            sku='PFAV-001',
            id_categoria=categoria,
            id_marca=marca
        )
        
        self.producto2 = Producto.objects.create(
            nombre='Producto Favorito 2',
            precio=Decimal('2000000.00'),
            stock=5,
            sku='PFAV-002',
            id_categoria=categoria,
            id_marca=marca
        )
        
        # Agregar productos a favoritos
        Favorito.objects.create(usuario=self.usuario, producto=self.producto1)
        Favorito.objects.create(usuario=self.usuario, producto=self.producto2)
    
    def test_listar_favoritos_exitoso(self):
        """
        CP42: Listar todos los favoritos del usuario
        Entrada: Usuario autenticado con favoritos
        Salida Esperada: Status 200, lista de favoritos
        """
        response = self.client.get(self.favoritos_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Verificar que contiene los productos correctos
        productos_ids = [f['producto']['id_producto'] if isinstance(f, dict) else f.producto.id_producto 
                        for f in response.data]
        self.assertIn(self.producto1.id_producto, productos_ids)
        self.assertIn(self.producto2.id_producto, productos_ids)
    
    def test_listar_favoritos_sin_autenticacion(self):
        """
        CP43: Intentar listar favoritos sin autenticación
        Entrada: Request sin token
        Salida Esperada: Error 401
        """
        self.client.credentials()  # Eliminar credenciales
        response = self.client.get(self.favoritos_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_listar_favoritos_vacio(self):
        """
        CP44: Listar favoritos cuando no hay ninguno
        Entrada: Usuario sin favoritos
        Salida Esperada: Status 200, lista vacía
        """
        # Crear nuevo usuario sin favoritos
        nuevo_usuario = Usuario.objects.create_user(
            email='sin_favoritos@test.com',
            nombre='Sin',
            apellido='Favoritos',
            password='Test123!'
        )
        nuevo_token = Token.objects.create(user=nuevo_usuario)
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + nuevo_token.key)
        response = self.client.get(self.favoritos_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    
    def test_favoritos_solo_del_usuario_autenticado(self):
        """
        CP45: Verificar que solo se muestran favoritos del usuario logueado
        Entrada: Usuario 1 autenticado
        Salida Esperada: Solo favoritos del Usuario 1, no de otros
        """
        # Crear otro usuario con favoritos
        otro_usuario = Usuario.objects.create_user(
            email='otro@test.com',
            nombre='Otro',
            apellido='Usuario',
            password='Test123!'
        )
        
        categoria = Categoria.objects.first()
        marca = Marca.objects.first()
        
        producto_otro = Producto.objects.create(
            nombre='Producto de Otro',
            precio=Decimal('500000.00'),
            stock=10,
            sku='POTRO-001',
            id_categoria=categoria,
            id_marca=marca
        )
        
        Favorito.objects.create(usuario=otro_usuario, producto=producto_otro)
        
        # Listar favoritos del usuario original
        response = self.client.get(self.favoritos_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Solo los 2 originales
        
        # Verificar que NO contiene el producto del otro usuario
        productos_ids = [f['producto']['id_producto'] if isinstance(f, dict) else f.producto.id_producto 
                        for f in response.data]
        self.assertNotIn(producto_otro.id_producto, productos_ids)


class EliminarFavoritoTestCase(APITestCase):
    """
    RF10/RF12 - Eliminar de favoritos
    Casos de prueba para eliminar productos de favoritos
    """
    
    def setUp(self):
        """Configuración inicial"""
        self.client = APIClient()
        
        # Crear usuario y autenticar
        self.usuario = Usuario.objects.create_user(
            email='eliminar_favorito@test.com',
            nombre='Usuario',
            apellido='Test',
            password='Test123!'
        )
        self.token = Token.objects.create(user=self.usuario)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Crear producto
        categoria = Categoria.objects.create(
            nombre='Tecnología',
            slug=slugify('Tecnología')
        )
        marca = Marca.objects.create(nombre='Samsung')
        
        self.producto = Producto.objects.create(
            nombre='Producto a Eliminar',
            precio=Decimal('1000000.00'),
            stock=10,
            sku='PELIM-001',
            id_categoria=categoria,
            id_marca=marca
        )
        
        # Crear favorito
        self.favorito = Favorito.objects.create(
            usuario=self.usuario,
            producto=self.producto
        )
    
    def test_eliminar_favorito_exitoso(self):
        """
        CP46: Eliminar producto de favoritos
        Entrada: ID de favorito válido
        Salida Esperada: Status 204, favorito eliminado
        """
        url = f'/api/favoritos/{self.favorito.id_favorito}/'
        response = self.client.delete(url)
        
        self.assertIn(
            response.status_code,
            [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK]
        )
        
        # Verificar que fue eliminado
        favorito_exists = Favorito.objects.filter(id_favorito=self.favorito.id_favorito).exists()
        self.assertFalse(favorito_exists)
    
    def test_eliminar_favorito_inexistente(self):
        """
        CP47: Eliminar favorito que no existe
        Entrada: ID de favorito inexistente
        Salida Esperada: Error 404
        """
        url = '/api/favoritos/99999/'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_eliminar_favorito_de_otro_usuario(self):
        """
        CP48: Intentar eliminar favorito de otro usuario
        Entrada: ID de favorito que pertenece a otro usuario
        Salida Esperada: Error 403 o 404
        """
        # Crear otro usuario con favorito
        otro_usuario = Usuario.objects.create_user(
            email='otro@test.com',
            nombre='Otro',
            apellido='Usuario',
            password='Test123!'
        )
        
        favorito_otro = Favorito.objects.create(
            usuario=otro_usuario,
            producto=self.producto
        )
        
        url = f'/api/favoritos/{favorito_otro.id_favorito}/'
        response = self.client.delete(url)
        
        # Debe retornar error (no puede eliminar favoritos de otros)
        self.assertIn(
            response.status_code,
            [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND]
        )
        
        # Verificar que NO fue eliminado
        favorito_exists = Favorito.objects.filter(id_favorito=favorito_otro.id_favorito).exists()
        self.assertTrue(favorito_exists)
    
    def test_eliminar_favorito_sin_autenticacion(self):
        """
        CP49: Eliminar favorito sin autenticación
        Entrada: Request sin token
        Salida Esperada: Error 401
        """
        self.client.credentials()  # Eliminar credenciales
        
        url = f'/api/favoritos/{self.favorito.id_favorito}/'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class FavoritoDetalleTestCase(APITestCase):
    """
    RF12 - Ver detalle de favorito
    Casos adicionales para información detallada de favoritos
    """
    
    def setUp(self):
        """Configuración inicial"""
        self.client = APIClient()
        
        # Crear usuario
        self.usuario = Usuario.objects.create_user(
            email='detalle@test.com',
            nombre='Usuario',
            apellido='Test',
            password='Test123!'
        )
        self.token = Token.objects.create(user=self.usuario)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Crear producto con detalles
        categoria = Categoria.objects.create(
            nombre='Electrónica',
            slug=slugify('Electrónica')
        )
        marca = Marca.objects.create(nombre='Samsung')
        
        self.producto = Producto.objects.create(
            nombre='Samsung Galaxy S21',
            descripcion='Smartphone premium',
            precio=Decimal('2500000.00'),
            stock=10,
            sku='SGAL-S21-002',
            id_categoria=categoria,
            id_marca=marca,
            en_oferta=True
        )
        
        # Agregar a favoritos
        self.favorito = Favorito.objects.create(
            usuario=self.usuario,
            producto=self.producto
        )
    
    def test_favorito_incluye_detalles_producto(self):
        """
        CP50: Verificar que favorito incluye detalles del producto
        Entrada: GET favoritos
        Salida Esperada: Datos completos del producto (nombre, precio, etc.)
        """
        response = self.client.get('/api/favoritos/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        
        # Verificar estructura de datos
        favorito_data = response.data[0]
        
        # Debe incluir información del producto
        if isinstance(favorito_data, dict) and 'producto' in favorito_data:
            producto_data = favorito_data['producto']
            self.assertEqual(producto_data['nombre'], self.producto.nombre)
            self.assertIn('precio', producto_data)
            self.assertIn('descripcion', producto_data)

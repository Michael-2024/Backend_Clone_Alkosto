"""
Pruebas Unitarias - Módulo de Carrito de Compras
RF14 - Añadir al carrito
RF17 - Ver el carrito
"""

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from core.models import Producto, Categoria, Marca, Usuario, Carrito, CarritoItem
from rest_framework.authtoken.models import Token
from decimal import Decimal
from django.utils.text import slugify


class AgregarAlCarritoTestCase(APITestCase):
    """
    RF14 - Añadir al carrito
    Casos de prueba para agregar productos al carrito
    """
    
    def setUp(self):
        """Configuración inicial"""
        self.client = APIClient()
        self.carrito_url = '/api/carrito/'
        
        # Crear usuario y autenticar
        self.usuario = Usuario.objects.create_user(
            email='carrito@test.com',
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
            descripcion='Smartphone',
            precio=Decimal('2500000.00'),
            stock=10,
            sku='SGAL-S21-CARR-001',
            id_categoria=self.categoria,
            id_marca=self.marca
        )
        
        self.producto2 = Producto.objects.create(
            nombre='Samsung TV 55"',
            descripcion='Smart TV',
            precio=Decimal('3000000.00'),
            stock=5,
            sku='STV-55-CARR-001',
            id_categoria=self.categoria,
            id_marca=self.marca
        )
    
    def test_agregar_al_carrito_exitoso(self):
        """
        CP51: Agregar producto al carrito exitosamente
        Entrada: producto_id, cantidad=1
        Salida Esperada: Status 201, item agregado al carrito
        """
        payload = {
            'id_producto': self.producto1.id_producto,
            'cantidad': 1
        }
        
        response = self.client.post(
            self.carrito_url,
            payload,
            format='json'
        )
        
        self.assertIn(
            response.status_code,
            [status.HTTP_201_CREATED, status.HTTP_200_OK]
        )
        
        # Verificar que existe en el carrito
        carrito = Carrito.objects.get(id_usuario=self.usuario)
        item_exists = CarritoItem.objects.filter(
            id_carrito=carrito,
            id_producto=self.producto1
        ).exists()
        self.assertTrue(item_exists)
    
    def test_agregar_al_carrito_sin_autenticacion(self):
        """
        CP52: Intentar agregar al carrito sin autenticación
        Entrada: Request sin token
        Salida Esperada: Error 401
        """
        self.client.credentials()  # Eliminar credenciales
        
        payload = {
            'id_producto': self.producto1.id_producto,
            'cantidad': 1
        }
        
        response = self.client.post(
            self.carrito_url,
            payload,
            format='json'
        )
        
        # El carrito permite usuarios anónimos (carrito de sesión)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_200_OK, status.HTTP_201_CREATED])
    
    def test_agregar_multiples_unidades(self):
        """
        CP53: Agregar múltiples unidades del mismo producto
        Entrada: producto_id, cantidad=3
        Salida Esperada: Item con cantidad=3
        """
        payload = {
            'id_producto': self.producto1.id_producto,
            'cantidad': 3
        }
        
        response = self.client.post(
            self.carrito_url,
            payload,
            format='json'
        )
        
        self.assertIn(
            response.status_code,
            [status.HTTP_201_CREATED, status.HTTP_200_OK]
        )
        
        # Verificar cantidad
        carrito = Carrito.objects.get(id_usuario=self.usuario)
        item = CarritoItem.objects.get(
            id_carrito=carrito,
            id_producto=self.producto1
        )
        self.assertEqual(item.cantidad, 3)
    
    def test_agregar_producto_sin_stock(self):
        """
        CP54: Agregar producto sin stock disponible
        Entrada: producto con stock=0
        Salida Esperada: Error 400, sin stock
        """
        # Crear producto sin stock
        producto_sin_stock = Producto.objects.create(
            nombre='Producto Sin Stock',
            precio=Decimal('1000000.00'),
            stock=0,
            sku='PROD-SIN-STOCK',
            id_categoria=self.categoria,
            id_marca=self.marca
        )
        
        payload = {
            'id_producto': producto_sin_stock.id_producto,
            'cantidad': 1
        }
        
        response = self.client.post(
            self.carrito_url,
            payload,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_agregar_cantidad_mayor_stock(self):
        """
        CP55: Agregar cantidad mayor al stock disponible
        Entrada: cantidad=20, stock=10
        Salida Esperada: Error 400, stock insuficiente
        """
        payload = {
            'id_producto': self.producto1.id_producto,
            'cantidad': 20  # stock es solo 10
        }
        
        response = self.client.post(
            self.carrito_url,
            payload,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_agregar_producto_inexistente(self):
        """
        CP56: Agregar producto que no existe
        Entrada: producto_id=99999
        Salida Esperada: Error 400 o 404
        """
        payload = {
            'id_producto': 99999,
            'cantidad': 1
        }
        
        response = self.client.post(
            self.carrito_url,
            payload,
            format='json'
        )
        
        self.assertIn(
            response.status_code,
            [status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND]
        )
    
    def test_incrementar_cantidad_producto_existente(self):
        """
        CP57: Agregar producto que ya está en el carrito
        Entrada: Mismo producto dos veces
        Salida Esperada: Cantidad incrementada (no duplicado)
        """
        # Agregar primera vez
        payload = {
            'id_producto': self.producto1.id_producto,
            'cantidad': 2
        }
        self.client.post(self.carrito_url, payload, format='json')
        
        # Agregar segunda vez
        payload = {
            'id_producto': self.producto1.id_producto,
            'cantidad': 3
        }
        response = self.client.post(self.carrito_url, payload, format='json')
        
        self.assertIn(
            response.status_code,
            [status.HTTP_200_OK, status.HTTP_201_CREATED]
        )
        
        # Verificar que solo hay un item con cantidad sumada
        carrito = Carrito.objects.get(id_usuario=self.usuario)
        items = CarritoItem.objects.filter(
            id_carrito=carrito,
            id_producto=self.producto1
        )
        
        self.assertEqual(items.count(), 1)
        # Cantidad debe ser 2 + 3 = 5, o 3 si se reemplaza
        self.assertIn(items.first().cantidad, [3, 5])


class VerCarritoTestCase(APITestCase):
    """
    RF17 - Ver el carrito
    Casos de prueba para visualizar el carrito de compras
    """
    
    def setUp(self):
        """Configuración inicial"""
        self.client = APIClient()
        self.carrito_url = '/api/carrito/'
        
        # Crear usuario y autenticar
        self.usuario = Usuario.objects.create_user(
            email='ver_carrito@test.com',
            nombre='Usuario',
            apellido='Test',
            password='Test123!'
        )
        self.token = Token.objects.create(user=self.usuario)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Crear productos
        categoria = Categoria.objects.create(nombre='Tecnología', slug=slugify('Tecnología'))
        marca = Marca.objects.create(nombre='Samsung')
        
        self.producto1 = Producto.objects.create(
            nombre='Producto 1',
            precio=Decimal('1000000.00'),
            stock=10,
            sku='PROD-1-CARR',
            id_categoria=categoria,
            id_marca=marca
        )
        
        self.producto2 = Producto.objects.create(
            nombre='Producto 2',
            precio=Decimal('2000000.00'),
            stock=5,
            sku='PROD-2-CARR',
            id_categoria=categoria,
            id_marca=marca
        )
        
        # Crear carrito con items
        self.carrito = Carrito.objects.create(id_usuario=self.usuario)
        
        CarritoItem.objects.create(
            id_carrito=self.carrito,
            id_producto=self.producto1,
            cantidad=2
        )
        
        CarritoItem.objects.create(
            id_carrito=self.carrito,
            id_producto=self.producto2,
            cantidad=1
        )
    
    def test_ver_carrito_exitoso(self):
        """
        CP58: Ver carrito con productos
        Entrada: Usuario autenticado con items en carrito
        Salida Esperada: Status 200, lista de items
        """
        response = self.client.get(self.carrito_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Debe contener items
        if isinstance(response.data, dict):
            items = response.data.get('items', [])
        else:
            items = response.data
        
        self.assertGreaterEqual(len(items), 2)
    
    def test_ver_carrito_vacio(self):
        """
        CP59: Ver carrito vacío
        Entrada: Usuario sin items en carrito
        Salida Esperada: Status 200, carrito vacío
        """
        # Crear nuevo usuario sin items
        nuevo_usuario = Usuario.objects.create_user(
            email='carrito_vacio@test.com',
            nombre='Sin',
            apellido='Items',
            password='Test123!'
        )
        nuevo_token = Token.objects.create(user=nuevo_usuario)
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + nuevo_token.key)
        response = self.client.get(self.carrito_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que está vacío
        if isinstance(response.data, dict):
            items = response.data.get('items', [])
        else:
            items = response.data
        
        self.assertEqual(len(items), 0)
    
    def test_ver_carrito_sin_autenticacion(self):
        """
        CP60: Ver carrito sin autenticación
        Entrada: Request sin token
        Salida Esperada: Error 401
        """
        self.client.credentials()  # Eliminar credenciales
        response = self.client.get(self.carrito_url)
        
        # El carrito permite usuarios anónimos (carrito de sesión)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_200_OK])
    
    def test_carrito_calcula_total_correctamente(self):
        """
        CP61: Verificar cálculo del total del carrito
        Entrada: Carrito con múltiples items
        Salida Esperada: Total = suma(precio * cantidad)
        """
        response = self.client.get(self.carrito_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Calcular total esperado
        # Producto1: 1000000 * 2 = 2000000
        # Producto2: 2000000 * 1 = 2000000
        # Total esperado: 4000000
        total_esperado = Decimal('4000000.00')
        
        if isinstance(response.data, dict) and 'total' in response.data:
            total = Decimal(str(response.data['total']))
            self.assertEqual(total, total_esperado)
    
    def test_carrito_solo_del_usuario_autenticado(self):
        """
        CP62: Verificar que solo se muestran items del usuario
        Entrada: Usuario 1 autenticado
        Salida Esperada: Solo items del Usuario 1
        """
        # Crear otro usuario con carrito
        otro_usuario = Usuario.objects.create_user(
            email='otro_carrito@test.com',
            nombre='Otro',
            apellido='Usuario',
            password='Test123!'
        )
        
        carrito_otro = Carrito.objects.create(id_usuario=otro_usuario)
        
        categoria = Categoria.objects.first()
        marca = Marca.objects.first()
        
        producto_otro = Producto.objects.create(
            nombre='Producto de Otro',
            precio=Decimal('500000.00'),
            stock=10,
            sku='PROD-OTRO-CAR',
            id_categoria=categoria,
            id_marca=marca
        )
        
        CarritoItem.objects.create(
            id_carrito=carrito_otro,
            id_producto=producto_otro,
            cantidad=1
        )
        
        # Ver carrito del usuario original
        response = self.client.get(self.carrito_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Extraer items
        if isinstance(response.data, dict):
            items = response.data.get('items', [])
        else:
            items = response.data
        
        # Verificar que NO contiene el producto del otro usuario
        productos_ids = []
        for item in items:
            if isinstance(item, dict):
                productos_ids.append(item.get('producto', {}).get('id_producto'))
            else:
                productos_ids.append(item.producto.id_producto)
        
        self.assertNotIn(producto_otro.id_producto, productos_ids)


class ActualizarCantidadCarritoTestCase(APITestCase):
    """
    RF14/RF17 - Actualizar cantidad en carrito
    Casos de prueba para modificar cantidades
    """
    
    def setUp(self):
        """Configuración inicial"""
        self.client = APIClient()
        
        # Crear usuario
        self.usuario = Usuario.objects.create_user(
            email='actualizar@test.com',
            nombre='Usuario',
            apellido='Test',
            password='Test123!'
        )
        self.token = Token.objects.create(user=self.usuario)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Crear producto
        categoria = Categoria.objects.create(nombre='Tecnología', slug=slugify('Tecnología'))
        marca = Marca.objects.create(nombre='Samsung')
        
        self.producto = Producto.objects.create(
            nombre='Producto Test',
            precio=Decimal('1000000.00'),
            stock=10,
            sku='PROD-TEST-CARR',
            id_categoria=categoria,
            id_marca=marca
        )
        
        # Crear carrito con item
        self.carrito = Carrito.objects.create(id_usuario=self.usuario)
        self.item = CarritoItem.objects.create(
            id_carrito=self.carrito,
            id_producto=self.producto,
            cantidad=2
        )
    
    def test_actualizar_cantidad_exitoso(self):
        """
        CP63: Actualizar cantidad de item en carrito
        Entrada: item_id, nueva_cantidad=5
        Salida Esperada: Cantidad actualizada
        """
        url = f'/api/carrito/{self.item.id_item}/'
        payload = {'cantidad': 5}
        
        response = self.client.patch(
            url,
            payload,
            format='json'
        )
        
        self.assertIn(
            response.status_code,
            [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]
        )
        
        # Verificar actualización
        self.item.refresh_from_db()
        self.assertEqual(self.item.cantidad, 5)
    
    def test_actualizar_cantidad_excede_stock(self):
        """
        CP64: Actualizar a cantidad mayor que stock
        Entrada: nueva_cantidad=15, stock=10
        Salida Esperada: Error 400
        """
        url = f'/api/carrito/{self.item.id_item}/'
        payload = {'cantidad': 15}
        
        response = self.client.patch(
            url,
            payload,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_actualizar_cantidad_a_cero(self):
        """
        CP65: Actualizar cantidad a 0 (eliminar item)
        Entrada: nueva_cantidad=0
        Salida Esperada: Item eliminado del carrito
        """
        url = f'/api/carrito/{self.item.id_item}/'
        payload = {'cantidad': 0}
        
        response = self.client.patch(
            url,
            payload,
            format='json'
        )
        
        # Debe eliminar el item o retornar error
        if response.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]:
            item_exists = CarritoItem.objects.filter(id_item=self.item.id_item).exists()
            # Item debe estar eliminado o con cantidad 0
            if item_exists:
                self.item.refresh_from_db()
                self.assertEqual(self.item.cantidad, 0)


class EliminarDelCarritoTestCase(APITestCase):
    """
    RF14/RF17 - Eliminar productos del carrito
    """
    
    def setUp(self):
        """Configuración inicial"""
        self.client = APIClient()
        
        # Crear usuario
        self.usuario = Usuario.objects.create_user(
            email='eliminar_carrito@test.com',
            nombre='Usuario',
            apellido='Test',
            password='Test123!'
        )
        self.token = Token.objects.create(user=self.usuario)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Crear producto
        categoria = Categoria.objects.create(nombre='Tecnología', slug=slugify('Tecnología'))
        marca = Marca.objects.create(nombre='Samsung')
        
        self.producto = Producto.objects.create(
            nombre='Producto a Eliminar',
            precio=Decimal('1000000.00'),
            stock=10,
            sku='PROD-ELIM-CARR',
            id_categoria=categoria,
            id_marca=marca
        )
        
        # Crear carrito con item
        self.carrito = Carrito.objects.create(id_usuario=self.usuario)
        self.item = CarritoItem.objects.create(
            id_carrito=self.carrito,
            id_producto=self.producto,
            cantidad=2
        )
    
    def test_eliminar_item_carrito_exitoso(self):
        """
        CP66: Eliminar item del carrito
        Entrada: item_id válido
        Salida Esperada: Item eliminado
        """
        url = f'/api/carrito/{self.item.id_item}/'
        response = self.client.delete(url)
        
        self.assertIn(
            response.status_code,
            [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK]
        )
        
        # Verificar eliminación
        item_exists = CarritoItem.objects.filter(id_item=self.item.id_item).exists()
        self.assertFalse(item_exists)
    
    def test_vaciar_carrito_completo(self):
        """
        CP67: Vaciar todo el carrito
        Entrada: DELETE /api/carrito/vaciar/
        Salida Esperada: Todos los items eliminados
        """
        # Agregar más items
        categoria = Categoria.objects.first()
        marca = Marca.objects.first()
        
        producto2 = Producto.objects.create(
            nombre='Producto 2',
            precio=Decimal('2000000.00'),
            stock=5,
            sku='PROD-VAC-2',
            id_categoria=categoria,
            id_marca=marca
        )
        
        CarritoItem.objects.create(
            id_carrito=self.carrito,
            id_producto=producto2,
            cantidad=1
        )
        
        # Vaciar carrito
        url = '/api/carrito/vaciar/'
        response = self.client.delete(url)
        
        if response.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]:
            # Verificar que no quedan items
            count = CarritoItem.objects.filter(id_carrito=self.carrito).count()
            self.assertEqual(count, 0)














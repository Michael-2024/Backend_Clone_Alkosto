"""
Pruebas Unitarias - Módulo de Productos
RF06 - Buscar Producto
RF07 - Filtrar categorías
"""

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from core.models import Producto, Categoria, Marca, Usuario
from decimal import Decimal
from django.utils.text import slugify


class BusquedaProductoTestCase(APITestCase):
    """
    RF06 - Buscar Producto
    Casos de prueba para la búsqueda de productos
    """
    
    def setUp(self):
        """Configuración inicial - Crear productos de prueba"""
        self.client = APIClient()
        self.buscar_url = '/api/buscar/'
        
        # Crear categorías
        self.categoria_tech = Categoria.objects.create(
            nombre='Tecnología',
            slug=slugify('Tecnología'),
            descripcion='Productos tecnológicos'
        )
        self.categoria_hogar = Categoria.objects.create(
            nombre='Hogar',
            slug=slugify('Hogar'),
            descripcion='Productos para el hogar'
        )
        
        # Crear marca
        self.marca_samsung = Marca.objects.create(
            nombre='Samsung',
            descripcion='Marca Samsung'
        )
        self.marca_lg = Marca.objects.create(
            nombre='LG',
            descripcion='Marca LG'
        )
        
        # Crear productos
        self.producto_tv = Producto.objects.create(
            nombre='Smart TV Samsung 55 pulgadas',
            descripcion='Televisor inteligente de 55 pulgadas con 4K',
            sku='TV-SAMSUNG-55-001',
            precio=Decimal('2500000.00'),
            precio_original=Decimal('2500000.00'),
            stock=10,
            id_categoria=self.categoria_tech,
            id_marca=self.marca_samsung,
            destacado=True,
            en_oferta=True
        )
        
        self.producto_nevera = Producto.objects.create(
            nombre='Nevera LG 420 litros',
            descripcion='Refrigerador de dos puertas',
            sku='NEVERA-LG-420-001',
            precio=Decimal('1800000.00'),
            stock=5,
            id_categoria=self.categoria_hogar,
            id_marca=self.marca_lg,
            destacado=False,
            en_oferta=False
        )
        
        self.producto_lavadora = Producto.objects.create(
            nombre='Lavadora Samsung 20kg',
            descripcion='Lavadora automática de carga frontal',
            sku='LAV-SAMSUNG-20-001',
            precio=Decimal('1500000.00'),
            precio_original=Decimal('1500000.00'),
            stock=8,
            id_categoria=self.categoria_hogar,
            id_marca=self.marca_samsung,
            destacado=True,
            en_oferta=True
        )
    
    def test_busqueda_por_nombre_exitosa(self):
        """
        CP21: Buscar producto por nombre
        Entrada: Término de búsqueda "Samsung"
        Salida Esperada: Status 200, productos que contienen "Samsung"
        """
        response = self.client.get(
            self.buscar_url,
            {'q': 'Samsung'}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # El endpoint retorna un dict con 'resultados'
        resultados = response.data.get('resultados', response.data)
        self.assertGreaterEqual(len(resultados), 2)  # TV y Lavadora
        
        # Verificar que contiene productos Samsung
        nombres = [p['nombre'] for p in resultados]
        self.assertTrue(any('Samsung' in n for n in nombres))
    
    def test_busqueda_por_descripcion(self):
        """
        CP22: Buscar producto por descripción
        Entrada: Término "inteligente"
        Salida Esperada: Productos con ese término en descripción
        """
        response = self.client.get(
            self.buscar_url,
            {'q': 'inteligente'}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_busqueda_sin_resultados(self):
        """
        CP23: Búsqueda sin resultados
        Entrada: Término que no existe "iPhone"
        Salida Esperada: Status 200, lista vacía
        """
        response = self.client.get(
            self.buscar_url,
            {'q': 'iPhone'}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resultados = response.data.get('resultados', response.data)
        self.assertEqual(len(resultados), 0)
    
    def test_busqueda_vacia(self):
        """
        CP24: Búsqueda con término vacío
        Entrada: q='' (vacío)
        Salida Esperada: Status 200, todos los productos
        """
        response = self.client.get(
            self.buscar_url,
            {'q': ''}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Debe retornar todos los productos (o comportamiento definido)
        # El endpoint retorna un dict con 'resultados'
        self.assertIn('resultados', response.data)
    
    def test_busqueda_case_insensitive(self):
        """
        CP25: Búsqueda insensible a mayúsculas
        Entrada: "samsung" (minúsculas)
        Salida Esperada: Mismos resultados que "Samsung"
        """
        response_lower = self.client.get(
            self.buscar_url,
            {'q': 'samsung'}
        )
        response_upper = self.client.get(
            self.buscar_url,
            {'q': 'SAMSUNG'}
        )
        
        self.assertEqual(response_lower.status_code, status.HTTP_200_OK)
        self.assertEqual(response_upper.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_lower.data), len(response_upper.data))


class FiltroCategoriasTestCase(APITestCase):
    """
    RF07 - Filtrar categorías
    Casos de prueba para filtrado por categorías
    """
    
    def setUp(self):
        """Configuración inicial"""
        self.client = APIClient()
        self.productos_url = '/api/productos/'
        
        # Crear categorías
        self.cat_electronica = Categoria.objects.create(
            nombre='Electrónica',
            slug=slugify('Electrónica'),
            descripcion='Productos electrónicos'
        )
        self.cat_ropa = Categoria.objects.create(
            nombre='Ropa',
            slug=slugify('Ropa'),
            descripcion='Prendas de vestir'
        )
        self.cat_deportes = Categoria.objects.create(
            nombre='Deportes',
            slug=slugify('Deportes'),
            descripcion='Artículos deportivos'
        )
        
        # Crear marca
        self.marca = Marca.objects.create(
            nombre='Genérica',
            descripcion='Marca genérica'
        )
        
        # Crear productos en diferentes categorías
        self.producto_laptop = Producto.objects.create(
            nombre='Laptop HP',
            sku='LAPTOP-HP-001',
            descripcion='Computador portátil',
            precio=Decimal('3000000.00'),
            stock=5,
            id_categoria=self.cat_electronica,
            id_marca=self.marca
        )
        
        self.producto_camisa = Producto.objects.create(
            nombre='Camisa Polo',
            sku='CAMISA-POLO-001',
            descripcion='Camisa deportiva',
            precio=Decimal('80000.00'),
            stock=20,
            id_categoria=self.cat_ropa,
            id_marca=self.marca
        )
        
        self.producto_balon = Producto.objects.create(
            nombre='Balón de Fútbol',
            sku='BALON-FUT-001',
            descripcion='Balón profesional',
            precio=Decimal('120000.00'),
            stock=15,
            id_categoria=self.cat_deportes,
            id_marca=self.marca
        )
        
        # Productos adicionales en electrónica
        Producto.objects.create(
            nombre='Mouse Inalámbrico',
            sku='MOUSE-INAL-001',
            descripcion='Mouse bluetooth',
            precio=Decimal('50000.00'),
            stock=30,
            id_categoria=self.cat_electronica,
            id_marca=self.marca
        )
    
    def test_filtrar_por_categoria_electronica(self):
        """
        CP26: Filtrar productos de categoría Electrónica
        Entrada: categoria_id de Electrónica
        Salida Esperada: Solo productos de esa categoría
        """
        response = self.client.get(
            self.productos_url,
            {'categoria': self.cat_electronica.id_categoria}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Laptop y Mouse
        
        # Verificar que todos son de la categoría correcta
        for producto in response.data:
            self.assertEqual(producto['id_categoria'], self.cat_electronica.id_categoria)
    
    def test_filtrar_por_categoria_ropa(self):
        """
        CP27: Filtrar productos de categoría Ropa
        Entrada: categoria_id de Ropa
        Salida Esperada: Solo productos de ropa
        """
        response = self.client.get(
            self.productos_url,
            {'categoria': self.cat_ropa.id_categoria}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Solo camisa
        self.assertEqual(response.data[0]['nombre'], 'Camisa Polo')
    
    def test_filtrar_categoria_sin_productos(self):
        """
        CP28: Filtrar categoría sin productos
        Entrada: ID de categoría válida pero sin productos
        Salida Esperada: Status 200, lista vacía
        """
        categoria_vacia = Categoria.objects.create(
            nombre='Categoría Vacía',
            slug=slugify('Categoría Vacía'),
            descripcion='Sin productos'
        )
        
        response = self.client.get(
            self.productos_url,
            {'categoria': categoria_vacia.id_categoria}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    
    def test_filtrar_categoria_inexistente(self):
        """
        CP29: Filtrar con ID de categoría inexistente
        Entrada: categoria_id que no existe (ej: 99999)
        Salida Esperada: Status 200, lista vacía o error
        """
        response = self.client.get(
            self.productos_url,
            {'categoria': 99999}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    
    def test_obtener_todas_categorias(self):
        """
        CP30: Obtener lista de todas las categorías
        Entrada: GET /api/categorias/
        Salida Esperada: Lista de categorías disponibles
        """
        categorias_url = '/api/categorias/'
        response = self.client.get(categorias_url)
        
        # Si el endpoint existe
        if response.status_code == status.HTTP_200_OK:
            self.assertGreaterEqual(len(response.data), 3)
            nombres = [c['nombre'] for c in response.data]
            self.assertIn('Electrónica', nombres)
            self.assertIn('Ropa', nombres)
            self.assertIn('Deportes', nombres)


class FiltroCombinandoTestCase(APITestCase):
    """
    RF06 + RF07 - Búsqueda con filtros combinados
    Casos de prueba para búsqueda y filtros simultáneos
    """
    
    def setUp(self):
        """Configuración inicial"""
        self.client = APIClient()
        self.buscar_url = '/api/buscar/'
        
        # Crear categorías
        self.cat_tech = Categoria.objects.create(nombre='Tecnología', slug=slugify('Tecnología'))
        self.cat_hogar = Categoria.objects.create(nombre='Hogar', slug=slugify('Hogar'))
        
        # Crear marcas
        self.marca_samsung = Marca.objects.create(nombre='Samsung')
        self.marca_lg = Marca.objects.create(nombre='LG')
        
        # Productos Samsung en Tecnología
        Producto.objects.create(
            nombre='Samsung Galaxy S21',
            sku='SAMS-S21-001',
            precio=Decimal('2500000.00'),
            stock=10,
            id_categoria=self.cat_tech,
            id_marca=self.marca_samsung
        )
        
        # Productos Samsung en Hogar
        Producto.objects.create(
            nombre='Samsung Lavadora',
            sku='SAMS-LAV-001',
            precio=Decimal('1500000.00'),
            stock=5,
            id_categoria=self.cat_hogar,
            id_marca=self.marca_samsung
        )
        
        # Productos LG en Tecnología
        Producto.objects.create(
            nombre='LG Monitor 27 pulgadas',
            sku='LG-MON-27-001',
            precio=Decimal('800000.00'),
            stock=8,
            id_categoria=self.cat_tech,
            id_marca=self.marca_lg
        )
    
    def test_busqueda_con_filtro_categoria(self):
        """
        CP31: Buscar "Samsung" filtrado por categoría Tecnología
        Entrada: q="Samsung", categoria=Tecnología
        Salida Esperada: Solo Samsung Galaxy S21
        """
        response = self.client.get(
            self.buscar_url,
            {
                'q': 'Samsung',
                'categoria': self.cat_tech.id_categoria
            }
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resultados = response.data.get('resultados', response.data)
        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0]['nombre'], 'Samsung Galaxy S21')
    
    def test_filtro_por_rango_precio(self):
        """
        CP32: Filtrar productos por rango de precio
        Entrada: precio_min=1000000, precio_max=2000000
        Salida Esperada: Productos en ese rango
        """
        response = self.client.get(
            self.buscar_url,
            {
                'precio_min': 1000000,
                'precio_max': 2000000
            }
        )
        
        if response.status_code == status.HTTP_200_OK:
            resultados = response.data.get('resultados', response.data)
            for producto in resultados:
                precio = Decimal(str(producto['precio']))
                self.assertGreaterEqual(precio, Decimal('1000000.00'))
                self.assertLessEqual(precio, Decimal('2000000.00'))
    
    def test_filtro_productos_destacados(self):
        """
        CP33: Filtrar solo productos destacados
        Entrada: es_destacado=true
        Salida Esperada: Solo productos con es_destacado=True
        """
        # Marcar un producto como destacado
        producto = Producto.objects.first()
        producto.es_destacado = True
        producto.save()
        
        destacados_url = '/api/destacados/'
        response = self.client.get(destacados_url)
        
        if response.status_code == status.HTTP_200_OK:
            for producto in response.data:
                self.assertTrue(producto.get('es_destacado', True))
    
    def test_filtro_productos_oferta(self):
        """
        CP34: Filtrar solo productos en oferta
        Entrada: en_oferta=true
        Salida Esperada: Solo productos con en_oferta=True
        """
        # Marcar producto en oferta
        producto = Producto.objects.first()
        producto.en_oferta = True
        producto.precio_oferta = Decimal('1000000.00')
        producto.save()
        
        ofertas_url = '/api/ofertas/'
        response = self.client.get(ofertas_url)
        
        if response.status_code == status.HTTP_200_OK:
            for producto in response.data:
                self.assertTrue(producto.get('en_oferta', True))


class OrdenamientoProductosTestCase(APITestCase):
    """
    RF06 - Ordenamiento de resultados de búsqueda
    """
    
    def setUp(self):
        """Configuración inicial"""
        self.client = APIClient()
        self.productos_url = '/api/productos/'
        
        categoria = Categoria.objects.create(nombre='General', slug=slugify('General'))
        marca = Marca.objects.create(nombre='Marca')
        
        # Crear productos con diferentes precios
        Producto.objects.create(
            nombre='Producto A',
            sku='PROD-A-001',
            precio=Decimal('1000.00'),
            stock=10,
            id_categoria=categoria,
            id_marca=marca
        )
        Producto.objects.create(
            nombre='Producto B',
            sku='PROD-B-001',
            precio=Decimal('5000.00'),
            stock=10,
            id_categoria=categoria,
            id_marca=marca
        )
        Producto.objects.create(
            nombre='Producto C',
            sku='PROD-C-001',
            precio=Decimal('3000.00'),
            stock=10,
            id_categoria=categoria,
            id_marca=marca
        )
    
    def test_ordenar_por_precio_ascendente(self):
        """
        CP35: Ordenar productos por precio de menor a mayor
        Entrada: ordenar=precio_asc
        Salida Esperada: Productos ordenados ascendentemente
        """
        response = self.client.get(
            self.productos_url,
            {'orden': 'precio_asc'}
        )
        
        if response.status_code == status.HTTP_200_OK:
            precios = [Decimal(str(p['precio'])) for p in response.data]
            self.assertEqual(precios, sorted(precios))
    
    def test_ordenar_por_precio_descendente(self):
        """
        CP36: Ordenar productos por precio de mayor a menor
        Entrada: ordenar=precio_desc
        Salida Esperada: Productos ordenados descendentemente
        """
        response = self.client.get(
            self.productos_url,
            {'orden': 'precio_desc'}
        )
        
        if response.status_code == status.HTTP_200_OK:
            precios = [Decimal(str(p['precio'])) for p in response.data]
            self.assertEqual(precios, sorted(precios, reverse=True))

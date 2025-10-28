"""
Pruebas de Rendimiento - Backend Clone Alkosto
==============================================

Este módulo contiene pruebas de rendimiento para evaluar:
- Tiempo de respuesta de endpoints críticos
- Throughput (peticiones por segundo)  
- Eficiencia de consultas a base de datos
- Rendimiento bajo carga concurrente
- Uso de memoria y CPU

Autor: Sistema de Pruebas Backend Clone Alkosto
Fecha: 24 de octubre de 2025
"""

import time
import statistics
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.test import TestCase, TransactionTestCase
from django.test.utils import override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db import connection
from django.test.client import Client
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
import json
import psutil
import os
from core.models import Usuario, Producto, Categoria, Marca, Favorito, Carrito, CarritoItem

Usuario = get_user_model()


class PerformanceTestMixin:
    """Mixin con utilidades para medición de rendimiento"""
    
    def measure_time(self, func, *args, **kwargs):
        """Mide el tiempo de ejecución de una función"""
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        return result, execution_time
    
    def measure_memory_usage(self):
        """Mide el uso actual de memoria"""
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024  # MB
    
    def run_multiple_times(self, func, iterations=10, *args, **kwargs):
        """Ejecuta una función múltiples veces y retorna estadísticas"""
        times = []
        results = []
        
        for i in range(iterations):
            result, exec_time = self.measure_time(func, *args, **kwargs)
            times.append(exec_time)
            results.append(result)
        
        stats = {
            'min_time': min(times),
            'max_time': max(times),
            'avg_time': statistics.mean(times),
            'median_time': statistics.median(times),
            'std_dev': statistics.stdev(times) if len(times) > 1 else 0,
            'total_time': sum(times),
            'iterations': iterations,
            'times': times,
            'results': results
        }
        
        return stats
    
    def concurrent_requests(self, func, num_threads=10, requests_per_thread=5):
        """Ejecuta peticiones concurrentes"""
        results = []
        times = []
        errors = []
        
        def worker():
            thread_results = []
            thread_times = []
            thread_errors = []
            
            for _ in range(requests_per_thread):
                try:
                    result, exec_time = self.measure_time(func)
                    thread_results.append(result)
                    thread_times.append(exec_time)
                except Exception as e:
                    thread_errors.append(str(e))
            
            return thread_results, thread_times, thread_errors
        
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(worker) for _ in range(num_threads)]
            
            for future in as_completed(futures):
                thread_results, thread_times, thread_errors = future.result()
                results.extend(thread_results)
                times.extend(thread_times)
                errors.extend(thread_errors)
        
        total_requests = num_threads * requests_per_thread
        successful_requests = len(results)
        
        stats = {
            'total_requests': total_requests,
            'successful_requests': successful_requests,
            'failed_requests': len(errors),
            'success_rate': (successful_requests / total_requests) * 100,
            'avg_response_time': statistics.mean(times) if times else 0,
            'min_response_time': min(times) if times else 0,
            'max_response_time': max(times) if times else 0,
            'requests_per_second': successful_requests / sum(times) if times else 0,
            'errors': errors,
            'times': times
        }
        
        return stats


class AuthenticationPerformanceTests(TestCase, PerformanceTestMixin):
    """Pruebas de rendimiento para autenticación"""
    
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'performance@test.com',
            'nombre': 'Performance',
            'apellido': 'Test',
            'password': 'TestPassword123!',
            'password_confirm': 'TestPassword123!'
        }
    
    def test_registro_performance(self):
        """Mide el rendimiento del endpoint de registro"""
        print("\n🚀 PRUEBA DE RENDIMIENTO: Registro de Usuario")
        
        def registro_request():
            # Usar email único para cada request
            unique_data = self.user_data.copy()
            unique_data['email'] = f"user_{int(time.time() * 1000000)}@test.com"
            
            response = self.client.post(
                reverse('registro'),
                data=json.dumps(unique_data),
                content_type='application/json'
            )
            return response.status_code == 201
        
        # Prueba de rendimiento individual
        stats = self.run_multiple_times(registro_request, iterations=20)
        
        print(f"📊 Estadísticas de Registro:")
        print(f"   • Tiempo promedio: {stats['avg_time']:.4f}s")
        print(f"   • Tiempo mínimo: {stats['min_time']:.4f}s") 
        print(f"   • Tiempo máximo: {stats['max_time']:.4f}s")
        print(f"   • Desviación estándar: {stats['std_dev']:.4f}s")
        print(f"   • Total de registros: {stats['iterations']}")
        
        # Verificaciones de rendimiento (ajustadas para entorno de desarrollo)
        self.assertLess(stats['avg_time'], 2.0, "Tiempo promedio de registro debe ser < 2s")
        self.assertLess(stats['max_time'], 3.0, "Tiempo máximo de registro debe ser < 3s")
        self.assertTrue(all(r for r in stats['results']), "Todos los registros deben ser exitosos")
    
    def test_login_performance(self):
        """Mide el rendimiento del endpoint de login"""
        print("\n🔐 PRUEBA DE RENDIMIENTO: Login de Usuario")
        
        # Crear usuario para login
        Usuario.objects.create_user(
            email='login_test@test.com',
            nombre='Login',
            apellido='Test',
            password='TestPassword123!'
        )
        
        def login_request():
            response = self.client.post(
                reverse('login'),
                data=json.dumps({
                    'email': 'login_test@test.com',
                    'password': 'TestPassword123!'
                }),
                content_type='application/json'
            )
            return response.status_code == 200
        
        stats = self.run_multiple_times(login_request, iterations=50)
        
        print(f"📊 Estadísticas de Login:")
        print(f"   • Tiempo promedio: {stats['avg_time']:.4f}s")
        print(f"   • Tiempo mínimo: {stats['min_time']:.4f}s")
        print(f"   • Tiempo máximo: {stats['max_time']:.4f}s")
        print(f"   • Requests/segundo: {stats['iterations']/stats['total_time']:.2f}")
        
        # Verificaciones de rendimiento (ajustadas para entorno de desarrollo)
        self.assertLess(stats['avg_time'], 1.0, "Tiempo promedio de login debe ser < 1s")
        self.assertLess(stats['max_time'], 2.0, "Tiempo máximo de login debe ser < 2s")
    
    def test_concurrent_login_performance(self):
        """Prueba de login concurrente"""
        print("\n⚡ PRUEBA DE RENDIMIENTO: Login Concurrente")
        
        # Crear usuario para pruebas concurrentes
        Usuario.objects.create_user(
            email='concurrent@test.com',
            nombre='Concurrent',
            apellido='Test', 
            password='TestPassword123!'
        )
        
        def concurrent_login():
            client = APIClient()
            response = client.post(
                reverse('login'),
                data=json.dumps({
                    'email': 'concurrent@test.com',
                    'password': 'TestPassword123!'
                }),
                content_type='application/json'
            )
            return response.status_code == 200
        
        # 20 threads, 5 requests cada uno = 100 logins concurrentes
        stats = self.concurrent_requests(concurrent_login, num_threads=20, requests_per_thread=5)
        
        print(f"📊 Estadísticas de Login Concurrente:")
        print(f"   • Total de requests: {stats['total_requests']}")
        print(f"   • Requests exitosos: {stats['successful_requests']}")
        print(f"   • Tasa de éxito: {stats['success_rate']:.2f}%")
        print(f"   • Tiempo promedio: {stats['avg_response_time']:.4f}s")
        print(f"   • Requests/segundo: {stats['requests_per_second']:.2f}")
        
        # Verificaciones (ajustadas para entorno de desarrollo)
        self.assertGreaterEqual(stats['success_rate'], 95.0, "Tasa de éxito debe ser >= 95%")
        self.assertLess(stats['avg_response_time'], 2.0, "Tiempo promedio debe ser < 2s")


class ProductsPerformanceTests(TestCase, PerformanceTestMixin):
    """Pruebas de rendimiento para productos"""
    
    def setUp(self):
        self.client = APIClient()
        
        # Crear categorías y marcas
        self.categoria = Categoria.objects.create(nombre='Electrónicos', descripcion='Productos electrónicos')
        self.marca = Marca.objects.create(nombre='Samsung', descripcion='Marca Samsung')
        
        # Crear muchos productos para pruebas de rendimiento
        print("🔄 Creando productos de prueba...")
        productos = []
        for i in range(1000):  # 1000 productos para pruebas realistas
            productos.append(Producto(
                nombre=f'Producto {i}',
                descripcion=f'Descripción del producto {i} con palabras clave Samsung smartphone',
                precio=1000000 + (i * 10000),
                sku=f'SKU-{i:04d}',
                stock=50 + i,
                id_categoria=self.categoria,
                id_marca=self.marca,
                destacado=(i % 10 == 0),  # 10% destacados
                en_oferta=(i % 5 == 0)    # 20% en oferta
            ))
        
        Producto.objects.bulk_create(productos, batch_size=100)
        print(f"✅ Creados {len(productos)} productos de prueba")
    
    def test_busqueda_productos_performance(self):
        """Mide el rendimiento de búsqueda de productos"""
        print("\n🔍 PRUEBA DE RENDIMIENTO: Búsqueda de Productos")
        
        def busqueda_request():
            response = self.client.get(reverse('buscar_productos') + '?q=Samsung')
            return response.status_code == 200 and len(response.json()) > 0
        
        stats = self.run_multiple_times(busqueda_request, iterations=100)
        
        print(f"📊 Estadísticas de Búsqueda:")
        print(f"   • Tiempo promedio: {stats['avg_time']:.4f}s")
        print(f"   • Tiempo mínimo: {stats['min_time']:.4f}s")
        print(f"   • Tiempo máximo: {stats['max_time']:.4f}s")
        print(f"   • Búsquedas/segundo: {stats['iterations']/stats['total_time']:.2f}")
        
        self.assertLess(stats['avg_time'], 0.3, "Búsqueda debe ser < 0.3s en promedio")
        self.assertLess(stats['max_time'], 1.0, "Búsqueda máxima debe ser < 1s")
    
    def test_filtro_categoria_performance(self):
        """Mide el rendimiento del filtro por categoría"""
        print("\n📂 PRUEBA DE RENDIMIENTO: Filtro por Categoría")
        
        def filtro_request():
            response = self.client.get(reverse('productos_por_categoria', args=[self.categoria.nombre.lower()]))
            return response.status_code == 200
        
        stats = self.run_multiple_times(filtro_request, iterations=100)
        
        print(f"📊 Estadísticas de Filtro:")
        print(f"   • Tiempo promedio: {stats['avg_time']:.4f}s")
        print(f"   • Filtros/segundo: {stats['iterations']/stats['total_time']:.2f}")
        
        self.assertLess(stats['avg_time'], 0.2, "Filtro debe ser < 0.2s en promedio")
    
    def test_concurrent_search_performance(self):
        """Prueba de búsqueda concurrente"""
        print("\n⚡ PRUEBA DE RENDIMIENTO: Búsqueda Concurrente")
        
        search_terms = ['Samsung', 'Producto', 'smartphone', 'descripción']
        
        def concurrent_search():
            client = APIClient()
            term = search_terms[threading.current_thread().ident % len(search_terms)]
            response = client.get(reverse('buscar_productos') + f'?q={term}')
            return response.status_code == 200
        
        # 30 threads, 10 requests cada uno
        stats = self.concurrent_requests(concurrent_search, num_threads=30, requests_per_thread=10)
        
        print(f"📊 Estadísticas de Búsqueda Concurrente:")
        print(f"   • Total de búsquedas: {stats['total_requests']}")
        print(f"   • Tasa de éxito: {stats['success_rate']:.2f}%")
        print(f"   • Búsquedas/segundo: {stats['requests_per_second']:.2f}")
        print(f"   • Tiempo promedio: {stats['avg_response_time']:.4f}s")
        
        self.assertGreaterEqual(stats['success_rate'], 98.0, "Tasa de éxito >= 98%")
        self.assertGreater(stats['requests_per_second'], 50, "Debe procesar > 50 búsquedas/segundo")


class FavoritosPerformanceTests(TestCase, PerformanceTestMixin):
    """Pruebas de rendimiento para favoritos"""
    
    def setUp(self):
        self.client = APIClient()
        
        # Crear usuario y autenticar
        self.user = Usuario.objects.create_user(
            email='favoritos@test.com',
            nombre='Favoritos',
            apellido='Test',
            password='TestPassword123!'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        # Crear productos
        self.categoria = Categoria.objects.create(nombre='Test', descripcion='Test')
        self.marca = Marca.objects.create(nombre='Test', descripcion='Test')
        
        self.productos = []
        for i in range(100):
            producto = Producto.objects.create(
                nombre=f'Producto Favorito {i}',
                descripcion=f'Descripción {i}',
                precio=100000,
                sku=f'FAV-{i:03d}',
                stock=10,
                id_categoria=self.categoria,
                id_marca=self.marca
            )
            self.productos.append(producto)
    
    def test_agregar_favorito_performance(self):
        """Mide el rendimiento de agregar favoritos"""
        print("\n❤️ PRUEBA DE RENDIMIENTO: Agregar Favoritos")
        
        product_index = 0
        
        def agregar_favorito():
            nonlocal product_index
            producto = self.productos[product_index % len(self.productos)]
            product_index += 1
            
            response = self.client.post(
                reverse('favoritos-list'),
                data=json.dumps({'id_producto': producto.id}),
                content_type='application/json'
            )
            return response.status_code in [200, 201]
        
        stats = self.run_multiple_times(agregar_favorito, iterations=50)
        
        print(f"📊 Estadísticas de Agregar Favoritos:")
        print(f"   • Tiempo promedio: {stats['avg_time']:.4f}s")
        print(f"   • Favoritos/segundo: {stats['iterations']/stats['total_time']:.2f}")
        
        self.assertLess(stats['avg_time'], 0.5, "Agregar favorito debe ser < 0.5s")
    
    def test_listar_favoritos_performance(self):
        """Mide el rendimiento de listar favoritos"""
        print("\n📋 PRUEBA DE RENDIMIENTO: Listar Favoritos")
        
        # Crear algunos favoritos primero
        for i in range(20):
            Favorito.objects.create(
                id_usuario=self.user,
                id_producto=self.productos[i]
            )
        
        def listar_favoritos():
            response = self.client.get(reverse('favoritos-list'))
            return response.status_code == 200 and len(response.json()) == 20
        
        stats = self.run_multiple_times(listar_favoritos, iterations=100)
        
        print(f"📊 Estadísticas de Listar Favoritos:")
        print(f"   • Tiempo promedio: {stats['avg_time']:.4f}s")
        print(f"   • Consultas/segundo: {stats['iterations']/stats['total_time']:.2f}")
        
        self.assertLess(stats['avg_time'], 0.3, "Listar favoritos debe ser < 0.3s")


class CarritoPerformanceTests(TestCase, PerformanceTestMixin):
    """Pruebas de rendimiento para carrito de compras"""
    
    def setUp(self):
        self.client = APIClient()
        
        # Crear usuario y autenticar
        self.user = Usuario.objects.create_user(
            email='carrito@test.com',
            nombre='Carrito',
            apellido='Test',
            password='TestPassword123!'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        # Crear carrito
        self.carrito = Carrito.objects.create(id_usuario=self.user)
        
        # Crear productos
        self.categoria = Categoria.objects.create(nombre='Test', descripcion='Test')
        self.marca = Marca.objects.create(nombre='Test', descripcion='Test')
        
        self.productos = []
        for i in range(50):
            producto = Producto.objects.create(
                nombre=f'Producto Carrito {i}',
                descripcion=f'Descripción {i}',
                precio=50000 + (i * 1000),
                sku=f'CART-{i:03d}',
                stock=100,
                id_categoria=self.categoria,
                id_marca=self.marca
            )
            self.productos.append(producto)
    
    def test_agregar_carrito_performance(self):
        """Mide el rendimiento de agregar al carrito"""
        print("\n🛒 PRUEBA DE RENDIMIENTO: Agregar al Carrito")
        
        product_index = 0
        
        def agregar_carrito():
            nonlocal product_index
            producto = self.productos[product_index % len(self.productos)]
            product_index += 1
            
            response = self.client.post(
                reverse('carrito-list'),
                data=json.dumps({
                    'id_producto': producto.id,
                    'cantidad': 1
                }),
                content_type='application/json'
            )
            return response.status_code in [200, 201]
        
        stats = self.run_multiple_times(agregar_carrito, iterations=30)
        
        print(f"📊 Estadísticas de Agregar al Carrito:")
        print(f"   • Tiempo promedio: {stats['avg_time']:.4f}s")
        print(f"   • Items/segundo: {stats['iterations']/stats['total_time']:.2f}")
        
        self.assertLess(stats['avg_time'], 0.8, "Agregar al carrito debe ser < 0.8s")
    
    def test_ver_carrito_performance(self):
        """Mide el rendimiento de ver carrito"""
        print("\n👁️ PRUEBA DE RENDIMIENTO: Ver Carrito")
        
        # Agregar items al carrito
        for i in range(10):
            CarritoItem.objects.create(
                id_carrito=self.carrito,
                id_producto=self.productos[i],
                cantidad=2
            )
        
        def ver_carrito():
            response = self.client.get(reverse('carrito-list'))
            return response.status_code == 200
        
        stats = self.run_multiple_times(ver_carrito, iterations=100)
        
        print(f"📊 Estadísticas de Ver Carrito:")
        print(f"   • Tiempo promedio: {stats['avg_time']:.4f}s")
        print(f"   • Consultas/segundo: {stats['iterations']/stats['total_time']:.2f}")
        
        self.assertLess(stats['avg_time'], 0.4, "Ver carrito debe ser < 0.4s")


class DatabasePerformanceTests(TestCase, PerformanceTestMixin):
    """Pruebas de rendimiento de base de datos"""
    
    def setUp(self):
        # Crear datos de prueba para analizar queries
        self.categoria = Categoria.objects.create(nombre='Performance', descripcion='Test')
        self.marca = Marca.objects.create(nombre='Performance', descripcion='Test')
        
        # Crear muchos productos para pruebas de BD
        productos = []
        for i in range(500):
            productos.append(Producto(
                nombre=f'DB Test Product {i}',
                descripcion=f'Performance test product {i}',
                precio=100000 + i,
                sku=f'DB-{i:04d}',
                stock=10 + i,
                id_categoria=self.categoria,
                id_marca=self.marca
            ))
        
        Producto.objects.bulk_create(productos, batch_size=50)
    
    def test_query_performance(self):
        """Analiza el rendimiento de consultas complejas"""
        print("\n🗃️ PRUEBA DE RENDIMIENTO: Consultas de Base de Datos")
        
        def complex_query():
            # Query compleja con joins y filtros
            productos = Producto.objects.select_related(
                'id_categoria', 'id_marca'
            ).filter(
                precio__gte=100000,
                precio__lte=200000,
                stock__gt=50
            ).order_by('-precio')[:20]
            
            return len(list(productos)) > 0
        
        # Medir queries
        initial_queries = len(connection.queries)
        stats = self.run_multiple_times(complex_query, iterations=50)
        final_queries = len(connection.queries)
        
        queries_executed = final_queries - initial_queries
        
        print(f"📊 Estadísticas de Consultas BD:")
        print(f"   • Tiempo promedio: {stats['avg_time']:.4f}s")
        print(f"   • Consultas ejecutadas: {queries_executed}")
        print(f"   • Consultas/iteración: {queries_executed/stats['iterations']:.1f}")
        print(f"   • Queries/segundo: {queries_executed/stats['total_time']:.2f}")
        
        self.assertLess(stats['avg_time'], 0.1, "Query compleja debe ser < 0.1s")
        self.assertLessEqual(queries_executed/stats['iterations'], 5, "Máximo 5 queries por iteración")
    
    def test_bulk_operations_performance(self):
        """Prueba el rendimiento de operaciones en lote"""
        print("\n📦 PRUEBA DE RENDIMIENTO: Operaciones en Lote")
        
        def bulk_create_test():
            # Crear usuario
            user = Usuario.objects.create_user(
                email=f'bulk_{int(time.time() * 1000000)}@test.com',
                nombre='Bulk',
                apellido='Test',
                password='TestPassword123!'
            )
            
            # Crear carrito
            carrito = Carrito.objects.create(id_usuario=user)
            
            # Crear items en lote
            items = []
            productos = Producto.objects.all()[:10]
            for producto in productos:
                items.append(CarritoItem(
                    id_carrito=carrito,
                    id_producto=producto,
                    cantidad=1
                ))
            
            CarritoItem.objects.bulk_create(items)
            return len(items)
        
        stats = self.run_multiple_times(bulk_create_test, iterations=20)
        
        print(f"📊 Estadísticas de Operaciones en Lote:")
        print(f"   • Tiempo promedio: {stats['avg_time']:.4f}s")
        print(f"   • Operaciones/segundo: {stats['iterations']/stats['total_time']:.2f}")
        
        self.assertLess(stats['avg_time'], 2.0, "Operación en lote debe ser < 2s")


class MemoryPerformanceTests(TestCase, PerformanceTestMixin):
    """Pruebas de rendimiento de memoria"""
    
    def test_memory_usage_trends(self):
        """Analiza el uso de memoria durante operaciones"""
        print("\n🧠 PRUEBA DE RENDIMIENTO: Uso de Memoria")
        
        initial_memory = self.measure_memory_usage()
        print(f"   • Memoria inicial: {initial_memory:.2f} MB")
        
        # Crear muchos objetos para ver el uso de memoria
        usuarios = []
        for i in range(100):
            user = Usuario(
                email=f'memory_test_{i}@test.com',
                nombre=f'User{i}',
                apellido='Test',
                password='TestPassword123!'
            )
            usuarios.append(user)
        
        mid_memory = self.measure_memory_usage()
        print(f"   • Memoria después de crear objetos: {mid_memory:.2f} MB")
        print(f"   • Incremento: {mid_memory - initial_memory:.2f} MB")
        
        # Limpiar objetos
        usuarios.clear()
        
        final_memory = self.measure_memory_usage()
        print(f"   • Memoria final: {final_memory:.2f} MB")
        print(f"   • Diferencia total: {final_memory - initial_memory:.2f} MB")
        
        # Verificar que no hay leak extremo de memoria
        memory_increase = final_memory - initial_memory
        self.assertLess(memory_increase, 50, "Incremento de memoria debe ser < 50MB")


def run_performance_suite():
    """Función para ejecutar toda la suite de rendimiento"""
    print("=" * 80)
    print("🚀 INICIANDO SUITE COMPLETA DE PRUEBAS DE RENDIMIENTO")
    print("   Backend Clone Alkosto - Performance Testing")
    print("=" * 80)
    
    # Las pruebas se ejecutan automáticamente con Django test runner
    pass


if __name__ == '__main__':
    run_performance_suite()
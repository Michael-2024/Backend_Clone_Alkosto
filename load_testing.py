#!/usr/bin/env python
"""
Script de Carga y Estrés - Backend Clone Alkosto
===============================================

Este script ejecuta pruebas de carga intensivas para evaluar:
- Límites de capacidad del sistema
- Comportamiento bajo estrés extremo
- Identificación de puntos de falla
- Métricas de escalabilidad

Ejecutar con: python load_testing.py
"""

import time
import json
import threading
import requests
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import sys
import os

# Configuración del servidor
BASE_URL = "http://127.0.0.1:8000/api"
ADMIN_URL = "http://127.0.0.1:8000/admin"

class LoadTester:
    def __init__(self):
        self.results = []
        self.errors = []
        self.start_time = None
        self.end_time = None
        
    def create_test_user(self, user_id):
        """Crear usuario de prueba único"""
        user_data = {
            'email': f'loadtest_{user_id}@test.com',
            'nombre': f'LoadTest{user_id}',
            'apellido': 'User',
            'password': 'LoadTest123!',
            'password_confirm': 'LoadTest123!'
        }
        
        try:
            response = requests.post(f"{BASE_URL}/auth/registro/", 
                                   json=user_data, 
                                   timeout=30)
            return response.status_code == 201, response.json() if response.status_code == 201 else None
        except Exception as e:
            return False, str(e)
    
    def login_user(self, email, password):
        """Login de usuario"""
        try:
            response = requests.post(f"{BASE_URL}/auth/login/", 
                                   json={'email': email, 'password': password},
                                   timeout=30)
            if response.status_code == 200:
                return True, response.json().get('token')
            return False, response.text
        except Exception as e:
            return False, str(e)
    
    def search_products(self, query="Samsung", timeout=30):
        """Búsqueda de productos"""
        try:
            response = requests.get(f"{BASE_URL}/buscar/", 
                                  params={'q': query},
                                  timeout=timeout)
            return response.status_code == 200, len(response.json()) if response.status_code == 200 else 0
        except Exception as e:
            return False, str(e)
    
    def get_products(self, timeout=30):
        """Obtener lista de productos"""
        try:
            response = requests.get(f"{BASE_URL}/productos/", timeout=timeout)
            return response.status_code == 200, len(response.json()) if response.status_code == 200 else 0
        except Exception as e:
            return False, str(e)
    
    def measure_time(self, func, *args, **kwargs):
        """Medir tiempo de ejecución"""
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        return result, end - start
    
    def worker_thread(self, thread_id, operations_per_thread, test_type="mixed"):
        """Worker thread para pruebas concurrentes"""
        thread_results = []
        thread_errors = []
        
        # Crear usuario para este thread
        success, user_data = self.create_test_user(thread_id)
        if not success:
            thread_errors.append(f"Thread {thread_id}: Error creando usuario - {user_data}")
            return thread_results, thread_errors
        
        # Login del usuario
        token = None
        if success and user_data:
            email = f'loadtest_{thread_id}@test.com'
            login_success, token_data = self.login_user(email, 'LoadTest123!')
            if login_success:
                token = token_data
        
        # Ejecutar operaciones
        for op in range(operations_per_thread):
            try:
                if test_type == "search" or (test_type == "mixed" and op % 3 == 0):
                    # Búsqueda de productos
                    result, exec_time = self.measure_time(self.search_products, "smartphone")
                    thread_results.append({
                        'thread_id': thread_id,
                        'operation': 'search',
                        'success': result[0],
                        'time': exec_time,
                        'data': result[1] if result[0] else result[1]
                    })
                
                elif test_type == "products" or (test_type == "mixed" and op % 3 == 1):
                    # Listar productos
                    result, exec_time = self.measure_time(self.get_products)
                    thread_results.append({
                        'thread_id': thread_id,
                        'operation': 'list_products',
                        'success': result[0],
                        'time': exec_time,
                        'data': result[1] if result[0] else result[1]
                    })
                
                else:
                    # Búsqueda alternativa
                    result, exec_time = self.measure_time(self.search_products, "producto")
                    thread_results.append({
                        'thread_id': thread_id,
                        'operation': 'search_alt',
                        'success': result[0],
                        'time': exec_time,
                        'data': result[1] if result[0] else result[1]
                    })
                
                # Pequeña pausa entre operaciones
                if test_type != "stress":
                    time.sleep(0.1)
                
            except Exception as e:
                thread_errors.append(f"Thread {thread_id} Op {op}: {str(e)}")
        
        return thread_results, thread_errors
    
    def run_load_test(self, num_threads=10, operations_per_thread=5, test_type="mixed"):
        """Ejecutar prueba de carga"""
        print(f"\n🚀 INICIANDO PRUEBA DE CARGA")
        print(f"   • Threads concurrentes: {num_threads}")
        print(f"   • Operaciones por thread: {operations_per_thread}")
        print(f"   • Tipo de prueba: {test_type}")
        print(f"   • Total de operaciones: {num_threads * operations_per_thread}")
        print(f"   • Iniciando en: {datetime.now().strftime('%H:%M:%S')}")
        
        self.start_time = time.perf_counter()
        all_results = []
        all_errors = []
        
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            # Enviar workers
            futures = [
                executor.submit(self.worker_thread, i, operations_per_thread, test_type)
                for i in range(num_threads)
            ]
            
            # Recoger resultados
            completed = 0
            for future in as_completed(futures):
                completed += 1
                print(f"   ⏳ Progreso: {completed}/{num_threads} threads completados...")
                
                try:
                    thread_results, thread_errors = future.result()
                    all_results.extend(thread_results)
                    all_errors.extend(thread_errors)
                except Exception as e:
                    all_errors.append(f"Error en thread: {str(e)}")
        
        self.end_time = time.perf_counter()
        self.results = all_results
        self.errors = all_errors
        
        return self.analyze_results()
    
    def analyze_results(self):
        """Analizar resultados de las pruebas"""
        if not self.results:
            return {"error": "No hay resultados para analizar"}
        
        total_time = self.end_time - self.start_time
        total_operations = len(self.results)
        successful_operations = len([r for r in self.results if r['success']])
        failed_operations = total_operations - successful_operations
        
        # Estadísticas de tiempo
        times = [r['time'] for r in self.results if r['success']]
        
        # Agrupar por tipo de operación
        operations_by_type = {}
        for result in self.results:
            op_type = result['operation']
            if op_type not in operations_by_type:
                operations_by_type[op_type] = []
            operations_by_type[op_type].append(result)
        
        stats = {
            'summary': {
                'total_operations': total_operations,
                'successful_operations': successful_operations,
                'failed_operations': failed_operations,
                'success_rate': (successful_operations / total_operations) * 100 if total_operations > 0 else 0,
                'total_test_time': total_time,
                'operations_per_second': successful_operations / total_time if total_time > 0 else 0
            },
            'timing_stats': {
                'min_time': min(times) if times else 0,
                'max_time': max(times) if times else 0,
                'avg_time': statistics.mean(times) if times else 0,
                'median_time': statistics.median(times) if times else 0,
                'std_dev': statistics.stdev(times) if len(times) > 1 else 0
            },
            'operations_breakdown': {},
            'errors': self.errors[:10],  # Primeros 10 errores
            'total_errors': len(self.errors)
        }
        
        # Análisis por tipo de operación
        for op_type, results in operations_by_type.items():
            successful = [r for r in results if r['success']]
            times_op = [r['time'] for r in successful]
            
            stats['operations_breakdown'][op_type] = {
                'total': len(results),
                'successful': len(successful),
                'success_rate': (len(successful) / len(results)) * 100 if results else 0,
                'avg_time': statistics.mean(times_op) if times_op else 0,
                'min_time': min(times_op) if times_op else 0,
                'max_time': max(times_op) if times_op else 0
            }
        
        return stats
    
    def print_results(self, stats):
        """Imprimir resultados formateados"""
        print("\n" + "="*80)
        print("📊 RESULTADOS DE PRUEBA DE CARGA")
        print("="*80)
        
        summary = stats['summary']
        timing = stats['timing_stats']
        
        print(f"\n🎯 RESUMEN GENERAL:")
        print(f"   • Total de operaciones: {summary['total_operations']}")
        print(f"   • Operaciones exitosas: {summary['successful_operations']}")
        print(f"   • Operaciones fallidas: {summary['failed_operations']}")
        print(f"   • Tasa de éxito: {summary['success_rate']:.2f}%")
        print(f"   • Tiempo total de prueba: {summary['total_test_time']:.2f}s")
        print(f"   • Throughput: {summary['operations_per_second']:.2f} ops/segundo")
        
        print(f"\n⏱️ ESTADÍSTICAS DE TIEMPO:")
        print(f"   • Tiempo mínimo: {timing['min_time']:.4f}s")
        print(f"   • Tiempo máximo: {timing['max_time']:.4f}s")
        print(f"   • Tiempo promedio: {timing['avg_time']:.4f}s")
        print(f"   • Tiempo mediano: {timing['median_time']:.4f}s")
        print(f"   • Desviación estándar: {timing['std_dev']:.4f}s")
        
        print(f"\n📋 DESGLOSE POR OPERACIÓN:")
        for op_type, op_stats in stats['operations_breakdown'].items():
            print(f"   📌 {op_type.upper()}:")
            print(f"      • Total: {op_stats['total']}")
            print(f"      • Exitosas: {op_stats['successful']}")
            print(f"      • Tasa éxito: {op_stats['success_rate']:.2f}%")
            print(f"      • Tiempo promedio: {op_stats['avg_time']:.4f}s")
            print(f"      • Rango: {op_stats['min_time']:.4f}s - {op_stats['max_time']:.4f}s")
        
        if stats['total_errors'] > 0:
            print(f"\n🚨 ERRORES ENCONTRADOS ({stats['total_errors']} total):")
            for i, error in enumerate(stats['errors'][:5], 1):
                print(f"   {i}. {error}")
            if stats['total_errors'] > 5:
                print(f"   ... y {stats['total_errors'] - 5} errores más")
        
        # Evaluación de rendimiento
        print(f"\n🏆 EVALUACIÓN DE RENDIMIENTO:")
        
        if summary['success_rate'] >= 95:
            print(f"   ✅ ESTABILIDAD: EXCELENTE ({summary['success_rate']:.1f}%)")
        elif summary['success_rate'] >= 85:
            print(f"   ⚠️ ESTABILIDAD: BUENA ({summary['success_rate']:.1f}%)")
        else:
            print(f"   🔴 ESTABILIDAD: CRÍTICA ({summary['success_rate']:.1f}%)")
        
        if timing['avg_time'] <= 0.5:
            print(f"   ✅ VELOCIDAD: EXCELENTE ({timing['avg_time']:.3f}s)")
        elif timing['avg_time'] <= 2.0:
            print(f"   ⚠️ VELOCIDAD: ACEPTABLE ({timing['avg_time']:.3f}s)")
        else:
            print(f"   🔴 VELOCIDAD: LENTA ({timing['avg_time']:.3f}s)")
        
        if summary['operations_per_second'] >= 50:
            print(f"   ✅ THROUGHPUT: EXCELENTE ({summary['operations_per_second']:.1f} ops/s)")
        elif summary['operations_per_second'] >= 10:
            print(f"   ⚠️ THROUGHPUT: ACEPTABLE ({summary['operations_per_second']:.1f} ops/s)")
        else:
            print(f"   🔴 THROUGHPUT: BAJO ({summary['operations_per_second']:.1f} ops/s)")


def main():
    """Función principal para ejecutar pruebas"""
    tester = LoadTester()
    
    print("🔥 SUITE DE PRUEBAS DE CARGA - BACKEND CLONE ALKOSTO")
    print("="*60)
    
    # Verificar que el servidor esté corriendo
    try:
        response = requests.get(f"{BASE_URL}/productos/", timeout=5)
        if response.status_code != 200:
            print("❌ ERROR: El servidor no está respondiendo correctamente")
            print("   Asegúrate de que el backend esté ejecutándose en http://127.0.0.1:8000")
            return
    except requests.exceptions.RequestException:
        print("❌ ERROR: No se puede conectar al servidor")
        print("   Asegúrate de que el backend esté ejecutándose en http://127.0.0.1:8000")
        return
    
    print("✅ Servidor detectado y funcionando")
    
    # Batería de pruebas
    tests = [
        {"name": "Prueba Ligera", "threads": 5, "ops": 3, "type": "mixed"},
        {"name": "Prueba Moderada", "threads": 10, "ops": 5, "type": "mixed"},
        {"name": "Prueba de Búsqueda Intensiva", "threads": 8, "ops": 10, "type": "search"},
        {"name": "Prueba de Listado Intensiva", "threads": 8, "ops": 10, "type": "products"},
        {"name": "Prueba de Estrés", "threads": 20, "ops": 8, "type": "stress"},
    ]
    
    for i, test in enumerate(tests, 1):
        print(f"\n{'='*60}")
        print(f"🧪 EJECUTANDO: {test['name']} ({i}/{len(tests)})")
        print(f"{'='*60}")
        
        stats = tester.run_load_test(
            num_threads=test['threads'],
            operations_per_thread=test['ops'],
            test_type=test['type']
        )
        
        tester.print_results(stats)
        
        # Pausa entre pruebas
        if i < len(tests):
            print(f"\n⏸️ Pausa de 10 segundos antes de la siguiente prueba...")
            time.sleep(10)
    
    print(f"\n🏁 TODAS LAS PRUEBAS COMPLETADAS")
    print(f"📅 Finalizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
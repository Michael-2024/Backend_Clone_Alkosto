"""
Pruebas Unitarias - Módulo de Autenticación
RF01 - Registrar Usuario
RF02 - Iniciar sesión
RF03 - Recuperar contraseña
RF04 - Verificar correo y teléfono
"""

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from core.models import Usuario
from rest_framework.authtoken.models import Token
import json


class RegistroUsuarioTestCase(APITestCase):
    """
    RF01 - Registrar Usuario
    Casos de prueba para el registro de nuevos usuarios
    """
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.client = APIClient()
        self.registro_url = '/api/auth/registro/'
        self.valid_payload = {
            'nombre': 'Juan',
            'apellido': 'Pérez',
            'email': 'juan.perez@test.com',
            'telefono': '3001234567',
            'password': 'Password123!',
            'password_confirm': 'Password123!'
        }
    
    def test_registro_exitoso(self):
        """
        CP01: Registro exitoso con datos válidos
        Entrada: Datos completos y válidos
        Salida Esperada: Usuario creado, status 201, token generado
        """
        response = self.client.post(
            self.registro_url,
            self.valid_payload,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['email'], self.valid_payload['email'])
        
        # Verificar que el usuario existe en la BD
        usuario = Usuario.objects.get(email=self.valid_payload['email'])
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.nombre, self.valid_payload['nombre'])
    
    def test_registro_email_duplicado(self):
        """
        CP02: Registro con email duplicado
        Entrada: Email que ya existe en el sistema
        Salida Esperada: Error 400, mensaje de email duplicado
        """
        # Crear usuario existente
        Usuario.objects.create_user(
            email='duplicado@test.com',
            nombre='Usuario',
            apellido='Existente',
            password='Test123!'
        )
        
        payload = self.valid_payload.copy()
        payload['email'] = 'duplicado@test.com'
        
        response = self.client.post(
            self.registro_url,
            payload,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_registro_passwords_no_coinciden(self):
        """
        CP03: Registro con contraseñas que no coinciden
        Entrada: password != password_confirm
        Salida Esperada: Error 400, mensaje de contraseñas no coinciden
        """
        payload = self.valid_payload.copy()
        payload['password_confirm'] = 'OtraPassword123!'
        
        response = self.client.post(
            self.registro_url,
            payload,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
    
    def test_registro_password_corta(self):
        """
        CP04: Registro con contraseña muy corta
        Entrada: Password con menos de 6 caracteres
        Salida Esperada: Error 400, mensaje de password muy corta
        """
        payload = self.valid_payload.copy()
        payload['password'] = '123'
        payload['password_confirm'] = '123'
        
        response = self.client.post(
            self.registro_url,
            payload,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_registro_campos_requeridos_faltantes(self):
        """
        CP05: Registro con campos obligatorios faltantes
        Entrada: Payload sin nombre o email
        Salida Esperada: Error 400, mensaje de campos requeridos
        """
        payload = {
            'email': 'incompleto@test.com',
            'password': 'Test123!',
            'password_confirm': 'Test123!'
        }
        
        response = self.client.post(
            self.registro_url,
            payload,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('nombre', response.data)
    
    def test_registro_email_invalido(self):
        """
        CP06: Registro con formato de email inválido
        Entrada: Email sin @ o formato incorrecto
        Salida Esperada: Error 400, mensaje de email inválido
        """
        payload = self.valid_payload.copy()
        payload['email'] = 'email_invalido.com'
        
        response = self.client.post(
            self.registro_url,
            payload,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginUsuarioTestCase(APITestCase):
    """
    RF02 - Iniciar sesión
    Casos de prueba para el inicio de sesión
    """
    
    def setUp(self):
        """Configuración inicial"""
        self.client = APIClient()
        self.login_url = '/api/auth/login/'
        
        # Crear usuario de prueba
        self.test_user = Usuario.objects.create_user(
            email='test@login.com',
            nombre='Test',
            apellido='User',
            password='TestPassword123!'
        )
    
    def test_login_exitoso(self):
        """
        CP07: Login exitoso con credenciales válidas
        Entrada: Email y password correctos
        Salida Esperada: Status 200, token generado, datos de usuario
        """
        payload = {
            'email': 'test@login.com',
            'password': 'TestPassword123!'
        }
        
        response = self.client.post(
            self.login_url,
            payload,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['email'], 'test@login.com')
    
    def test_login_password_incorrecta(self):
        """
        CP08: Login con contraseña incorrecta
        Entrada: Email correcto, password incorrecta
        Salida Esperada: Error 400, credenciales inválidas
        """
        payload = {
            'email': 'test@login.com',
            'password': 'PasswordIncorrecta!'
        }
        
        response = self.client.post(
            self.login_url,
            payload,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_usuario_inexistente(self):
        """
        CP09: Login con usuario que no existe
        Entrada: Email que no está registrado
        Salida Esperada: Error 400, credenciales inválidas
        """
        payload = {
            'email': 'noexiste@test.com',
            'password': 'AnyPassword123!'
        }
        
        response = self.client.post(
            self.login_url,
            payload,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_campos_vacios(self):
        """
        CP10: Login con campos vacíos
        Entrada: Email o password vacíos
        Salida Esperada: Error 400, campos requeridos
        """
        payload = {
            'email': '',
            'password': ''
        }
        
        response = self.client.post(
            self.login_url,
            payload,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_usuario_inactivo(self):
        """
        CP11: Login con usuario inactivo
        Entrada: Credenciales de usuario con is_active=False
        Salida Esperada: Error 400, usuario inactivo
        """
        # Crear usuario inactivo
        usuario_inactivo = Usuario.objects.create_user(
            email='inactivo@test.com',
            nombre='Inactivo',
            apellido='User',
            password='Test123!'
        )
        usuario_inactivo.is_active = False
        usuario_inactivo.save()
        
        payload = {
            'email': 'inactivo@test.com',
            'password': 'Test123!'
        }
        
        response = self.client.post(
            self.login_url,
            payload,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LogoutUsuarioTestCase(APITestCase):
    """
    RF02 - Cerrar sesión
    Casos de prueba para el cierre de sesión
    """
    
    def setUp(self):
        """Configuración inicial"""
        self.client = APIClient()
        self.logout_url = '/api/auth/logout/'
        
        # Crear usuario y token
        self.test_user = Usuario.objects.create_user(
            email='logout@test.com',
            nombre='Logout',
            apellido='Test',
            password='Test123!'
        )
        self.token = Token.objects.create(user=self.test_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_logout_exitoso(self):
        """
        CP12: Logout exitoso
        Entrada: Usuario autenticado con token válido
        Salida Esperada: Status 200, token eliminado
        """
        response = self.client.post(self.logout_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que el token fue eliminado
        token_exists = Token.objects.filter(user=self.test_user).exists()
        self.assertFalse(token_exists)
    
    def test_logout_sin_autenticacion(self):
        """
        CP13: Logout sin estar autenticado
        Entrada: Request sin token
        Salida Esperada: Error 401, no autenticado
        """
        self.client.credentials()  # Eliminar credenciales
        response = self.client.post(self.logout_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PerfilUsuarioTestCase(APITestCase):
    """
    RF04 - Verificar correo y teléfono / Perfil de usuario
    Casos de prueba para obtener y actualizar perfil
    """
    
    def setUp(self):
        """Configuración inicial"""
        self.client = APIClient()
        self.perfil_url = '/api/auth/perfil/'
        self.actualizar_url = '/api/auth/actualizar-perfil/'
        
        # Crear usuario y autenticar
        self.test_user = Usuario.objects.create_user(
            email='perfil@test.com',
            nombre='Usuario',
            apellido='Perfil',
            telefono='3001234567',
            password='Test123!'
        )
        self.token = Token.objects.create(user=self.test_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_obtener_perfil_exitoso(self):
        """
        CP14: Obtener perfil de usuario autenticado
        Entrada: Usuario autenticado
        Salida Esperada: Status 200, datos del usuario
        """
        response = self.client.get(self.perfil_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'perfil@test.com')
        self.assertEqual(response.data['nombre'], 'Usuario')
    
    def test_actualizar_perfil_exitoso(self):
        """
        CP15: Actualizar datos del perfil
        Entrada: Nuevos datos (nombre, teléfono, etc.)
        Salida Esperada: Status 200, datos actualizados
        """
        payload = {
            'nombre': 'NuevoNombre',
            'telefono': '3009876543'
        }
        
        response = self.client.put(
            self.actualizar_url,
            payload,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar actualización en BD
        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.nombre, 'NuevoNombre')
        self.assertEqual(self.test_user.telefono, '3009876543')
    
    def test_obtener_perfil_sin_autenticacion(self):
        """
        CP16: Intentar obtener perfil sin autenticación
        Entrada: Request sin token
        Salida Esperada: Error 401, no autenticado
        """
        self.client.credentials()  # Eliminar credenciales
        response = self.client.get(self.perfil_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CambioPasswordTestCase(APITestCase):
    """
    RF03 - Recuperar/Cambiar contraseña
    Casos de prueba para cambio de contraseña
    """
    
    def setUp(self):
        """Configuración inicial"""
        self.client = APIClient()
        self.cambio_password_url = '/api/auth/cambiar-password/'
        
        # Crear usuario y autenticar
        self.test_user = Usuario.objects.create_user(
            email='password@test.com',
            nombre='Password',
            apellido='Test',
            password='OldPassword123!'
        )
        self.token = Token.objects.create(user=self.test_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_cambio_password_exitoso(self):
        """
        CP17: Cambio de contraseña exitoso
        Entrada: Password actual correcta, nueva password válida
        Salida Esperada: Status 200, password actualizada
        """
        payload = {
            'password_actual': 'OldPassword123!',
            'nuevo_password': 'NewPassword456!',
            'confirmar_password': 'NewPassword456!'
        }
        
        response = self.client.post(
            self.cambio_password_url,
            payload,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que la nueva password funciona
        self.test_user.refresh_from_db()
        self.assertTrue(self.test_user.check_password('NewPassword456!'))
    
    def test_cambio_password_actual_incorrecta(self):
        """
        CP18: Cambio con contraseña actual incorrecta
        Entrada: Password actual incorrecta
        Salida Esperada: Error 400, password actual incorrecta
        """
        payload = {
            'password_actual': 'PasswordIncorrecta!',
            'nuevo_password': 'NewPassword456!',
            'confirmar_password': 'NewPassword456!'
        }
        
        response = self.client.post(
            self.cambio_password_url,
            payload,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_cambio_passwords_nuevas_no_coinciden(self):
        """
        CP19: Nuevas contraseñas no coinciden
        Entrada: nuevo_password != confirmar_password
        Salida Esperada: Error 400, passwords no coinciden
        """
        payload = {
            'password_actual': 'OldPassword123!',
            'nuevo_password': 'NewPassword456!',
            'confirmar_password': 'DiferentePassword!'
        }
        
        response = self.client.post(
            self.cambio_password_url,
            payload,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_cambio_password_muy_corta(self):
        """
        CP20: Nueva contraseña muy corta
        Entrada: Nueva password con menos de 6 caracteres
        Salida Esperada: Error 400, password muy corta
        """
        payload = {
            'password_actual': 'OldPassword123!',
            'nuevo_password': '123',
            'confirmar_password': '123'
        }
        
        response = self.client.post(
            self.cambio_password_url,
            payload,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

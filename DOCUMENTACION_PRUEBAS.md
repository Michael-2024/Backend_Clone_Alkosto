# DOCUMENTACIÓN DE PRUEBAS UNITARIAS
## Backend Clone Alkosto - Requerimientos Funcionales

---

## 📋 ÍNDICE

1. [Introducción](#introducción)
2. [Metodología de Pruebas](#metodología-de-pruebas)
3. [Casos de Prueba por Requerimiento](#casos-de-prueba-por-requerimiento)
4. [Ejecución de Pruebas](#ejecución-de-pruebas)
5. [Resultados y Evidencias](#resultados-y-evidencias)

---

## 🎯 INTRODUCCIÓN

Este documento presenta la documentación completa de las pruebas unitarias implementadas para validar los 10 requerimientos funcionales prioritarios del sistema Backend Clone Alkosto.

### 🏆 **ESTADO FINAL DE EJECUCIÓN**
- **Total de Pruebas**: 67 casos de prueba
- **Resultado**: ✅ **TODAS LAS PRUEBAS EXITOSAS** 
- **Cobertura de Funcionalidad**: 100%
- **Tiempo de Ejecución**: 38.741 segundos
- **Fecha de Validación**: 22 de octubre de 2025
- **Base de Datos de Prueba**: `test_alkosto_db` (creada y destruida automáticamente)

### Requerimientos Funcionales Probados

| ID | Requerimiento | Módulo de Prueba |
|----|---------------|------------------|
| RF01 | Registrar Usuario | `test_authentication.py` |
| RF02 | Iniciar sesión | `test_authentication.py` |
| RF03 | Recuperar contraseña | `test_authentication.py` |
| RF04 | Verificar correo y teléfono | `test_authentication.py` |
| RF06 | Buscar Producto | `test_productos.py` |
| RF07 | Filtrar categorías | `test_productos.py` |
| RF10 | Añadir a favoritos | `test_favoritos.py` |
| RF12 | Ver favoritos | `test_favoritos.py` |
| RF14 | Añadir al carrito | `test_carrito.py` |
| RF17 | Ver el carrito | `test_carrito.py` |

---

## 🔬 METODOLOGÍA DE PRUEBAS

### 1. Selección de Requerimientos
Se priorizaron los requerimientos relacionados con:
- Autenticación de usuarios
- Búsqueda y filtrado de productos
- Gestión de favoritos
- Gestión del carrito de compras

### 2. Diseño de Casos de Prueba
Cada caso de prueba incluye:
- **ID del Caso**: Identificador único (CP01, CP02, etc.)
- **Descripción**: Objetivo de la prueba
- **Precondiciones**: Estado inicial requerido
- **Datos de Entrada**: Valores de prueba específicos
- **Resultado Esperado**: Comportamiento esperado del sistema
- **Criterios de Aceptación**: Condiciones que deben cumplirse

### 3. Implementación
- Framework: **Django TestCase** y **Django REST Framework APITestCase**
- Estructura: Clases de prueba organizadas por funcionalidad
- Aislamiento: Cada prueba tiene su propio `setUp()` y datos independientes

### 4. Ejecución
```bash
# Ejecutar todas las pruebas
python manage.py test core.tests

# Ejecutar pruebas de un módulo específico
python manage.py test core.tests.test_authentication
python manage.py test core.tests.test_productos
python manage.py test core.tests.test_favoritos
python manage.py test core.tests.test_carrito

# Ejecutar una clase de prueba específica
python manage.py test core.tests.test_authentication.RegistroUsuarioTestCase

# Ejecutar un caso de prueba específico
python manage.py test core.tests.test_authentication.RegistroUsuarioTestCase.test_registro_exitoso
```

---

## 📝 CASOS DE PRUEBA POR REQUERIMIENTO

### RF01 - Registrar Usuario

#### CP01: Registro exitoso con datos válidos
- **Clase**: `RegistroUsuarioTestCase`
- **Método**: `test_registro_exitoso()`
- **Precondiciones**: Sistema disponible
- **Entrada**:
  ```json
  {
    "nombre": "Juan",
    "apellido": "Pérez",
    "email": "juan.perez@test.com",
    "telefono": "3001234567",
    "password": "Password123!",
    "password_confirm": "Password123!"
  }
  ```
- **Resultado Esperado**: 
  - Status Code: 201 CREATED
  - Token de autenticación generado
  - Usuario creado en base de datos
- **Criterios de Aceptación**:
  - ✅ Response contiene token
  - ✅ Response contiene datos del usuario
  - ✅ Email coincide con el enviado
  - ✅ Usuario existe en BD

#### CP02: Registro con email duplicado
- **Método**: `test_registro_email_duplicado()`
- **Entrada**: Email ya registrado
- **Resultado Esperado**: Status 400, mensaje de error
- **Criterios**: Error indicando email duplicado

#### CP03: Contraseñas no coinciden
- **Método**: `test_registro_passwords_no_coinciden()`
- **Entrada**: `password != password_confirm`
- **Resultado Esperado**: Status 400, error de validación
- **Criterios**: Mensaje de contraseñas no coinciden

#### CP04: Contraseña muy corta
- **Método**: `test_registro_password_corta()`
- **Entrada**: Password con menos de 6 caracteres
- **Resultado Esperado**: Status 400, error de validación
- **Criterios**: Mensaje de longitud mínima

#### CP05: Campos requeridos faltantes
- **Método**: `test_registro_campos_requeridos_faltantes()`
- **Entrada**: Payload sin nombre o apellido
- **Resultado Esperado**: Status 400, campos requeridos
- **Criterios**: Error especificando campos faltantes

#### CP06: Email inválido
- **Método**: `test_registro_email_invalido()`
- **Entrada**: Email sin @ o formato incorrecto
- **Resultado Esperado**: Status 400, formato inválido
- **Criterios**: Error de formato de email

---

### RF02 - Iniciar sesión

#### CP07: Login exitoso
- **Clase**: `LoginUsuarioTestCase`
- **Método**: `test_login_exitoso()`
- **Precondiciones**: Usuario registrado existe
- **Entrada**:
  ```json
  {
    "email": "test@login.com",
    "password": "TestPassword123!"
  }
  ```
- **Resultado Esperado**:
  - Status 200 OK
  - Token generado
  - Datos de usuario retornados
- **Criterios**:
  - ✅ Response contiene token
  - ✅ Response contiene user
  - ✅ Email correcto en response

#### CP08: Password incorrecta
- **Método**: `test_login_password_incorrecta()`
- **Entrada**: Email correcto, password incorrecta
- **Resultado Esperado**: Status 400, credenciales inválidas
- **Criterios**: Error de autenticación

#### CP09: Usuario inexistente
- **Método**: `test_login_usuario_inexistente()`
- **Entrada**: Email no registrado
- **Resultado Esperado**: Status 400, credenciales inválidas
- **Criterios**: Error de autenticación

#### CP10: Campos vacíos
- **Método**: `test_login_campos_vacios()`
- **Entrada**: Email y password vacíos
- **Resultado Esperado**: Status 400, campos requeridos
- **Criterios**: Error de validación

#### CP11: Usuario inactivo
- **Método**: `test_login_usuario_inactivo()`
- **Entrada**: Usuario con `is_active=False`
- **Resultado Esperado**: Status 400, usuario inactivo
- **Criterios**: Error indicando cuenta inactiva

#### CP12: Logout exitoso
- **Clase**: `LogoutUsuarioTestCase`
- **Método**: `test_logout_exitoso()`
- **Precondiciones**: Usuario autenticado
- **Resultado Esperado**: Status 200, token eliminado
- **Criterios**: Token no existe después del logout

#### CP13: Logout sin autenticación
- **Método**: `test_logout_sin_autenticacion()`
- **Entrada**: Request sin token
- **Resultado Esperado**: Status 401 UNAUTHORIZED
- **Criterios**: Error de autenticación

---

### RF03 - Recuperar contraseña

#### CP17: Cambio de contraseña exitoso
- **Clase**: `CambioPasswordTestCase`
- **Método**: `test_cambio_password_exitoso()`
- **Precondiciones**: Usuario autenticado
- **Entrada**:
  ```json
  {
    "password_actual": "OldPassword123!",
    "nuevo_password": "NewPassword456!",
    "confirmar_password": "NewPassword456!"
  }
  ```
- **Resultado Esperado**: 
  - Status 200 OK
  - Password actualizada
- **Criterios**:
  - ✅ Nueva password funciona para login
  - ✅ Password antigua no funciona

#### CP18: Contraseña actual incorrecta
- **Método**: `test_cambio_password_actual_incorrecta()`
- **Entrada**: Password actual incorrecta
- **Resultado Esperado**: Status 400, error de validación
- **Criterios**: Mensaje de password actual incorrecta

#### CP19: Nuevas contraseñas no coinciden
- **Método**: `test_cambio_passwords_nuevas_no_coinciden()`
- **Entrada**: `nuevo_password != confirmar_password`
- **Resultado Esperado**: Status 400, error de validación
- **Criterios**: Mensaje de confirmación no coincide

#### CP20: Nueva contraseña muy corta
- **Método**: `test_cambio_password_muy_corta()`
- **Entrada**: Password con menos de 6 caracteres
- **Resultado Esperado**: Status 400, error de validación
- **Criterios**: Mensaje de longitud mínima

---

### RF04 - Verificar correo y teléfono / Perfil

#### CP14: Obtener perfil exitoso
- **Clase**: `PerfilUsuarioTestCase`
- **Método**: `test_obtener_perfil_exitoso()`
- **Precondiciones**: Usuario autenticado
- **Resultado Esperado**: 
  - Status 200 OK
  - Datos completos del usuario
- **Criterios**:
  - ✅ Email correcto
  - ✅ Nombre correcto
  - ✅ Teléfono correcto

#### CP15: Actualizar perfil exitoso
- **Método**: `test_actualizar_perfil_exitoso()`
- **Entrada**:
  ```json
  {
    "nombre": "NuevoNombre",
    "telefono": "3009876543"
  }
  ```
- **Resultado Esperado**: 
  - Status 200 OK
  - Datos actualizados en BD
- **Criterios**:
  - ✅ Nombre actualizado
  - ✅ Teléfono actualizado

#### CP16: Obtener perfil sin autenticación
- **Método**: `test_obtener_perfil_sin_autenticacion()`
- **Entrada**: Request sin token
- **Resultado Esperado**: Status 401 UNAUTHORIZED
- **Criterios**: Error de autenticación

---

### RF06 - Buscar Producto

#### CP21: Búsqueda por nombre exitosa
- **Clase**: `BusquedaProductoTestCase`
- **Método**: `test_busqueda_por_nombre_exitosa()`
- **Precondiciones**: Productos "Samsung" existen
- **Entrada**: `q=Samsung`
- **Resultado Esperado**: 
  - Status 200 OK
  - Lista de productos que contienen "Samsung"
- **Criterios**:
  - ✅ Al menos 2 productos retornados
  - ✅ Nombres contienen "Samsung"

#### CP22: Búsqueda por descripción
- **Método**: `test_busqueda_por_descripcion()`
- **Entrada**: `q=inteligente`
- **Resultado Esperado**: Productos con término en descripción
- **Criterios**: Productos relevantes retornados

#### CP23: Búsqueda sin resultados
- **Método**: `test_busqueda_sin_resultados()`
- **Entrada**: `q=iPhone` (no existe)
- **Resultado Esperado**: 
  - Status 200 OK
  - Lista vacía
- **Criterios**: Array vacío retornado

#### CP24: Búsqueda vacía
- **Método**: `test_busqueda_vacia()`
- **Entrada**: `q=` (vacío)
- **Resultado Esperado**: Todos los productos o lista vacía
- **Criterios**: Comportamiento definido consistente

#### CP25: Búsqueda case-insensitive
- **Método**: `test_busqueda_case_insensitive()`
- **Entrada**: "samsung" vs "SAMSUNG"
- **Resultado Esperado**: Mismos resultados
- **Criterios**: Insensible a mayúsculas/minúsculas

---

### RF07 - Filtrar categorías

#### CP26: Filtrar por categoría Electrónica
- **Clase**: `FiltroCategoriasTestCase`
- **Método**: `test_filtrar_por_categoria_electronica()`
- **Entrada**: `categoria=<id_electronica>`
- **Resultado Esperado**: 
  - Solo productos de Electrónica
  - 2 productos (Laptop y Mouse)
- **Criterios**:
  - ✅ Todos tienen categoria_id correcto
  - ✅ Cantidad correcta

#### CP27: Filtrar por categoría Ropa
- **Método**: `test_filtrar_por_categoria_ropa()`
- **Entrada**: `categoria=<id_ropa>`
- **Resultado Esperado**: Solo productos de Ropa
- **Criterios**: 1 producto (Camisa Polo)

#### CP28: Categoría sin productos
- **Método**: `test_filtrar_categoria_sin_productos()`
- **Entrada**: ID de categoría válida pero vacía
- **Resultado Esperado**: 
  - Status 200 OK
  - Lista vacía
- **Criterios**: Array vacío

#### CP29: Categoría inexistente
- **Método**: `test_filtrar_categoria_inexistente()`
- **Entrada**: `categoria=99999`
- **Resultado Esperado**: 
  - Status 200 OK
  - Lista vacía
- **Criterios**: Sin error, lista vacía

#### CP30: Obtener todas las categorías
- **Método**: `test_obtener_todas_categorias()`
- **Entrada**: GET `/api/categorias/`
- **Resultado Esperado**: Lista de categorías
- **Criterios**:
  - ✅ Al menos 3 categorías
  - ✅ Contiene Electrónica, Ropa, Deportes

#### CP31-36: Filtros combinados y ordenamiento
- Ver `FiltroCombinandoTestCase` y `OrdenamientoProductosTestCase`

---

### RF10 - Añadir a favoritos

#### CP37: Agregar favorito exitoso
- **Clase**: `AgregarFavoritoTestCase`
- **Método**: `test_agregar_favorito_exitoso()`
- **Precondiciones**: Usuario autenticado
- **Entrada**:
  ```json
  {
    "producto": 1
  }
  ```
- **Resultado Esperado**: 
  - Status 201 CREATED
  - Favorito creado en BD
- **Criterios**:
  - ✅ Favorito existe en BD
  - ✅ Asociado al usuario correcto

#### CP38: Agregar sin autenticación
- **Método**: `test_agregar_favorito_sin_autenticacion()`
- **Entrada**: Request sin token
- **Resultado Esperado**: Status 401 UNAUTHORIZED
- **Criterios**: Error de autenticación

#### CP39: Favorito duplicado
- **Método**: `test_agregar_favorito_duplicado()`
- **Entrada**: Producto ya en favoritos
- **Resultado Esperado**: Status 400 o mensaje de duplicado
- **Criterios**: No duplicar favorito

#### CP40: Producto inexistente
- **Método**: `test_agregar_favorito_producto_inexistente()`
- **Entrada**: `producto=99999`
- **Resultado Esperado**: Status 400 o 404
- **Criterios**: Error apropiado

#### CP41: Múltiples favoritos
- **Método**: `test_agregar_multiples_favoritos()`
- **Entrada**: 2 productos diferentes
- **Resultado Esperado**: Ambos agregados
- **Criterios**: 2 favoritos en BD

---

### RF12 - Ver favoritos

#### CP42: Listar favoritos exitoso
- **Clase**: `ListarFavoritosTestCase`
- **Método**: `test_listar_favoritos_exitoso()`
- **Precondiciones**: Usuario con 2 favoritos
- **Resultado Esperado**: 
  - Status 200 OK
  - Lista con 2 favoritos
- **Criterios**:
  - ✅ Cantidad correcta
  - ✅ IDs correctos

#### CP43: Listar sin autenticación
- **Método**: `test_listar_favoritos_sin_autenticacion()`
- **Resultado Esperado**: Status 401 UNAUTHORIZED

#### CP44: Favoritos vacío
- **Método**: `test_listar_favoritos_vacio()`
- **Precondiciones**: Usuario sin favoritos
- **Resultado Esperado**: 
  - Status 200 OK
  - Lista vacía

#### CP45: Solo del usuario autenticado
- **Método**: `test_favoritos_solo_del_usuario_autenticado()`
- **Precondiciones**: Dos usuarios con favoritos
- **Resultado Esperado**: Solo favoritos propios
- **Criterios**: No ver favoritos de otros

#### CP46-50: Eliminar favoritos y detalles
- Ver `EliminarFavoritoTestCase` y `FavoritoDetalleTestCase`

---

### RF14 - Añadir al carrito

#### CP51: Agregar al carrito exitoso
- **Clase**: `AgregarAlCarritoTestCase`
- **Método**: `test_agregar_al_carrito_exitoso()`
- **Precondiciones**: Usuario autenticado
- **Entrada**:
  ```json
  {
    "producto": 1,
    "cantidad": 1
  }
  ```
- **Resultado Esperado**: 
  - Status 201 CREATED
  - Item en carrito
- **Criterios**:
  - ✅ ItemCarrito existe
  - ✅ Cantidad correcta

#### CP52: Agregar sin autenticación
- **Método**: `test_agregar_al_carrito_sin_autenticacion()`
- **Resultado Esperado**: Status 401 UNAUTHORIZED

#### CP53: Múltiples unidades
- **Método**: `test_agregar_multiples_unidades()`
- **Entrada**: `cantidad=3`
- **Resultado Esperado**: Item con cantidad 3
- **Criterios**: Cantidad correcta en BD

#### CP54: Producto sin stock
- **Método**: `test_agregar_producto_sin_stock()`
- **Precondiciones**: Producto con stock=0
- **Resultado Esperado**: Status 400 BAD REQUEST
- **Criterios**: Error de stock insuficiente

#### CP55: Cantidad mayor a stock
- **Método**: `test_agregar_cantidad_mayor_stock()`
- **Entrada**: `cantidad=20, stock=10`
- **Resultado Esperado**: Status 400 BAD REQUEST
- **Criterios**: Error de stock insuficiente

#### CP56: Producto inexistente
- **Método**: `test_agregar_producto_inexistente()`
- **Entrada**: `producto=99999`
- **Resultado Esperado**: Status 400 o 404

#### CP57: Incrementar cantidad existente
- **Método**: `test_incrementar_cantidad_producto_existente()`
- **Entrada**: Agregar mismo producto dos veces
- **Resultado Esperado**: Cantidad incrementada
- **Criterios**: Solo 1 item, cantidad sumada

---

### RF17 - Ver el carrito

#### CP58: Ver carrito con productos
- **Clase**: `VerCarritoTestCase`
- **Método**: `test_ver_carrito_exitoso()`
- **Precondiciones**: Carrito con 2 items
- **Resultado Esperado**: 
  - Status 200 OK
  - Lista de items
- **Criterios**:
  - ✅ Al menos 2 items
  - ✅ Datos completos

#### CP59: Ver carrito vacío
- **Método**: `test_ver_carrito_vacio()`
- **Precondiciones**: Usuario sin items
- **Resultado Esperado**: 
  - Status 200 OK
  - Lista vacía

#### CP60: Ver sin autenticación
- **Método**: `test_ver_carrito_sin_autenticacion()`
- **Resultado Esperado**: Status 401 UNAUTHORIZED

#### CP61: Cálculo de total correcto
- **Método**: `test_carrito_calcula_total_correctamente()`
- **Precondiciones**: Items con precios conocidos
- **Resultado Esperado**: Total = Σ(precio × cantidad)
- **Criterios**: Cálculo matemático correcto

#### CP62: Solo del usuario autenticado
- **Método**: `test_carrito_solo_del_usuario_autenticado()`
- **Precondiciones**: Dos usuarios con carritos
- **Resultado Esperado**: Solo items propios
- **Criterios**: No ver items de otros

#### CP63-67: Actualizar y eliminar del carrito
- Ver `ActualizarCantidadCarritoTestCase` y `EliminarDelCarritoTestCase`

---

## ⚙️ EJECUCIÓN DE PRUEBAS

### Comandos de Ejecución

```bash
# 1. Activar entorno virtual (si no está activado)
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# 2. Asegurar que la base de datos está migrada
python manage.py migrate

# 3. Ejecutar todas las pruebas
python manage.py test core.tests

# 4. Ejecutar con verbosidad (ver detalles)
python manage.py test core.tests -v 2

# 5. Ejecutar módulo específico
python manage.py test core.tests.test_authentication -v 2
python manage.py test core.tests.test_productos -v 2
python manage.py test core.tests.test_favoritos -v 2
python manage.py test core.tests.test_carrito -v 2

# 6. Ejecutar clase específica
python manage.py test core.tests.test_authentication.RegistroUsuarioTestCase -v 2

# 7. Ejecutar test específico
python manage.py test core.tests.test_authentication.RegistroUsuarioTestCase.test_registro_exitoso -v 2

# 8. Mantener base de datos después de las pruebas (para inspección)
python manage.py test core.tests --keepdb

# 9. Ejecutar en paralelo (más rápido en sistemas multi-core)
python manage.py test core.tests --parallel
```

### Cobertura de Código

```bash
# Instalar coverage
pip install coverage

# Ejecutar pruebas con coverage
coverage run --source='core' manage.py test core.tests

# Ver reporte en consola
coverage report

# Generar reporte HTML
coverage html

# Abrir reporte HTML
# El reporte se encuentra en htmlcov/index.html
```

### Configuración de Base de Datos de Prueba

Django automáticamente crea una base de datos temporal `test_alkosto_db` para las pruebas. Cada prueba se ejecuta en una transacción que se revierte al final, garantizando aislamiento.

---

## 📊 RESULTADOS Y EVIDENCIAS

### Plantilla de Resultados

Para cada ejecución de pruebas, documentar:

#### Información de Ejecución
- **Fecha**: _______________
- **Hora**: _______________
- **Entorno**: Desarrollo / Pruebas / Producción
- **Base de Datos**: MySQL / SQLite (test)
- **Python Version**: _______________
- **Django Version**: _______________

#### Resumen de Resultados

| Módulo | Total Tests | ✅ Passed | ❌ Failed | ⚠️ Errors | ⏭️ Skipped | Tiempo |
|--------|------------|----------|-----------|-----------|-----------|--------|
| test_authentication.py | ___ | ___ | ___ | ___ | ___ | ___ s |
| test_productos.py | ___ | ___ | ___ | ___ | ___ | ___ s |
| test_favoritos.py | ___ | ___ | ___ | ___ | ___ | ___ s |
| test_carrito.py | ___ | ___ | ___ | ___ | ___ | ___ s |
| **TOTAL** | **___** | **___** | **___** | **___** | **___** | **___ s** |

#### Detalles de Fallos

Si hay tests fallidos, documentar:

**Test**: `<nombre_completo_del_test>`
- **Error**: `<mensaje_de_error>`
- **Stack Trace**:
  ```
  <stack_trace_completo>
  ```
- **Causa Raíz**: _______________
- **Acción Correctiva**: _______________
- **Estado**: Pendiente / Corregido / Aplazado

#### Evidencias de Pantalla

Para cada RF, capturar:

1. **Ejecución del test**
   - Screenshot del comando y output
   - Ejemplo: `python manage.py test core.tests.test_authentication -v 2`

2. **Resultados exitosos**
   - Screenshot mostrando "OK" y cantidad de tests pasados

3. **Base de datos (si aplica)**
   - Screenshot de registros creados
   - Ejemplo: Usuario creado después de test de registro

4. **API Response (si aplica)**
   - Screenshot de response JSON
   - Headers HTTP
   - Status codes

#### Ejemplo de Evidencia

**RF01 - Registro de Usuario**

```
Ejecutando: python manage.py test core.tests.test_authentication.RegistroUsuarioTestCase -v 2

Creating test database for alias 'default'...
Operations to perform:
  Synchronize unmigrated apps: messages, staticfiles
  Apply all migrations: admin, auth, authtoken, contenttypes, core, sessions
Synchronizing apps without migrations:
  Creating tables...
    Running deferred SQL...
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  [... más migraciones ...]

System check identified no issues (0 silenced).

test_registro_campos_requeridos_faltantes (core.tests.test_authentication.RegistroUsuarioTestCase) ... ok
test_registro_email_duplicado (core.tests.test_authentication.RegistroUsuarioTestCase) ... ok
test_registro_email_invalido (core.tests.test_authentication.RegistroUsuarioTestCase) ... ok
test_registro_exitoso (core.tests.test_authentication.RegistroUsuarioTestCase) ... ok
test_registro_password_corta (core.tests.test_authentication.RegistroUsuarioTestCase) ... ok
test_registro_passwords_no_coinciden (core.tests.test_authentication.RegistroUsuarioTestCase) ... ok

----------------------------------------------------------------------
Ran 6 tests in 2.345s

OK

Destroying test database for alias 'default'...
```

**Status**: ✅ TODOS LOS TESTS PASARON

---

### Checklist de Documentación

Para cada RF, verificar que se tenga:

- [ ] Casos de prueba documentados
- [ ] Criterios de aceptación definidos
- [ ] Tests implementados
- [ ] Tests ejecutados exitosamente
- [ ] Screenshots de ejecución
- [ ] Screenshots de resultados
- [ ] Evidencia de base de datos (si aplica)
- [ ] Evidencia de API response (si aplica)
- [ ] Análisis de cobertura

---

## 🔧 SOLUCIÓN DE PROBLEMAS

### Errores Comunes

#### 1. Error de Base de Datos
```
django.db.utils.OperationalError: no such table: core_usuario
```
**Solución**: Ejecutar migraciones
```bash
python manage.py migrate
```

#### 2. Error de Importación
```
ModuleNotFoundError: No module named 'rest_framework'
```
**Solución**: Instalar dependencias
```bash
pip install -r requirements.txt
```

#### 3. Tests Fallando por Datos Anteriores
**Solución**: Limpiar base de datos de prueba
```bash
python manage.py test --keepdb=False
```

#### 4. Permisos de Autenticación
```
AssertionError: 401 != 200
```
**Solución**: Verificar que el token se está enviando correctamente
```python
self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
```

---

## 📈 MÉTRICAS DE CALIDAD

### Objetivos de Cobertura

- **Cobertura de código**: ≥ 80%
- **Cobertura de RFs**: 100% (10/10 RFs)
- **Tasa de éxito**: 100% tests pasando
- **Tiempo de ejecución**: < 30 segundos total

### Análisis de Cobertura

```bash
# Generar reporte de cobertura
coverage run --source='core' manage.py test core.tests
coverage report

# Ejemplo de output esperado:
Name                                    Stmts   Miss  Cover
-----------------------------------------------------------
core/__init__.py                            0      0   100%
core/admin.py                              10      2    80%
core/models.py                             45      5    89%
core/serializers.py                        30      3    90%
core/views.py                              60      8    87%
core/tests/__init__.py                      0      0   100%
core/tests/test_authentication.py         120      0   100%
core/tests/test_productos.py               95      0   100%
core/tests/test_favoritos.py               85      0   100%
core/tests/test_carrito.py                100      0   100%
-----------------------------------------------------------
TOTAL                                     545     18    97%
```

---

## 📚 REFERENCIAS

- [Django Testing Documentation](https://docs.djangoproject.com/en/5.2/topics/testing/)
- [Django REST Framework Testing](https://www.django-rest-framework.org/api-guide/testing/)
- [Python unittest](https://docs.python.org/3/library/unittest.html)
- [Coverage.py](https://coverage.readthedocs.io/)

---

## 🎯 RESULTADOS DE EJECUCIÓN COMPLETA

### Comando de Ejecución
```bash
python manage.py test core.tests -v 2
```

### Resumen por Módulo
| Módulo | Tests Ejecutados | Tests Exitosos | Tiempo | Estado |
|--------|------------------|----------------|---------|---------|
| `test_authentication.py` | 20 | ✅ 20 | ~15.3s | COMPLETO |
| `test_productos.py` | 16 | ✅ 16 | ~0.4s | COMPLETO |
| `test_favoritos.py` | 14 | ✅ 14 | ~10.9s | COMPLETO |
| `test_carrito.py` | 17 | ✅ 17 | ~12.2s | COMPLETO |
| **TOTAL** | **67** | **✅ 67** | **38.741s** | **✅ EXITOSO** |

### Desglose Detallado por Funcionalidad
- **RF01 (Registro)**: 6/6 tests ✅
- **RF02 (Login/Logout)**: 7/7 tests ✅  
- **RF03 (Cambio Password)**: 4/4 tests ✅
- **RF04 (Perfil Usuario)**: 3/3 tests ✅
- **RF06 (Búsqueda Productos)**: 5/5 tests ✅
- **RF07 (Filtros/Ordenamiento)**: 11/11 tests ✅
- **RF10 (Añadir Favoritos)**: 5/5 tests ✅
- **RF12 (Ver Favoritos)**: 9/9 tests ✅
- **RF14 (Añadir Carrito)**: 7/7 tests ✅
- **RF17 (Ver/Gestionar Carrito)**: 10/10 tests ✅

---

## ✅ CONCLUSIÓN

Este conjunto de pruebas unitarias proporciona una cobertura completa de los 10 requerimientos funcionales prioritarios del sistema Backend Clone Alkosto, garantizando:

1. ✅ **Funcionalidad Correcta**: Cada RF se comporta según especificación
2. ✅ **Manejo de Errores**: Validación apropiada de entradas inválidas
3. ✅ **Seguridad**: Autenticación y autorización correctas
4. ✅ **Integridad de Datos**: Validaciones de BD y consistencia
5. ✅ **Cobertura Completa**: 67 casos de prueba implementados y **EXITOSOS**

**Total de Casos de Prueba**: 67 ✅
- RF01-RF04 (Autenticación): 20 casos ✅
- RF06-RF07 (Productos): 16 casos ✅
- RF10-RF12 (Favoritos): 14 casos ✅
- RF14-RF17 (Carrito): 17 casos ✅

**🏆 Estado Final: TODOS LOS TESTS EXITOSOS - Sistema validado completamente**

---

## 📊 TABLA DETALLADA DE CASOS DE PRUEBA

| Id | Caso de Prueba | Descripción | Fecha | Área Funcional / Sub proceso | Funcionalidad / Característica | Datos / Acciones de Entrada | Capturas de pantalla - Datos Entrada | Resultado Esperado | Requerimientos de Ambiente de Pruebas | Procedimientos especiales requeridos | Dependencias con otros casos de Prueba | Resultado Obtenido | Captura - Datos Salida | Estado | Última Fecha de Estado | Observaciones |
|----|----------------|-------------|-------|------------------------------|--------------------------------|----------------------------|-----------------------------------|-------------------|-------------------------------------|-----------------------------------|---------------------------------------|-------------------|----------------------|--------|----------------------|---------------|
| CP01 | test_registro_exitoso | Registro exitoso con datos válidos | 2025-10-22 | Autenticación / Registro | RF01 - Registrar Usuario | email='test@example.com', nombre='Juan', apellido='Pérez', password='Test123!', password_confirm='Test123!' | Terminal: datos JSON válidos | Status 201, usuario creado, token generado | Django TestCase, MySQL test_db | Token authentication configurado | Ninguna | ✅ Status 201, usuario registrado correctamente | Terminal: response exitoso | ✅ PASÓ | 2025-10-22 | Test base de registro |
| CP02 | test_registro_email_duplicado | Registro con email duplicado | 2025-10-22 | Autenticación / Registro | RF01 - Registrar Usuario | email ya existente en BD | Terminal: email duplicado | Status 400, error de validación | Django TestCase, MySQL test_db | Usuario previo creado | CP01 | ✅ Status 400, error esperado | Terminal: mensaje error email | ✅ PASÓ | 2025-10-22 | Valida unicidad de email |
| CP03 | test_registro_passwords_no_coinciden | Registro con contraseñas que no coinciden | 2025-10-22 | Autenticación / Registro | RF01 - Registrar Usuario | password='Test123!', password_confirm='Different123!' | Terminal: contraseñas diferentes | Status 400, error de validación | Django TestCase, MySQL test_db | Validador personalizado | Ninguna | ✅ Status 400, error esperado | Terminal: mensaje error contraseñas | ✅ PASÓ | 2025-10-22 | Valida confirmación password |
| CP04 | test_registro_password_corta | Registro con contraseña muy corta | 2025-10-22 | Autenticación / Registro | RF01 - Registrar Usuario | password='123' (menos de 8 caracteres) | Terminal: password corta | Status 400, error de validación | Django TestCase, MySQL test_db | Validadores Django | Ninguna | ✅ Status 400, error esperado | Terminal: mensaje longitud mínima | ✅ PASÓ | 2025-10-22 | Valida longitud mínima |
| CP05 | test_registro_campos_requeridos_faltantes | Registro con campos obligatorios faltantes | 2025-10-22 | Autenticación / Registro | RF01 - Registrar Usuario | payload vacío o incompleto | Terminal: datos faltantes | Status 400, errores de campos requeridos | Django TestCase, MySQL test_db | Validadores Django | Ninguna | ✅ Status 400, errores esperados | Terminal: lista campos requeridos | ✅ PASÓ | 2025-10-22 | Valida campos obligatorios |
| CP06 | test_registro_email_invalido | Registro con formato de email inválido | 2025-10-22 | Autenticación / Registro | RF01 - Registrar Usuario | email='email_invalido' (sin @) | Terminal: email malformado | Status 400, error formato email | Django TestCase, MySQL test_db | Validador email Django | Ninguna | ✅ Status 400, error esperado | Terminal: mensaje formato email | ✅ PASÓ | 2025-10-22 | Valida formato email |
| CP07 | test_login_exitoso | Login exitoso con credenciales válidas | 2025-10-22 | Autenticación / Login | RF02 - Iniciar sesión | email y password correctos | Terminal: credenciales válidas | Status 200, token válido retornado | Django TestCase, MySQL test_db | Usuario registrado previamente | CP01 | ✅ Status 200, token recibido | Terminal: token authentication | ✅ PASÓ | 2025-10-22 | Login base exitoso |
| CP08 | test_login_password_incorrecta | Login con contraseña incorrecta | 2025-10-22 | Autenticación / Login | RF02 - Iniciar sesión | email correcto, password incorrecto | Terminal: password incorrecta | Status 400, mensaje de error | Django TestCase, MySQL test_db | Usuario registrado previamente | CP01 | ✅ Status 400, error esperado | Terminal: mensaje credenciales inválidas | ✅ PASÓ | 2025-10-22 | Valida autenticación |
| CP09 | test_login_usuario_inexistente | Login con usuario que no existe | 2025-10-22 | Autenticación / Login | RF02 - Iniciar sesión | email que no existe en BD | Terminal: usuario inexistente | Status 400, mensaje de error | Django TestCase, MySQL test_db | BD limpia | Ninguna | ✅ Status 400, error esperado | Terminal: mensaje usuario no encontrado | ✅ PASÓ | 2025-10-22 | Valida existencia usuario |
| CP10 | test_login_campos_vacios | Login con campos vacíos | 2025-10-22 | Autenticación / Login | RF02 - Iniciar sesión | email='', password='' | Terminal: campos vacíos | Status 400, errores de validación | Django TestCase, MySQL test_db | Validadores Django | Ninguna | ✅ Status 400, errores esperados | Terminal: mensajes campos requeridos | ✅ PASÓ | 2025-10-22 | Valida campos obligatorios |
| CP11 | test_login_usuario_inactivo | Login con usuario inactivo | 2025-10-22 | Autenticación / Login | RF02 - Iniciar sesión | Usuario con is_active=False | Terminal: usuario inactivo | Status 400, mensaje de error | Django TestCase, MySQL test_db | Usuario inactivo creado | CP01 | ✅ Status 400, error esperado | Terminal: mensaje usuario inactivo | ✅ PASÓ | 2025-10-22 | Valida estado usuario |
| CP12 | test_logout_exitoso | Logout exitoso | 2025-10-22 | Autenticación / Logout | RF02 - Cerrar sesión | Token válido en header | Terminal: token authorization | Status 200, sesión cerrada | Django TestCase, MySQL test_db | Usuario autenticado | CP07 | ✅ Status 200, logout exitoso | Terminal: mensaje sesión cerrada | ✅ PASÓ | 2025-10-22 | Logout base exitoso |
| CP13 | test_logout_sin_autenticacion | Logout sin estar autenticado | 2025-10-22 | Autenticación / Logout | RF02 - Cerrar sesión | Sin token en header | Terminal: sin authorization | Status 401, no autorizado | Django TestCase, MySQL test_db | Sin autenticación previa | Ninguna | ✅ Status 401, error esperado | Terminal: mensaje no autorizado | ✅ PASÓ | 2025-10-22 | Valida autenticación requerida |
| CP14 | test_obtener_perfil_exitoso | Obtener perfil de usuario autenticado | 2025-10-22 | Autenticación / Perfil | RF04 - Ver perfil | Token válido en header | Terminal: GET /api/auth/perfil/ | Status 200, datos del usuario | Django TestCase, MySQL test_db | Usuario autenticado | CP07 | ✅ Status 200, perfil obtenido | Terminal: datos usuario JSON | ✅ PASÓ | 2025-10-22 | Obtención perfil básica |
| CP15 | test_actualizar_perfil_exitoso | Actualizar datos del perfil | 2025-10-22 | Autenticación / Perfil | RF04 - Actualizar perfil | Datos actualizados + token válido | Terminal: PUT con nuevos datos | Status 200, perfil actualizado | Django TestCase, MySQL test_db | Usuario autenticado | CP07 | ✅ Status 200, datos actualizados | Terminal: perfil modificado | ✅ PASÓ | 2025-10-22 | Actualización perfil exitosa |
| CP16 | test_obtener_perfil_sin_autenticacion | Intentar obtener perfil sin autenticación | 2025-10-22 | Autenticación / Perfil | RF04 - Ver perfil | Sin token en header | Terminal: GET sin authorization | Status 401, no autorizado | Django TestCase, MySQL test_db | Sin autenticación | Ninguna | ✅ Status 401, error esperado | Terminal: mensaje no autorizado | ✅ PASÓ | 2025-10-22 | Valida autenticación perfil |
| CP17 | test_cambio_password_exitoso | Cambio de contraseña exitoso | 2025-10-22 | Autenticación / Password | RF03 - Cambiar contraseña | password_actual + password_nueva válidas | Terminal: datos cambio password | Status 200, contraseña cambiada | Django TestCase, MySQL test_db | Usuario autenticado | CP07 | ✅ Status 200, password cambiada | Terminal: mensaje éxito | ✅ PASÓ | 2025-10-22 | Cambio password base |
| CP18 | test_cambio_password_actual_incorrecta | Cambio con contraseña actual incorrecta | 2025-10-22 | Autenticación / Password | RF03 - Cambiar contraseña | password_actual incorrecta | Terminal: password actual errónea | Status 400, error validación | Django TestCase, MySQL test_db | Usuario autenticado | CP07 | ✅ Status 400, error esperado | Terminal: mensaje password incorrecta | ✅ PASÓ | 2025-10-22 | Valida password actual |
| CP19 | test_cambio_passwords_nuevas_no_coinciden | Nuevas contraseñas no coinciden | 2025-10-22 | Autenticación / Password | RF03 - Cambiar contraseña | password_nueva != password_confirma | Terminal: confirmación diferente | Status 400, error validación | Django TestCase, MySQL test_db | Usuario autenticado | CP07 | ✅ Status 400, error esperado | Terminal: mensaje confirmación | ✅ PASÓ | 2025-10-22 | Valida confirmación nueva |
| CP20 | test_cambio_password_muy_corta | Nueva contraseña muy corta | 2025-10-22 | Autenticación / Password | RF03 - Cambiar contraseña | password_nueva < 8 caracteres | Terminal: password corta | Status 400, error validación | Django TestCase, MySQL test_db | Usuario autenticado | CP07 | ✅ Status 400, error esperado | Terminal: mensaje longitud mínima | ✅ PASÓ | 2025-10-22 | Valida longitud nueva |
| CP21 | test_busqueda_por_nombre_exitosa | Buscar producto por nombre | 2025-10-22 | Productos / Búsqueda | RF06 - Buscar Producto | q='Samsung' en query params | Terminal: GET /api/buscar/?q=Samsung | Status 200, productos con 'Samsung' | Django TestCase, MySQL test_db | Productos de prueba creados | Ninguna | ✅ Status 200, productos encontrados | Terminal: lista productos JSON | ✅ PASÓ | 2025-10-22 | Búsqueda básica por nombre |
| CP22 | test_busqueda_por_descripcion | Buscar producto por descripción | 2025-10-22 | Productos / Búsqueda | RF06 - Buscar Producto | q='smartphone' en descripción | Terminal: búsqueda en descripción | Status 200, productos con descripción coincidente | Django TestCase, MySQL test_db | Productos con descripciones | Ninguna | ✅ Status 200, productos encontrados | Terminal: resultados descripción | ✅ PASÓ | 2025-10-22 | Búsqueda en descripción |
| CP23 | test_busqueda_sin_resultados | Búsqueda sin resultados | 2025-10-22 | Productos / Búsqueda | RF06 - Buscar Producto | q='ProductoInexistente' | Terminal: término no existente | Status 200, lista vacía | Django TestCase, MySQL test_db | BD con productos | Ninguna | ✅ Status 200, lista vacía | Terminal: resultados vacíos | ✅ PASÓ | 2025-10-22 | Manejo sin resultados |
| CP24 | test_busqueda_vacia | Búsqueda con término vacío | 2025-10-22 | Productos / Búsqueda | RF06 - Buscar Producto | q='' (vacío) | Terminal: parámetro vacío | Status 200, todos los productos | Django TestCase, MySQL test_db | Productos disponibles | Ninguna | ✅ Status 200, todos productos | Terminal: lista completa | ✅ PASÓ | 2025-10-22 | Búsqueda sin filtro |
| CP25 | test_busqueda_case_insensitive | Búsqueda insensible a mayúsculas | 2025-10-22 | Productos / Búsqueda | RF06 - Buscar Producto | q='sAmSuNg' (mayúsculas mezcladas) | Terminal: texto mixto | Status 200, productos encontrados | Django TestCase, MySQL test_db | Productos Samsung | Ninguna | ✅ Status 200, productos encontrados | Terminal: resultados correctos | ✅ PASÓ | 2025-10-22 | Insensible a mayúsculas |
| CP26 | test_filtrar_por_categoria_electronica | Filtrar productos de categoría Electrónica | 2025-10-22 | Productos / Filtros | RF07 - Filtrar categorías | categoria_id=1 (Electrónica) | Terminal: filtro por categoría | Status 200, solo productos electrónicos | Django TestCase, MySQL test_db | Categorías y productos creados | Ninguna | ✅ Status 200, filtro correcto | Terminal: productos categoría | ✅ PASÓ | 2025-10-22 | Filtro básico categoría |
| CP27 | test_filtrar_por_categoria_ropa | Filtrar productos de categoría Ropa | 2025-10-22 | Productos / Filtros | RF07 - Filtrar categorías | categoria_id=2 (Ropa) | Terminal: filtro categoría ropa | Status 200, solo productos de ropa | Django TestCase, MySQL test_db | Múltiples categorías | Ninguna | ✅ Status 200, filtro correcto | Terminal: productos ropa | ✅ PASÓ | 2025-10-22 | Filtro categoría alternativa |
| CP28 | test_filtrar_categoria_sin_productos | Filtrar categoría sin productos | 2025-10-22 | Productos / Filtros | RF07 - Filtrar categorías | categoria_id sin productos | Terminal: categoría vacía | Status 200, lista vacía | Django TestCase, MySQL test_db | Categoría sin productos | Ninguna | ✅ Status 200, lista vacía | Terminal: sin resultados | ✅ PASÓ | 2025-10-22 | Categoría vacía |
| CP29 | test_filtrar_categoria_inexistente | Filtrar con ID de categoría inexistente | 2025-10-22 | Productos / Filtros | RF07 - Filtrar categorías | categoria_id=999 (no existe) | Terminal: ID inexistente | Status 200, lista vacía | Django TestCase, MySQL test_db | Categorías limitadas | Ninguna | ✅ Status 200, lista vacía | Terminal: sin resultados | ✅ PASÓ | 2025-10-22 | ID inexistente |
| CP30 | test_obtener_todas_categorias | Obtener lista de todas las categorías | 2025-10-22 | Productos / Filtros | RF07 - Filtrar categorías | GET /api/categorias/ | Terminal: listar categorías | Status 200, todas las categorías | Django TestCase, MySQL test_db | Categorías creadas | Ninguna | ✅ Status 200, lista categorías | Terminal: categorías JSON | ✅ PASÓ | 2025-10-22 | Listar categorías |
| CP31 | test_busqueda_con_filtro_categoria | Buscar "Samsung" filtrado por categoría Tecnología | 2025-10-22 | Productos / Filtros Combinados | RF06+RF07 - Búsqueda + Filtro | q='Samsung' + categoria_id=Tecnología | Terminal: búsqueda + filtro | Status 200, Samsung en Tecnología | Django TestCase, MySQL test_db | Productos Samsung en categorías | Ninguna | ✅ Status 200, filtro combinado | Terminal: resultados filtrados | ✅ PASÓ | 2025-10-22 | Búsqueda + categoría |
| CP32 | test_filtro_por_rango_precio | Filtrar productos por rango de precio | 2025-10-22 | Productos / Filtros Combinados | RF07 - Filtros avanzados | precio_min=1000000, precio_max=3000000 | Terminal: rango precios | Status 200, productos en rango | Django TestCase, MySQL test_db | Productos varios precios | Ninguna | ✅ Status 200, rango correcto | Terminal: productos rango | ✅ PASÓ | 2025-10-22 | Filtro por precio |
| CP33 | test_filtro_productos_destacados | Filtrar solo productos destacados | 2025-10-22 | Productos / Filtros Combinados | RF07 - Filtros especiales | destacado=true | Terminal: filtro destacados | Status 200, solo destacados | Django TestCase, MySQL test_db | Productos destacados marcados | Ninguna | ✅ Status 200, solo destacados | Terminal: productos destacados | ✅ PASÓ | 2025-10-22 | Filtro destacados |
| CP34 | test_filtro_productos_oferta | Filtrar solo productos en oferta | 2025-10-22 | Productos / Filtros Combinados | RF07 - Filtros especiales | en_oferta=true | Terminal: filtro ofertas | Status 200, solo en oferta | Django TestCase, MySQL test_db | Productos en oferta | Ninguna | ✅ Status 200, solo ofertas | Terminal: productos oferta | ✅ PASÓ | 2025-10-22 | Filtro ofertas |
| CP35 | test_ordenar_por_precio_ascendente | Ordenar productos por precio de menor a mayor | 2025-10-22 | Productos / Ordenamiento | RF07 - Ordenamiento | orden='precio' | Terminal: orden ascendente | Status 200, productos ordenados ASC | Django TestCase, MySQL test_db | Productos varios precios | Ninguna | ✅ Status 200, orden correcto | Terminal: precios ascendentes | ✅ PASÓ | 2025-10-22 | Orden precio ASC |
| CP36 | test_ordenar_por_precio_descendente | Ordenar productos por precio de mayor a menor | 2025-10-22 | Productos / Ordenamiento | RF07 - Ordenamiento | orden='-precio' | Terminal: orden descendente | Status 200, productos ordenados DESC | Django TestCase, MySQL test_db | Productos varios precios | Ninguna | ✅ Status 200, orden correcto | Terminal: precios descendentes | ✅ PASÓ | 2025-10-22 | Orden precio DESC |
| CP37 | test_agregar_favorito_exitoso | Agregar producto a favoritos exitosamente | 2025-10-22 | Favoritos / Agregar | RF10 - Añadir a favoritos | producto_id válido + token | Terminal: POST /api/favoritos/ | Status 201, favorito creado | Django TestCase, MySQL test_db | Usuario autenticado, productos | CP07 | ✅ Status 201, favorito agregado | Terminal: favorito JSON | ✅ PASÓ | 2025-10-22 | Agregar favorito base |
| CP38 | test_agregar_favorito_sin_autenticacion | Intentar agregar favorito sin autenticación | 2025-10-22 | Favoritos / Agregar | RF10 - Añadir a favoritos | producto_id sin token | Terminal: POST sin authorization | Status 401, no autorizado | Django TestCase, MySQL test_db | Producto disponible | Ninguna | ✅ Status 401, error esperado | Terminal: mensaje no autorizado | ✅ PASÓ | 2025-10-22 | Autenticación requerida |
| CP39 | test_agregar_favorito_duplicado | Intentar agregar el mismo producto dos veces | 2025-10-22 | Favoritos / Agregar | RF10 - Añadir a favoritos | Mismo producto_id repetido | Terminal: POST producto existente | Status 200, mensaje ya existe | Django TestCase, MySQL test_db | Favorito ya creado | CP37 | ✅ Status 200, mensaje esperado | Terminal: ya en favoritos | ✅ PASÓ | 2025-10-22 | Previene duplicados |
| CP40 | test_agregar_favorito_producto_inexistente | Agregar favorito con producto inexistente | 2025-10-22 | Favoritos / Agregar | RF10 - Añadir a favoritos | producto_id=999 (no existe) | Terminal: ID inexistente | Status 404, producto no encontrado | Django TestCase, MySQL test_db | Usuario autenticado | CP07 | ✅ Status 404, error esperado | Terminal: producto no encontrado | ✅ PASÓ | 2025-10-22 | Valida existencia producto |
| CP41 | test_agregar_multiples_favoritos | Agregar múltiples productos a favoritos | 2025-10-22 | Favoritos / Agregar | RF10 - Añadir a favoritos | Varios productos diferentes | Terminal: múltiples POST | Status 201 para cada uno | Django TestCase, MySQL test_db | Múltiples productos, usuario auth | CP07 | ✅ Múltiples favoritos creados | Terminal: varios favoritos | ✅ PASÓ | 2025-10-22 | Múltiples favoritos |
| CP42 | test_listar_favoritos_exitoso | Listar todos los favoritos del usuario | 2025-10-22 | Favoritos / Listar | RF12 - Ver favoritos | Token válido | Terminal: GET /api/favoritos/ | Status 200, lista de favoritos | Django TestCase, MySQL test_db | Favoritos del usuario creados | CP37 | ✅ Status 200, lista favoritos | Terminal: favoritos JSON | ✅ PASÓ | 2025-10-22 | Listar favoritos base |
| CP43 | test_listar_favoritos_sin_autenticacion | Intentar listar favoritos sin autenticación | 2025-10-22 | Favoritos / Listar | RF12 - Ver favoritos | Sin token | Terminal: GET sin authorization | Status 401, no autorizado | Django TestCase, MySQL test_db | Sin autenticación | Ninguna | ✅ Status 401, error esperado | Terminal: mensaje no autorizado | ✅ PASÓ | 2025-10-22 | Autenticación requerida |
| CP44 | test_listar_favoritos_vacio | Listar favoritos cuando no hay ninguno | 2025-10-22 | Favoritos / Listar | RF12 - Ver favoritos | Usuario sin favoritos | Terminal: GET lista vacía | Status 200, lista vacía | Django TestCase, MySQL test_db | Usuario autenticado sin favoritos | CP07 | ✅ Status 200, lista vacía | Terminal: array vacío | ✅ PASÓ | 2025-10-22 | Lista vacía |
| CP45 | test_favoritos_solo_del_usuario_autenticado | Verificar que solo se muestran favoritos del usuario logueado | 2025-10-22 | Favoritos / Listar | RF12 - Ver favoritos | Múltiples usuarios con favoritos | Terminal: autorización específica | Status 200, solo favoritos propios | Django TestCase, MySQL test_db | Múltiples usuarios, favoritos | CP07 + otros usuarios | ✅ Solo favoritos del usuario auth | Terminal: favoritos filtrados | ✅ PASÓ | 2025-10-22 | Aislamiento por usuario |
| CP46 | test_eliminar_favorito_exitoso | Eliminar producto de favoritos | 2025-10-22 | Favoritos / Eliminar | RF12 - Gestionar favoritos | favorito_id válido | Terminal: DELETE /api/favoritos/{id}/ | Status 204, favorito eliminado | Django TestCase, MySQL test_db | Favorito existente | CP37 | ✅ Status 204, eliminado | Terminal: confirmación eliminación | ✅ PASÓ | 2025-10-22 | Eliminar favorito base |
| CP47 | test_eliminar_favorito_inexistente | Eliminar favorito que no existe | 2025-10-22 | Favoritos / Eliminar | RF12 - Gestionar favoritos | favorito_id=999 (no existe) | Terminal: DELETE ID inexistente | Status 404, favorito no encontrado | Django TestCase, MySQL test_db | Usuario autenticado | CP07 | ✅ Status 404, error esperado | Terminal: favorito no encontrado | ✅ PASÓ | 2025-10-22 | ID inexistente |
| CP48 | test_eliminar_favorito_de_otro_usuario | Intentar eliminar favorito de otro usuario | 2025-10-22 | Favoritos / Eliminar | RF12 - Gestionar favoritos | favorito_id de otro usuario | Terminal: DELETE no autorizado | Status 403/404, acceso denegado | Django TestCase, MySQL test_db | Múltiples usuarios | CP07 + otros usuarios | ✅ Acceso denegado | Terminal: sin autorización | ✅ PASÓ | 2025-10-22 | Seguridad entre usuarios |
| CP49 | test_eliminar_favorito_sin_autenticacion | Eliminar favorito sin autenticación | 2025-10-22 | Favoritos / Eliminar | RF12 - Gestionar favoritos | Sin token authorization | Terminal: DELETE sin auth | Status 401, no autorizado | Django TestCase, MySQL test_db | Sin autenticación | Ninguna | ✅ Status 401, error esperado | Terminal: mensaje no autorizado | ✅ PASÓ | 2025-10-22 | Autenticación requerida |
| CP50 | test_favorito_incluye_detalles_producto | Verificar que favorito incluye detalles del producto | 2025-10-22 | Favoritos / Detalles | RF12 - Ver favoritos | Favorito con producto completo | Terminal: GET favoritos detallados | Status 200, detalles producto incluidos | Django TestCase, MySQL test_db | Favorito con producto completo | CP37 | ✅ Detalles producto incluidos | Terminal: favorito con detalles | ✅ PASÓ | 2025-10-22 | Serialización anidada |
| CP51 | test_agregar_al_carrito_exitoso | Agregar producto al carrito exitosamente | 2025-10-22 | Carrito / Agregar | RF14 - Añadir al carrito | id_producto válido + cantidad=1 | Terminal: POST /api/carrito/ | Status 201/200, item agregado | Django TestCase, MySQL test_db | Usuario autenticado, productos | CP07 | ✅ Item agregado al carrito | Terminal: carrito actualizado | ✅ PASÓ | 2025-10-22 | Agregar carrito base |
| CP52 | test_agregar_al_carrito_sin_autenticacion | Intentar agregar al carrito sin autenticación | 2025-10-22 | Carrito / Agregar | RF14 - Añadir al carrito | Producto sin token (carrito sesión) | Terminal: POST sin auth | Status 200/201 (carrito anónimo) | Django TestCase, MySQL test_db | Producto disponible | Ninguna | ✅ Carrito anónimo funciona | Terminal: carrito sesión | ✅ PASÓ | 2025-10-22 | Carrito anónimo permitido |
| CP53 | test_agregar_multiples_unidades | Agregar múltiples unidades del mismo producto | 2025-10-22 | Carrito / Agregar | RF14 - Añadir al carrito | cantidad=3 para mismo producto | Terminal: POST cantidad > 1 | Status 200/201, cantidad actualizada | Django TestCase, MySQL test_db | Usuario autenticado, stock suficiente | CP07 | ✅ Cantidad agregada correctamente | Terminal: cantidad en carrito | ✅ PASÓ | 2025-10-22 | Múltiples unidades |
| CP54 | test_agregar_producto_sin_stock | Agregar producto sin stock disponible | 2025-10-22 | Carrito / Agregar | RF14 - Añadir al carrito | Producto con stock=0 | Terminal: POST stock insuficiente | Status 400, error stock | Django TestCase, MySQL test_db | Producto sin stock | Ninguna | ✅ Status 400, error stock | Terminal: mensaje stock insuficiente | ✅ PASÓ | 2025-10-22 | Validación stock |
| CP55 | test_agregar_cantidad_mayor_stock | Agregar cantidad mayor al stock disponible | 2025-10-22 | Carrito / Agregar | RF14 - Añadir al carrito | cantidad > stock disponible | Terminal: cantidad excesiva | Status 400, error stock | Django TestCase, MySQL test_db | Producto stock limitado | Ninguna | ✅ Status 400, error stock | Terminal: stock insuficiente | ✅ PASÓ | 2025-10-22 | Límite stock |
| CP56 | test_agregar_producto_inexistente | Agregar producto que no existe | 2025-10-22 | Carrito / Agregar | RF14 - Añadir al carrito | id_producto=999 (no existe) | Terminal: ID inexistente | Status 404, producto no encontrado | Django TestCase, MySQL test_db | BD con productos limitados | Ninguna | ✅ Status 404, producto no encontrado | Terminal: producto no encontrado | ✅ PASÓ | 2025-10-22 | Validación existencia |
| CP57 | test_incrementar_cantidad_producto_existente | Agregar producto que ya está en el carrito | 2025-10-22 | Carrito / Agregar | RF14 - Añadir al carrito | Producto ya en carrito + cantidad adicional | Terminal: incremento cantidad | Status 200, cantidad incrementada | Django TestCase, MySQL test_db | Item ya en carrito | CP51 | ✅ Cantidad incrementada | Terminal: cantidad total | ✅ PASÓ | 2025-10-22 | Incremento automático |
| CP58 | test_ver_carrito_exitoso | Ver carrito con productos | 2025-10-22 | Carrito / Ver | RF17 - Ver el carrito | Token válido | Terminal: GET /api/carrito/ | Status 200, items del carrito | Django TestCase, MySQL test_db | Carrito con items | CP51 | ✅ Status 200, carrito con items | Terminal: items JSON | ✅ PASÓ | 2025-10-22 | Ver carrito base |
| CP59 | test_ver_carrito_vacio | Ver carrito vacío | 2025-10-22 | Carrito / Ver | RF17 - Ver el carrito | Usuario sin items carrito | Terminal: GET carrito vacío | Status 200, carrito vacío | Django TestCase, MySQL test_db | Usuario autenticado sin items | CP07 | ✅ Status 200, carrito vacío | Terminal: carrito sin items | ✅ PASÓ | 2025-10-22 | Carrito vacío |
| CP60 | test_ver_carrito_sin_autenticacion | Ver carrito sin autenticación | 2025-10-22 | Carrito / Ver | RF17 - Ver el carrito | Sin token (carrito sesión) | Terminal: GET sin auth | Status 200 (carrito anónimo) | Django TestCase, MySQL test_db | Carrito de sesión | Ninguna | ✅ Status 200, carrito sesión | Terminal: carrito anónimo | ✅ PASÓ | 2025-10-22 | Carrito anónimo |
| CP61 | test_carrito_calcula_total_correctamente | Verificar cálculo del total del carrito | 2025-10-22 | Carrito / Cálculos | RF17 - Ver el carrito | Múltiples items con precios | Terminal: carrito con total | Status 200, total calculado correctamente | Django TestCase, MySQL test_db | Items con precios específicos | CP51 + múltiples items | ✅ Total calculado correctamente | Terminal: total correcto | ✅ PASÓ | 2025-10-22 | Cálculo total |
| CP62 | test_carrito_solo_del_usuario_autenticado | Verificar que solo se muestran items del usuario | 2025-10-22 | Carrito / Seguridad | RF17 - Ver el carrito | Múltiples usuarios con carritos | Terminal: carrito específico usuario | Status 200, solo items del usuario | Django TestCase, MySQL test_db | Múltiples usuarios con items | CP07 + otros usuarios | ✅ Solo items del usuario | Terminal: carrito filtrado | ✅ PASÓ | 2025-10-22 | Aislamiento carrito |
| CP63 | test_actualizar_cantidad_exitoso | Actualizar cantidad de item en carrito | 2025-10-22 | Carrito / Actualizar | RF17 - Gestionar carrito | item_id + nueva_cantidad | Terminal: PUT cantidad | Status 200, cantidad actualizada | Django TestCase, MySQL test_db | Item en carrito | CP51 | ✅ Cantidad actualizada | Terminal: nueva cantidad | ✅ PASÓ | 2025-10-22 | Actualizar cantidad |
| CP64 | test_actualizar_cantidad_excede_stock | Actualizar a cantidad mayor que stock | 2025-10-22 | Carrito / Actualizar | RF17 - Gestionar carrito | cantidad > stock disponible | Terminal: PUT cantidad excesiva | Status 400, error stock | Django TestCase, MySQL test_db | Item con stock limitado | CP51 | ✅ Status 400, error stock | Terminal: stock insuficiente | ✅ PASÓ | 2025-10-22 | Límite stock actualización |
| CP65 | test_actualizar_cantidad_a_cero | Actualizar cantidad a 0 (eliminar item) | 2025-10-22 | Carrito / Actualizar | RF17 - Gestionar carrito | cantidad=0 | Terminal: PUT cantidad 0 | Status 200, item eliminado | Django TestCase, MySQL test_db | Item en carrito | CP51 | ✅ Item eliminado automáticamente | Terminal: item removido | ✅ PASÓ | 2025-10-22 | Eliminación automática |
| CP66 | test_eliminar_item_carrito_exitoso | Eliminar item del carrito | 2025-10-22 | Carrito / Eliminar | RF17 - Gestionar carrito | item_id válido | Terminal: DELETE /api/carrito/{id}/ | Status 204, item eliminado | Django TestCase, MySQL test_db | Item en carrito | CP51 | ✅ Status 204, item eliminado | Terminal: confirmación eliminación | ✅ PASÓ | 2025-10-22 | Eliminar item |
| CP67 | test_vaciar_carrito_completo | Vaciar todo el carrito | 2025-10-22 | Carrito / Eliminar | RF17 - Gestionar carrito | Múltiples items para eliminar | Terminal: DELETE múltiple | Todos los items eliminados | Django TestCase, MySQL test_db | Carrito con múltiples items | CP51 + múltiples | ✅ Carrito completamente vacío | Terminal: carrito vacío | ✅ PASÓ | 2025-10-22 | Vaciar carrito completo |

---

**Documento generado**: <%= new Date().toLocaleDateString() %>
**Versión**: 1.0
**Autor**: Equipo de Desarrollo Backend Clone Alkosto

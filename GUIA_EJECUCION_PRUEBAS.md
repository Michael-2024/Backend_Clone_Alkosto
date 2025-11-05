# Guía Rápida para Ejecutar Pruebas Unitarias

## Requisitos Previos
1. Entorno virtual activado
2. Base de datos migrada
3. Dependencias instaladas

## Comandos de Ejecución

### 1. Activar Entorno Virtual
```powershell
cd C:\Users\micha\Desktop\Inge_Soft
.\.venv\Scripts\Activate.ps1
cd Backend_Clone_Alkosto
```

### 2. Ejecutar TODAS las Pruebas
```bash
python manage.py test core.tests -v 2
```

### 3. Ejecutar Pruebas por Módulo

#### Autenticación (RF01-RF04)
```bash
python manage.py test core.tests.test_authentication -v 2
```

#### Productos (RF06-RF07)
```bash
python manage.py test core.tests.test_productos -v 2
```

#### Favoritos (RF10-RF12)
```bash
python manage.py test core.tests.test_favoritos -v 2
```

#### Carrito (RF14-RF17)
```bash
python manage.py test core.tests.test_carrito -v 2
```

### 4. Ejecutar una Clase Específica
```bash
python manage.py test core.tests.test_authentication.RegistroUsuarioTestCase -v 2
```

### 5. Ejecutar un Test Específico
```bash
python manage.py test core.tests.test_authentication.RegistroUsuarioTestCase.test_registro_exitoso -v 2
```

## Opciones Útiles

### Ver más detalles
```bash
python manage.py test core.tests -v 3
```

### Mantener la base de datos de prueba
```bash
python manage.py test core.tests --keepdb
```

### Ejecutar con coverage
```bash
# Instalar coverage
pip install coverage

# Ejecutar con coverage
coverage run --source='core' manage.py test core.tests

# Ver reporte
coverage report

# Generar HTML
coverage html
```

## Notas Importantes

⚠️ **ANTES DE EJECUTAR LAS PRUEBAS**:
- Los tests esperan ciertos endpoints en el backend
- Algunos tests pueden fallar si faltan vistas o serializers
- Django creará automáticamente una base de datos de prueba (test_alkosto_db)
- Cada test se ejecuta en una transacción que se revierte después

## Solución de Problemas Comunes

### Error: No module named 'X'
```bash
pip install -r requirements.txt
```

### Error: No such table
```bash
python manage.py migrate
```

### Tests fallando por URLs
- Verificar que las URLs en core/urls.py coincidan con las esperadas en los tests
- Actualmente esperamos:
  - `/api/auth/registro/`
  - `/api/auth/login/`
  - `/api/auth/logout/`
  - `/api/auth/perfil/`
  - `/api/auth/actualizar-perfil/`
  - `/api/auth/cambiar-password/`
  - `/api/productos/`
  - `/api/categorias/`
  - `/api/buscar/`
  - `/api/favoritos/` (pendiente implementar)
  - `/api/carrito/`

## Próximos Pasos

1. ✅ Modelo Favorito creado y migrado
2. ⏳ Ejecutar pruebas de autenticación
3. ⏳ Corregir errores encontrados
4. ⏳ Implementar endpoints faltantes (favoritos)
5. ⏳ Ejecutar todas las pruebas
6. ⏳ Documentar resultados

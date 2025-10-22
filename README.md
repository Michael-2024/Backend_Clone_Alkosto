🛒 Backend Alkosto - Django REST API
📋 Descripción
Backend completo para una plataforma de e-commerce estilo Alkosto, desarrollado con Django REST Framework. Este proyecto incluye un sistema completo de productos, carrito de compras, usuarios, autenticación y búsquedas avanzadas.

🚀 Características Principales
🔍 Sistema de Productos Avanzado
Catálogo completo con imágenes, precios, stock y categorías
Búsqueda inteligente por nombre, descripción y SKU
Filtros múltiples por categoría, marca, rango de precios, ofertas
Ordenamiento por precio, nombre, más vendidos, mejor calificados
Productos destacados y en oferta
🛒 Carrito de Compras Inteligente
Agregar/eliminar productos con validación de stock
Actualizar cantidades en tiempo real
Carrito persistente (sesión anónima y usuarios registrados)
Migración automática de carrito al iniciar sesión
Cálculo automático de subtotales y totales
👤 Sistema de Usuarios y Autenticación
Registro seguro de nuevos usuarios
Autenticación con tokens JWT
Perfiles de usuario personalizables
Sistema de roles (cliente, empleado, administrador)
Gestión de contraseñas segura
🏪 Funcionalidades de Tienda
Gestión de categorías jerárquicas
Sistema de marcas
Control de inventario y stock
API RESTful completamente documentada
🛠️ Tecnologías Utilizadas
Backend: Django 5.2.7, Django REST Framework 3.15.2
Base de datos: MySQL
Autenticación: JWT (djangorestframework-simplejwt)
CORS: django-cors-headers 4.4.0
Imágenes: Pillow 10.4.0
Cliente MySQL: mysqlclient 2.2.4
📁 Estructura del Proyecto
alkosto_backend/
├── 📁 alkosto_backend/ # Configuración del proyecto
│ ├── settings.py # Configuración principal
│ ├── urls.py # URLs principales
│ └── wsgi.py # Configuración WSGI
├── 📁 productos/ # App principal (todo en uno)
│ ├── models.py # Todos los modelos
│ ├── views.py # Todas las vistas y APIs
│ ├── urls.py # Rutas de la API
│ ├── serializers.py # Serializers para APIs
│ ├── admin.py # Panel de administración
│ └── migrations/ # Migraciones de base de datos
├── manage.py # Script de gestión
├── requirements.txt # Dependencias del proyecto
└── database_setup.sql # Estructura de base de datos
🚀 Instalación y Configuración
Prerrequisitos
Python 3.8 o superior
MySQL 5.7 o superior
pip (gestor de paquetes Python)
1. Clonar el repositorio
git clone https://github.com/tu-usuario/alkosto-backend.git cd alkosto-backend

Crear y activar entorno virtual
Windows
python -m venv venv venv\Scripts\activate

Linux/Mac
python3 -m venv venv source venv/bin/activate

Instalar dependencias pip install -r requirements.txt

Configurar base de datos MySQL

-- Crear base de datos CREATE DATABASE alkosto_db;

-- Opcional: Crear usuario específico CREATE USER 'alkosto_user'@'localhost' IDENTIFIED BY 'tu_password'; GRANT ALL PRIVILEGES ON alkosto_db.* TO 'alkosto_user'@'localhost'; FLUSH PRIVILEGES;

Configurar variables de entorno Crear archivo .env en la raíz del proyecto:
env DB_NAME=alkosto_db DB_USER=root DB_PASSWORD=tu_password_mysql DB_HOST=localhost DB_PORT=3306 SECRET_KEY=tu_django_secret_key DEBUG=True

Aplicar migraciones bash python manage.py makemigrations python manage.py migrate

Crear superusuario bash python manage.py createsuperuser Sigue las instrucciones para crear el usuario administrador.

Ejecutar servidor de desarrollo bash python manage.py runserver El servidor estará disponible en: http://localhost:8000

📚 Documentación de la API

🔐 Autenticación

Registro de Usuario http POST /api/auth/registro/ Content-Type: application/json

{ "nombre": "Juan", "apellido": "Pérez", "email": "juan@ejemplo.com", "password": "password123", "password_confirm": "password123", "telefono": "3001234567" }

Iniciar Sesión http POST /api/auth/login/ Content-Type: application/json

{ "email": "juan@ejemplo.com", "password": "password123" }

Ver Perfil (Requiere autenticación) http GET /api/auth/perfil/ Authorization: Token tu_token_jwt

Actualizar Perfil (Requiere autenticación) http PUT /api/auth/actualizar-perfil/ Authorization: Token tu_token_jwt Content-Type: application/json

{ "nombre": "Carlos", "apellido": "Gómez", "telefono": "3109876543" }

Cambiar Contraseña (Requiere autenticación) http POST /api/auth/cambiar-password/ Authorization: Token tu_token_jwt Content-Type: application/json

{ "password_actual": "password123", "nuevo_password": "nuevaPassword456", "confirmar_password": "nuevaPassword456" }

📦 Productos

Listar Todos los Productos http GET /api/productos/

Buscar Productos http GET /api/productos/?search=samsung GET /api/productos/?categoria=5&marca=1 GET /api/productos/?precio_min=100000&precio_max=3000000 GET /api/productos/?orden=precio_asc

Productos Destacados http GET /api/destacados/

Productos en Oferta http GET /api/ofertas/

Búsqueda Avanzada http GET /api/buscar/?q=iphone&categoria=5&orden=precio_desc

🛒 Carrito de Compras

Ver Carrito http GET /api/carrito/

Agregar Producto al Carrito http POST /api/carrito/ Content-Type: application/json

{ "id_producto": 1, "cantidad": 2 }

Actualizar Cantidad http PATCH /api/carrito/1/ # Donde 1 es el id_item Content-Type: application/json

{ "cantidad": 3 }

Eliminar Item del Carrito http DELETE /api/carrito/1/ # Donde 1 es el id_item Vaciar Carrito http DELETE /api/carrito/vaciar/

🏷️ Catálogo

Listar Categorías http GET /api/categorias/

Listar Marcas http GET /api/marcas/

Productos por Categoría http GET /api/categoria/tecnologia/

🗃️ Modelos de Base de Datos

Usuario Información personal y autenticación

Roles: cliente, empleado, administrador

Historial de accesos y actividad

Producto Información completa del producto

Precios, stock, categorías, marcas

Imágenes y especificaciones técnicas

Control de inventario

Carrito Gestión de compras del usuario

Items con cantidades y precios actualizados

Persistencia por sesión y usuario

Categoría Organización jerárquica de productos

Slug para URLs amigables

Imágenes y descripción

🔧 Configuración de Desarrollo Variables importantes en settings.py python DEBUG = True ALLOWED_HOSTS = ['localhost', '127.0.0.1'] DATABASES = { 'default': { 'ENGINE': 'django.db.backends.mysql', 'NAME': 'alkosto_db', 'USER': 'root', 'PASSWORD': 'tu_password', 'HOST': 'localhost', 'PORT': '3306', } } AUTH_USER_MODEL = 'productos.Usuario' Configuración CORS para desarrollo python CORS_ALLOW_ALL_ORIGINS = True CORS_ALLOW_CREDENTIALS = True 🧪 Testing Ejecutar tests del proyecto:

bash python manage.py test productos 📊 Estado del Proyecto ✅ Completado Sistema completo de productos y catálogo

Carrito de compras con todas las funcionalidades

Búsqueda y filtros avanzados

Sistema de autenticación y usuarios

APIs RESTful documentadas

Panel de administración Django

🚧 Próximas Características Sistema de pedidos y checkout

Reseñas y calificaciones de productos

Sistema de cupones y descuentos

Wishlist/favoritos

Historial de compras

Notificaciones por email

👥 Contribución Las contribuciones son bienvenidas. Para contribuir:

Haz fork del proyecto

Crea una rama para tu feature (git checkout -b feature/AmazingFeature)

Commit tus cambios (git commit -m 'Add AmazingFeature')

Push a la rama (git push origin feature/AmazingFeature)

Abre un Pull Request

📝 Licencia Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.

👨‍💻 Autor Tu Nombre - GitHub

🙏 Agradecimientos Equipo de Django por el excelente framework

Django REST Framework por las herramientas de API

Comunidad de código abierto

🔗 Enlaces Rápidos Panel de Administración: http://localhost:8000/admin/

API Root: http://localhost:8000/api/

Documentación API: http://localhost:8000/api/docs/ (pendiente)

Backend_Clone_Alkosto/alkosto_backend/README.md at main · Michael-2024/Backend_Clone_Alkosto

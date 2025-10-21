from django.core.management.base import BaseCommand
from django.utils.text import slugify
from core.models import Usuario, Categoria, Marca, Producto, ImagenProducto
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Pobla la base de datos con datos realistas tipo Alkosto'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('=== POBLACIÓN DE BASE DE DATOS ALKOSTO ===\n'))

        # Limpiar datos existentes (opcional)
        respuesta = input('¿Deseas limpiar los datos existentes? (s/n): ')
        if respuesta.lower() == 's':
            self.stdout.write('Limpiando datos...')
            ImagenProducto.objects.all().delete()
            Producto.objects.all().delete()
            Marca.objects.all().delete()
            Categoria.objects.all().delete()
            Usuario.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.SUCCESS('✓ Datos limpiados\n'))

        # 1. Crear usuarios
        # self.stdout.write('Creando usuarios...')
        # usuarios = self.crear_usuarios()
        # self.stdout.write(self.style.SUCCESS(f'✓ {len(usuarios)} usuarios creados\n'))

        # 2. Crear categorías
        self.stdout.write('Creando categorías...')
        categorias = self.crear_categorias()
        self.stdout.write(self.style.SUCCESS(f'✓ {len(categorias)} categorías creadas\n'))

        # 3. Crear marcas
        self.stdout.write('Creando marcas...')
        marcas = self.crear_marcas()
        self.stdout.write(self.style.SUCCESS(f'✓ {len(marcas)} marcas creadas\n'))

        # 4. Crear productos
        self.stdout.write('Creando productos...')
        productos = self.crear_productos(categorias, marcas)
        self.stdout.write(self.style.SUCCESS(f'✓ {len(productos)} productos creados\n'))

        self.mostrar_resumen()

    def mostrar_resumen(self):
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('¡BASE DE DATOS POBLADA EXITOSAMENTE!'))
        self.stdout.write(self.style.SUCCESS('='*60 + '\n'))
        
        self.stdout.write('📊 RESUMEN:')
        self.stdout.write(f'  • {Usuario.objects.count()} usuarios')
        self.stdout.write(f'  • {Categoria.objects.count()} categorías')
        self.stdout.write(f'  • {Marca.objects.count()} marcas')
        self.stdout.write(f'  • {Producto.objects.count()} productos')
        self.stdout.write(f'  • {Producto.objects.filter(destacado=True).count()} productos destacados')
        self.stdout.write(f'  • {Producto.objects.filter(en_oferta=True).count()} productos en oferta\n')
        
        self.stdout.write('👥 USUARIOS DE PRUEBA:')
        self.stdout.write('  🔐 Admin:    admin@alkosto.com / admin123')
        self.stdout.write('  👤 Cliente:  cliente@test.com / cliente123')
        self.stdout.write('  💼 Empleado: empleado@alkosto.com / empleado123\n')
        
        self.stdout.write('🌐 ENDPOINTS DISPONIBLES:')
        self.stdout.write('  • http://localhost:8000/admin/')
        self.stdout.write('  • http://localhost:8000/api/productos/')
        self.stdout.write('  • http://localhost:8000/api/categorias/')
        self.stdout.write(self.style.SUCCESS('\n' + '='*60 + '\n'))

    def crear_usuarios(self):
        usuarios = []
        
        # Admin
        if not Usuario.objects.filter(email='admin@alkosto.com').exists():
            admin = Usuario.objects.create_superuser(
                email='admin@alkosto.com',
                password='admin123',
                nombre='Administrador',
                apellido='Sistema',
                telefono='6017468001',
                rol='admin'
            )
            usuarios.append(admin)

        # Clientes
        clientes_data = [
            ('cliente@test.com', 'cliente123', 'Juan', 'Pérez', '3109876543'),
            ('maria.gomez@email.com', 'test123', 'María', 'Gómez', '3157654321'),
            ('carlos.ruiz@email.com', 'test123', 'Carlos', 'Ruiz', '3201234567'),
            ('ana.martinez@email.com', 'test123', 'Ana', 'Martínez', '3158765432'),
            ('luis.garcia@email.com', 'test123', 'Luis', 'García', '3209876543'),
        ]

        for email, password, nombre, apellido, telefono in clientes_data:
            if not Usuario.objects.filter(email=email).exists():
                usuario = Usuario.objects.create_user(
                    email=email,
                    password=password,
                    nombre=nombre,
                    apellido=apellido,
                    telefono=telefono,
                    rol='cliente'
                )
                usuarios.append(usuario)

        # Empleado
        if not Usuario.objects.filter(email='empleado@alkosto.com').exists():
            empleado = Usuario.objects.create_user(
                email='empleado@alkosto.com',
                password='empleado123',
                nombre='María',
                apellido='Rodríguez',
                telefono='6014073033',
                rol='empleado',
                is_staff=True
            )
            usuarios.append(empleado)

        return usuarios

    def crear_categorias(self):
        """Crea categorías basadas en Alkosto con slugs únicos"""
        categorias_estructura = {
            'Celulares': ['Smartphones', 'Celulares Básicos', 'Accesorios Celulares', 'Cargadores', 'Cables', 'Audífonos'],
            'Computadores': ['Portátiles', 'Escritorio', 'All in One', 'Gaming', 'Accesorios PC', 'Impresoras'],
            'Electrodomésticos': ['Neveras', 'Lavadoras', 'Estufas', 'Microondas', 'Licuadoras', 'Cafeteras', 'Aspiradoras'],
            'TV': ['Smart TV', 'TV LED', 'TV OLED', 'TV QLED', 'Soportes TV'],
            'Audio': ['Parlantes', 'Audífonos', 'Barras de Sonido', 'Equipos de Sonido', 'Parlantes Bluetooth'],
            'Videojuegos': ['PlayStation', 'Xbox', 'Nintendo', 'Controles', 'Juegos', 'Accesorios Gaming'],
            'Cámaras': ['Cámaras Digitales', 'Cámaras Profesionales', 'Cámaras Seguridad', 'Drones'],
            'Smartwatch': ['Apple Watch', 'Samsung Watch', 'Xiaomi Band', 'Smartband'],
            'Hogar': ['Muebles', 'Colchones', 'Almohadas', 'Decoración', 'Organización'],
            'Deportes': ['Bicicletas', 'Fitness', 'Ropa Deportiva', 'Pesas', 'Máquinas Ejercicio'],
            'Juguetes': ['Muñecas', 'Carros', 'Juegos de Mesa', 'LEGO', 'Peluches'],
        }

        categorias = []
        orden = 0
        
        for cat_nombre, subcategorias in categorias_estructura.items():
            # Crear categoría padre
            cat_padre, created = Categoria.objects.get_or_create(
                slug=slugify(cat_nombre),
                defaults={
                    'nombre': cat_nombre,
                    'descripcion': f'Productos de {cat_nombre}',
                    'activa': True,
                    'orden_display': orden
                }
            )
            categorias.append(cat_padre)
            orden += 1

            # Crear subcategorías
            sub_orden = 0
            for sub_nombre in subcategorias:
                slug_sub = slugify(f'{cat_nombre}-{sub_nombre}')
                sub, created = Categoria.objects.get_or_create(
                    slug=slug_sub,
                    defaults={
                        'nombre': sub_nombre,
                        'descripcion': f'{sub_nombre} en {cat_nombre}',
                        'id_categoria_padre': cat_padre,
                        'activa': True,
                        'orden_display': sub_orden
                    }
                )
                categorias.append(sub)
                sub_orden += 1

        return categorias

    def crear_marcas(self):
        """Crea marcas reales"""
        marcas_data = [
            ('Samsung', 'Innovación tecnológica líder', 'https://www.samsung.com'),
            ('Apple', 'Diseño y tecnología premium', 'https://www.apple.com'),
            ('Xiaomi', 'Tecnología inteligente accesible', 'https://www.mi.com'),
            ('Huawei', 'Conectando el mundo', 'https://www.huawei.com'),
            ('Motorola', 'Hello Moto', 'https://www.motorola.com'),
            ('HP', 'Computadores y tecnología', 'https://www.hp.com'),
            ('Lenovo', 'For those who do', 'https://www.lenovo.com'),
            ('Dell', 'Tecnología empresarial', 'https://www.dell.com'),
            ('Asus', 'In search of incredible', 'https://www.asus.com'),
            ('LG', 'Life is Good', 'https://www.lg.com'),
            ('Whirlpool', 'Every day, care', 'https://www.whirlpool.com'),
            ('Haceb', 'Marca colombiana', 'https://www.haceb.com'),
            ('Electrolux', 'Shape living for the better', 'https://www.electrolux.com'),
            ('Oster', 'Calidad desde 1924', 'https://www.oster.com'),
            ('Sony', 'Entretenimiento sin límites', 'https://www.sony.com'),
            ('TCL', 'Creative life', 'https://www.tcl.com'),
            ('Kalley', 'Tecnología para todos', 'https://www.kalley.com.co'),
            ('JBL', 'Audio profesional', 'https://www.jbl.com'),
            ('PlayStation', 'Play has no limits', 'https://www.playstation.com'),
            ('Xbox', 'Power your dreams', 'https://www.xbox.com'),
            ('Nintendo', 'Play Nintendo', 'https://www.nintendo.com'),
            ('Nike', 'Just do it', 'https://www.nike.com'),
            ('Adidas', 'Impossible is nothing', 'https://www.adidas.com'),
            ('GW', 'Bicicletas colombianas', 'https://www.gw.com.co'),
        ]

        marcas = []
        for nombre, descripcion, sitio_web in marcas_data:
            marca, created = Marca.objects.get_or_create(
                nombre=nombre,
                defaults={
                    'descripcion': descripcion,
                    'sitio_web': sitio_web,
                    'activa': True
                }
            )
            marcas.append(marca)

        return marcas

    def generar_sku(self, nombre, categoria):
        """Genera un SKU único basado en el nombre y categoría"""
        palabras = nombre.split()[:3]
        prefijo = ''.join([p[:3].upper() for p in palabras])
        sufijo = str(random.randint(1000, 9999))
        return f'{prefijo}-{sufijo}'

    def crear_productos(self, categorias, marcas):
        """Crea productos realistas"""
        
        productos_data = [
            # CELULARES
            {
                'nombre': 'Celular SAMSUNG Galaxy A54 5G 256GB',
                'descripcion': 'Pantalla AMOLED 6.4", Cámara 50MP, Batería 5000mAh, Procesador Exynos 1380, 5G',
                'descripcion_corta': 'Galaxy A54 5G con cámara 50MP y pantalla AMOLED',
                'precio': Decimal('1699900'),
                'categoria': 'Smartphones',
                'marca': 'Samsung',
                'stock': 45,
                'destacado': True,
                'descuento': Decimal('15'),
                'color': 'Negro',
                'garantia': 12
            },
            {
                'nombre': 'Celular XIAOMI Redmi Note 13 Pro 256GB',
                'descripcion': 'Pantalla AMOLED 6.67" 120Hz, Cámara 200MP, Carga rápida 67W, Android 13',
                'descripcion_corta': 'Redmi Note 13 Pro con cámara 200MP',
                'precio': Decimal('1399900'),
                'categoria': 'Smartphones',
                'marca': 'Xiaomi',
                'stock': 60,
                'destacado': True,
                'descuento': Decimal('20'),
                'color': 'Azul',
                'garantia': 12
            },
            {
                'nombre': 'iPhone 14 128GB',
                'descripcion': 'Chip A15 Bionic, Cámara dual 12MP, Pantalla Super Retina XDR 6.1", iOS 17',
                'descripcion_corta': 'iPhone 14 con chip A15 Bionic',
                'precio': Decimal('3999900'),
                'categoria': 'Smartphones',
                'marca': 'Apple',
                'stock': 30,
                'destacado': True,
                'descuento': Decimal('10'),
                'color': 'Midnight',
                'garantia': 12
            },
            {
                'nombre': 'Celular MOTOROLA Moto G84 256GB',
                'descripcion': 'Pantalla OLED 6.5" 120Hz, Cámara 50MP, Batería 5000mAh, Android 13',
                'descripcion_corta': 'Moto G84 con pantalla OLED',
                'precio': Decimal('999900'),
                'categoria': 'Smartphones',
                'marca': 'Motorola',
                'stock': 50,
                'destacado': False,
                'descuento': Decimal('25'),
                'color': 'Verde',
                'garantia': 12
            },
            
            # COMPUTADORES
            {
                'nombre': 'Portátil HP 15.6" Intel Core i5 12va Gen',
                'descripcion': '8GB RAM, 512GB SSD, Intel Core i5-1235U, Windows 11 Home, Pantalla Full HD',
                'descripcion_corta': 'HP i5 12va Gen con 512GB SSD',
                'precio': Decimal('2199900'),
                'categoria': 'Portátiles',
                'marca': 'HP',
                'stock': 25,
                'destacado': True,
                'descuento': Decimal('12'),
                'color': 'Plata',
                'garantia': 12
            },
            {
                'nombre': 'Portátil LENOVO IdeaPad 3 15.6" AMD Ryzen 5',
                'descripcion': '16GB RAM, 512GB SSD, AMD Ryzen 5 5500U, Windows 11 Home, Pantalla Full HD',
                'descripcion_corta': 'Lenovo Ryzen 5 con 16GB RAM',
                'precio': Decimal('2499900'),
                'categoria': 'Portátiles',
                'marca': 'Lenovo',
                'stock': 20,
                'destacado': True,
                'descuento': Decimal('15'),
                'color': 'Gris',
                'garantia': 12
            },
            {
                'nombre': 'MacBook Air 13" M2 256GB',
                'descripcion': 'Chip M2, 8GB RAM, Pantalla Liquid Retina 13.6", macOS Sonoma',
                'descripcion_corta': 'MacBook Air con chip M2',
                'precio': Decimal('5499900'),
                'categoria': 'Portátiles',
                'marca': 'Apple',
                'stock': 12,
                'destacado': True,
                'descuento': Decimal('8'),
                'color': 'Space Gray',
                'garantia': 12
            },
            {
                'nombre': 'Portátil Gaming ASUS ROG 15.6" RTX 4050',
                'descripcion': 'Intel Core i7, 16GB RAM, 512GB SSD, NVIDIA RTX 4050 6GB, 144Hz',
                'descripcion_corta': 'ASUS ROG Gaming con RTX 4050',
                'precio': Decimal('4999900'),
                'categoria': 'Gaming',
                'marca': 'Asus',
                'stock': 8,
                'destacado': True,
                'descuento': Decimal('10'),
                'color': 'Negro',
                'garantia': 24
            },
            
            # ELECTRODOMÉSTICOS
            {
                'nombre': 'Nevera SAMSUNG 350L No Frost Twin Cooling',
                'descripcion': 'Tecnología No Frost, Twin Cooling Plus, Dispensador agua, Eficiencia A+',
                'descripcion_corta': 'Nevera Samsung 350L No Frost',
                'precio': Decimal('1899900'),
                'categoria': 'Neveras',
                'marca': 'Samsung',
                'stock': 15,
                'destacado': True,
                'descuento': Decimal('18'),
                'color': 'Plateado',
                'garantia': 12,
                'peso': Decimal('65.5'),
                'dimensiones': '178x60x65 cm'
            },
            {
                'nombre': 'Nevera LG 400L Inverter Linear',
                'descripcion': 'Compresor Inverter Linear, Door Cooling+, Multi Air Flow, Smart Diagnosis',
                'descripcion_corta': 'Nevera LG 400L Inverter',
                'precio': Decimal('2299900'),
                'categoria': 'Neveras',
                'marca': 'LG',
                'stock': 12,
                'destacado': True,
                'descuento': Decimal('15'),
                'color': 'Acero',
                'garantia': 12,
                'peso': Decimal('72.0'),
                'dimensiones': '185x68x70 cm'
            },
            {
                'nombre': 'Lavadora WHIRLPOOL 18Kg Carga Superior',
                'descripcion': 'Carga superior 18kg, 12 programas, Tecnología 6th Sense, Bajo consumo',
                'descripcion_corta': 'Lavadora Whirlpool 18Kg',
                'precio': Decimal('1299900'),
                'categoria': 'Lavadoras',
                'marca': 'Whirlpool',
                'stock': 20,
                'destacado': True,
                'descuento': Decimal('20'),
                'color': 'Blanco',
                'garantia': 12,
                'peso': Decimal('45.0')
            },
            {
                'nombre': 'Lavadora SAMSUNG 15Kg Inverter Eco Bubble',
                'descripcion': 'Tecnología Eco Bubble, Digital Inverter, 14 programas, Vapor',
                'descripcion_corta': 'Lavadora Samsung 15Kg Eco Bubble',
                'precio': Decimal('1799900'),
                'categoria': 'Lavadoras',
                'marca': 'Samsung',
                'stock': 18,
                'destacado': True,
                'descuento': Decimal('22'),
                'color': 'Blanco',
                'garantia': 12
            },
            {
                'nombre': 'Microondas HACEB 0.7 pies 700W',
                'descripcion': '0.7 pies cúbicos, 700W, 6 niveles potencia, Descongelamiento automático',
                'descripcion_corta': 'Microondas Haceb 0.7 pies',
                'precio': Decimal('289900'),
                'categoria': 'Microondas',
                'marca': 'Haceb',
                'stock': 40,
                'destacado': False,
                'descuento': Decimal('15'),
                'color': 'Negro',
                'garantia': 12
            },
            {
                'nombre': 'Licuadora OSTER 3 Velocidades Vaso Vidrio',
                'descripcion': 'Vaso vidrio 1.5L, 3 velocidades, Cuchillas reversibles All Metal Drive',
                'descripcion_corta': 'Licuadora Oster 3 velocidades',
                'precio': Decimal('179900'),
                'categoria': 'Licuadoras',
                'marca': 'Oster',
                'stock': 50,
                'destacado': False,
                'descuento': Decimal('10'),
                'color': 'Rojo',
                'garantia': 12
            },
            
            # TELEVISORES
            {
                'nombre': 'TV SAMSUNG 55" QLED 4K Q60C',
                'descripcion': 'QLED 4K, Procesador Quantum Lite, HDR10+, Tizen OS, Motion Xcelerator',
                'descripcion_corta': 'Samsung QLED 55" 4K',
                'precio': Decimal('2799900'),
                'categoria': 'Smart TV',
                'marca': 'Samsung',
                'stock': 20,
                'destacado': True,
                'descuento': Decimal('25'),
                'talla': '55 pulgadas',
                'garantia': 12
            },
            {
                'nombre': 'TV LG 65" OLED evo C3 4K',
                'descripcion': 'OLED evo, Procesador α9 Gen6, Dolby Vision IQ, webOS 23, HDMI 2.1',
                'descripcion_corta': 'LG OLED 65" 4K',
                'precio': Decimal('6499900'),
                'categoria': 'TV OLED',
                'marca': 'LG',
                'stock': 8,
                'destacado': True,
                'descuento': Decimal('15'),
                'talla': '65 pulgadas',
                'garantia': 12
            },
            {
                'nombre': 'TV TCL 50" LED UHD 4K Android TV',
                'descripcion': '4K Ultra HD, Android TV, HDR10, Dolby Audio, Google Assistant',
                'descripcion_corta': 'TCL 50" 4K Android',
                'precio': Decimal('1299900'),
                'categoria': 'Smart TV',
                'marca': 'TCL',
                'stock': 35,
                'destacado': True,
                'descuento': Decimal('30'),
                'talla': '50 pulgadas',
                'garantia': 12
            },
            {
                'nombre': 'TV KALLEY 43" Full HD Smart TV',
                'descripcion': 'Full HD 1080p, Smart TV, WiFi, 2 HDMI, 1 USB, Netflix, YouTube',
                'descripcion_corta': 'Kalley 43" Full HD Smart',
                'precio': Decimal('799900'),
                'categoria': 'Smart TV',
                'marca': 'Kalley',
                'stock': 45,
                'destacado': False,
                'descuento': Decimal('20'),
                'talla': '43 pulgadas',
                'garantia': 12
            },
            
            # AUDIO
            {
                'nombre': 'Parlante JBL Charge 5 Bluetooth',
                'descripcion': 'Bluetooth 5.1, Resistente agua IP67, 20 horas batería, PartyBoost',
                'descripcion_corta': 'JBL Charge 5 Bluetooth',
                'precio': Decimal('549900'),
                'categoria': 'Parlantes Bluetooth',
                'marca': 'JBL',
                'stock': 30,
                'destacado': True,
                'descuento': Decimal('18'),
                'color': 'Negro',
                'garantia': 12
            },
            {
                'nombre': 'Audífonos SONY WH-1000XM5 Cancelación Ruido',
                'descripcion': 'ANC Premium, 30hrs batería, Hi-Res Audio, Multipunto, Llamadas HD',
                'descripcion_corta': 'Sony WH-1000XM5 ANC',
                'precio': Decimal('1499900'),
                'categoria': 'Audífonos',
                'marca': 'Sony',
                'stock': 15,
                'destacado': True,
                'descuento': Decimal('12'),
                'color': 'Negro',
                'garantia': 12
            },
            {
                'nombre': 'Barra de Sonido SAMSUNG HW-Q600C 3.1.2Ch',
                'descripcion': 'Dolby Atmos, DTS:X, Subwoofer inalámbrico, Q-Symphony, 360W',
                'descripcion_corta': 'Samsung Soundbar Q600C',
                'precio': Decimal('1299900'),
                'categoria': 'Barras de Sonido',
                'marca': 'Samsung',
                'stock': 12,
                'destacado': True,
                'descuento': Decimal('20'),
                'color': 'Negro',
                'garantia': 12
            },
            
            # SMARTWATCH
            {
                'nombre': 'Apple Watch Series 9 GPS 41mm',
                'descripcion': 'Pantalla Always-On, S9 SiP, watchOS 10, Detección accidentes, ECG',
                'descripcion_corta': 'Apple Watch Series 9 GPS',
                'precio': Decimal('2199900'),
                'categoria': 'Apple Watch',
                'marca': 'Apple',
                'stock': 15,
                'destacado': True,
                'descuento': Decimal('8'),
                'talla': '41mm',
                'garantia': 12
            },
            {
                'nombre': 'SAMSUNG Galaxy Watch6 44mm',
                'descripcion': 'Wear OS, Análisis sueño avanzado, Monitor frecuencia, GPS, Batería 40hrs',
                'descripcion_corta': 'Galaxy Watch6 44mm',
                'precio': Decimal('1399900'),
                'categoria': 'Samsung Watch',
                'marca': 'Samsung',
                'stock': 20,
                'destacado': True,
                'descuento': Decimal('15'),
                'talla': '44mm',
                'garantia': 12
            },
            {
                'nombre': 'Xiaomi Smart Band 8',
                'descripcion': 'Pantalla AMOLED 1.62", 150 modos deporte, 16 días batería, 5ATM',
                'descripcion_corta': 'Xiaomi Band 8',
                'precio': Decimal('199900'),
                'categoria': 'Xiaomi Band',
                'marca': 'Xiaomi',
                'stock': 60,
                'destacado': True,
                'descuento': Decimal('25'),
                'garantia': 12
            },
            
            # GAMING
            {
                'nombre': 'PlayStation 5 Slim 1TB',
                'descripcion': 'PS5 Slim, 1TB SSD, Ray Tracing, 4K 120Hz, Control DualSense incluido',
                'descripcion_corta': 'PS5 Slim 1TB',
                'precio': Decimal('2999900'),
                'categoria': 'PlayStation',
                'marca': 'PlayStation',
                'stock': 10,
                'destacado': True,
                'descuento': Decimal('5'),
                'color': 'Blanco',
                'garantia': 12
            },
            {
                'nombre': 'Xbox Series S 512GB',
                'descripcion': 'Next-Gen Gaming, 512GB SSD, 1440p 120fps, Game Pass Ready',
                'descripcion_corta': 'Xbox Series S 512GB',
                'precio': Decimal('1499900'),
                'categoria': 'Xbox',
                'marca': 'Xbox',
                'stock': 15,
                'destacado': True,
                'descuento': Decimal('10'),
                'color': 'Blanco',
                'garantia': 12
            },
            {
                'nombre': 'Nintendo Switch OLED',
                'descripcion': 'Pantalla OLED 7", 64GB, Dock mejorado, Audio envolvente',
                'descripcion_corta': 'Switch OLED',
                'precio': Decimal('1699900'),
                'categoria': 'Nintendo',
                'marca': 'Nintendo',
                'stock': 12,
                'destacado': True,
                'descuento': Decimal('8'),
                'color': 'Blanco',
                'garantia': 12
            },
            
            # DEPORTES
            {
                'nombre': 'Bicicleta Montaña GW Alligator Rin 29"',
                'descripcion': 'Aro 29", Suspensión delantera, 21 velocidades Shimano, Frenos disco',
                'descripcion_corta': 'Bicicleta MTB GW Rin 29',
                'precio': Decimal('1299900'),
                'categoria': 'Bicicletas',
                'marca': 'GW',
                'stock': 8,
                'destacado': False,
                'descuento': Decimal('15'),
                'talla': 'M',
                'garantia': 6
            },
        ]

        productos = []
        for prod_data in productos_data:
            try:
                # Buscar categoría
                categoria = Categoria.objects.get(nombre=prod_data['categoria'])
                # Buscar marca
                marca = Marca.objects.get(nombre=prod_data['marca'])
                
                # Generar SKU único
                sku = self.generar_sku(prod_data['nombre'], prod_data['categoria'])
                
                # Calcular precio original si hay descuento
                precio = prod_data['precio']
                descuento = prod_data.get('descuento', Decimal('0'))
                precio_original = None
                en_oferta = False
                
                if descuento > 0:
                    # Calcular precio original antes del descuento
                    precio_original = precio / (1 - (descuento / 100))
                    en_oferta = True
                
                # Crear producto
                producto, created = Producto.objects.get_or_create(
                    sku=sku,
                    defaults={
                        'nombre': prod_data['nombre'],
                        'descripcion': prod_data['descripcion'],
                        'descripcion_corta': prod_data.get('descripcion_corta', ''),
                        'precio': precio,
                        'precio_original': precio_original,
                        'descuento_porcentaje': descuento,
                        'id_categoria': categoria,
                        'id_marca': marca,
                        'stock': prod_data['stock'],
                        'stock_minimo': 5,
                        'activo': True,
                        'destacado': prod_data.get('destacado', False),
                        'en_oferta': en_oferta,
                        'color': prod_data.get('color', ''),
                        'talla': prod_data.get('talla', ''),
                        'garantia_meses': prod_data.get('garantia', 12),
                        'peso': prod_data.get('peso', None),
                        'dimensiones': prod_data.get('dimensiones', ''),
                        'calificacion_promedio': Decimal(str(random.uniform(4.0, 5.0)))[:3],
                        'total_resenas': random.randint(10, 200),
                        'total_ventas': random.randint(50, 500)
                    }
                )
                
                # Crear imagen principal del producto
                if created:
                    ImagenProducto.objects.create(
                        id_producto=producto,
                        url_imagen=f'https://via.placeholder.com/600x600/0052A3/ffffff?text={marca.nombre}',
                        alt_text=prod_data['nombre'],
                        es_principal=True,
                        orden_display=0
                    )
                
                productos.append(producto)
                
            except (Categoria.DoesNotExist, Marca.DoesNotExist) as e:
                self.stdout.write(self.style.ERROR(f'Error: {e} - {prod_data["nombre"]}'))
                continue
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creando producto: {e}'))
                continue

        return productos
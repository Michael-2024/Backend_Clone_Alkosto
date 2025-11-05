from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import  login, logout, update_session_auth_hash
from django.db.models import Q
#from django.db import models
<<<<<<< HEAD
from .models import Producto, Categoria, Marca, Usuario, Carrito, CarritoItem, Favorito
=======
from .models import Producto, Categoria, Marca, Usuario, Carrito, CarritoItem,Favorito, Resena
>>>>>>> origin/master
from .serializers import (ProductoSerializer, CategoriaSerializer, 
                          MarcaSerializer, UsuarioSerializer, LoginSerializer, 
                          CarritoSerializer, CarritoItemSerializer,UsuarioRegistroSerializer, 
                          UsuarioLoginSerializer, UsuarioPerfilSerializer, UsuarioUpdateSerializer, 
<<<<<<< HEAD
                         CambioPasswordSerializer, FavoritoSerializer)
import alkosto_backend.settings as settings
=======
                         CambioPasswordSerializer, FavoritoSerializer, ResenaSerializer, CrearResenaSerializer, 
                         ProductoConResenasSerializer)
>>>>>>> origin/master
from django.utils import timezone

# Nota: la implementación completa de `ProductoViewSet` aparece más abajo
# con filtros y opciones avanzadas; la definición simplificada inicial se
# eliminó para evitar duplicidad.

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.filter(activa=True) 
    #queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.AllowAny]

class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.filter(activa=True)
    #queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    permission_classes = [permissions.AllowAny]

# API para login
class AutenticacionViewSet(viewsets.ViewSet):
    """
    ViewSet para manejar todas las operaciones de autenticación y perfil de usuario
    """
    def list(self, request):
        """
        Lista todos los endpoints disponibles de autenticación
        GET /api/auth/
        """
        base_url = request.build_absolute_uri('/')[:-1]  # Remover slash final
        
        endpoints = {
            "message": "API de Autenticación - Alkosto Backend",
            "endpoints_available": {
                "registro": {
                    "url": f"{base_url}/api/auth/registro/",
                    "method": "POST",
                    "description": "Registro de nuevos usuarios",
                    "body_required": {
                        "nombre": "string",
                        "apellido": "string", 
                        "email": "string",
                        "telefono": "string (opcional)",
                        "password": "string",
                        "password_confirm": "string"
                    }
                },
                "login": {
                    "url": f"{base_url}/api/auth/login/",
                    "method": "POST", 
                    "description": "Inicio de sesión de usuarios",
                    "body_required": {
                        "email": "string",
                        "password": "string"
                    }
                },
                "logout": {
                    "url": f"{base_url}/api/auth/logout/",
                    "method": "POST",
                    "description": "Cerrar sesión del usuario",
                    "authentication_required": True
                },
                "perfil": {
                    "url": f"{base_url}/api/auth/perfil/",
                    "method": "GET",
                    "description": "Obtener perfil del usuario actual", 
                    "authentication_required": True
                },
                "actualizar_perfil": {
                    "url": f"{base_url}/api/auth/actualizar_perfil/",
                    "method": "PUT",
                    "description": "Actualizar perfil del usuario",
                    "authentication_required": True,
                    "body_optional": {
                        "nombre": "string",
                        "apellido": "string",
                        "telefono": "string", 
                        "fecha_nacimiento": "YYYY-MM-DD",
                        "genero": "M|F|Otro"
                    }
                },
                "cambiar_password": {
                    "url": f"{base_url}/api/auth/cambiar_password/",
                    "method": "POST",
                    "description": "Cambiar contraseña del usuario",
                    "authentication_required": True,
                    "body_required": {
                        "password_actual": "string",
                        "nuevo_password": "string", 
                        "confirmar_password": "string"
                    }
                },
                "verificar_token": {
                    "url": f"{base_url}/api/auth/verificar_token/",
                    "method": "GET", 
                    "description": "Verificar si el token es válido",
                    "authentication_required": True
                }
            }
        }
        return Response(endpoints)
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def registro(self, request):
        """Registro de nuevos usuarios - POST /api/auth/registro/"""
        serializer = UsuarioRegistroSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Crear token de autenticación
            token, created = Token.objects.get_or_create(user=user)

            # Iniciar sesión automáticamente
            login(request, user)
            
            # Migrar carrito de sesión a usuario si existe
            migrar_carrito_sesion_a_usuario(request, user)
            
            return Response({
                'token': token.key,
                'user': UsuarioPerfilSerializer(user).data,
                'message': 'Usuario registrado exitosamente'
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        """Inicio de sesión de usuarios - POST /api/auth/login/"""
        serializer = UsuarioLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Actualizar último acceso
            user.fecha_ultimo_acceso = timezone.now()
            user.save()
            
            # Crear o obtener token
            token, created = Token.objects.get_or_create(user=user)
            
            # Iniciar sesión
            login(request, user)
            
            # Migrar carrito de sesión a usuario si existe
            migrar_carrito_sesion_a_usuario(request, user)
            
            return Response({
                'token': token.key,
                'user': UsuarioPerfilSerializer(user).data,
                'message': 'Login exitoso'
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        """Cerrar sesión del usuario - POST /api/auth/logout/"""
        # Eliminar token
        Token.objects.filter(user=request.user).delete()
        
        # Cerrar sesión
        logout(request)
        
        return Response({'message': 'Logout exitoso'})

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def perfil(self, request):
        """Obtener perfil del usuario actual - GET /api/auth/perfil/"""
        serializer = UsuarioPerfilSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def actualizar_perfil(self, request):
        """Actualizar perfil del usuario - PUT /api/auth/actualizar_perfil/"""
        serializer = UsuarioUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'user': UsuarioPerfilSerializer(request.user).data,
                'message': 'Perfil actualizado exitosamente'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def cambiar_password(self, request):
        """Cambiar contraseña del usuario - POST /api/auth/cambiar_password/"""
        serializer = CambioPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            
            # Verificar contraseña actual
            if not user.check_password(serializer.validated_data['password_actual']):
                return Response(
                    {'error': 'La contraseña actual es incorrecta'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Cambiar contraseña
            user.set_password(serializer.validated_data['nuevo_password'])
            user.save()
            
            # Actualizar sesión para no cerrarla
            update_session_auth_hash(request, user)
            
            return Response({'message': 'Contraseña cambiada exitosamente'})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def verificar_token(self, request):
        """Verificar si el token es válido - GET /api/auth/verificar_token/"""
        return Response({
            'valido': True,
            'user': UsuarioPerfilSerializer(request.user).data,
            'message': 'Token válido'
        })

# 🔧 FUNCIÓN AUXILIAR PARA MIGRAR CARRITO
def migrar_carrito_sesion_a_usuario(request, user):
    """Migrar carrito de sesión anónima a usuario autenticado"""
    session_id = request.session.session_key
    if session_id:
        carrito_sesion = Carrito.objects.filter(session_id=session_id).first()
        carrito_usuario, created = Carrito.objects.get_or_create(id_usuario=user)
        
        if carrito_sesion and carrito_sesion != carrito_usuario:
            # Migrar items del carrito de sesión al carrito del usuario
            for item_sesion in carrito_sesion.items.all():
                item_existente = carrito_usuario.items.filter(
                    id_producto=item_sesion.id_producto
                ).first()
                
                if item_existente:
                    item_existente.cantidad += item_sesion.cantidad
                    item_existente.save()
                else:
                    carrito_usuario.items.create(
                        id_producto=item_sesion.id_producto,
                        cantidad=item_sesion.cantidad,
                        precio_unitario=item_sesion.precio_unitario
                    )
            
            # Eliminar carrito de sesión
            carrito_sesion.delete()    

# API para productos destacados
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def productos_destacados(request):
    productos = Producto.objects.filter(destacado=True, activo=True)
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data)

# API para productos en oferta
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def productos_oferta(request):
    productos = Producto.objects.filter(en_oferta=True, activo=True)
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data)

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.filter(activo=True) 
    serializer_class = ProductoSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Producto.objects.filter(activo=True)
        
        # 🔍 BÚSQUEDA POR TEXTO (nombre, descripción, SKU)
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) |
                Q(descripcion__icontains=search) |
                Q(descripcion_corta__icontains=search) |
                Q(sku__icontains=search)
            )
        
        # 🏷️ FILTRO POR CATEGORÍA
        categoria = self.request.query_params.get('categoria', None)
        if categoria:
            queryset = queryset.filter(id_categoria=categoria)
        
        # 🏭 FILTRO POR MARCA
        marca = self.request.query_params.get('marca', None)
        if marca:
            queryset = queryset.filter(id_marca=marca)
        
        # 💰 FILTRO POR RANGO DE PRECIO
        precio_min = self.request.query_params.get('precio_min', None)
        precio_max = self.request.query_params.get('precio_max', None)
        if precio_min:
            queryset = queryset.filter(precio__gte=precio_min)
        if precio_max:
            queryset = queryset.filter(precio__lte=precio_max)
        
        # ⭐ FILTRO POR PRODUCTOS DESTACADOS
        destacados = self.request.query_params.get('destacados', None)
        if destacados and destacados.lower() == 'true':
            queryset = queryset.filter(destacado=True)
        
        # 🏷️ FILTRO POR OFERTA
        oferta = self.request.query_params.get('oferta', None)
        if oferta and oferta.lower() == 'true':
            queryset = queryset.filter(en_oferta=True)
        
        # 📦 FILTRO POR DISPONIBILIDAD
        disponible = self.request.query_params.get('disponible', None)
        if disponible and disponible.lower() == 'true':
            queryset = queryset.filter(stock__gt=0)
        
        # 🔄 ORDENAMIENTO
        orden = self.request.query_params.get('orden', None)
        if orden:
            if orden == 'precio_asc':
                queryset = queryset.order_by('precio')
            elif orden == 'precio_desc':
                queryset = queryset.order_by('-precio')
            elif orden == 'nombre_asc':
                queryset = queryset.order_by('nombre')
            elif orden == 'nombre_desc':
                queryset = queryset.order_by('-nombre')
            elif orden == 'mas_vendidos':
                queryset = queryset.order_by('-total_ventas')
            elif orden == 'mejor_calificados':
                queryset = queryset.order_by('-calificacion_promedio')
            elif orden == 'nuevos':
                queryset = queryset.order_by('-created_at')
        
        return queryset

    # 📊 ACCIÓN EXTRA: Obtener estadísticas de filtros disponibles
    @action(detail=False, methods=['get'])
    def filtros_disponibles(self, request):
        from django.db.models import Min, Max
        
        categorias = Categoria.objects.filter(activa=True)
        marcas = Marca.objects.filter(activa=True)
        
        # Calcular rangos de precios
        precios = Producto.objects.filter(activo=True).aggregate(
            min_precio=Min('precio'),
            max_precio=Max('precio')
        )
        
        return Response({
            'categorias': CategoriaSerializer(categorias, many=True).data,
            'marcas': MarcaSerializer(marcas, many=True).data,
            'rangos_precio': precios,
            'total_productos': Producto.objects.filter(activo=True).count(),
            'productos_destacados': Producto.objects.filter(destacado=True, activo=True).count(),
            'productos_oferta': Producto.objects.filter(en_oferta=True, activo=True).count(),
        })
    
    # 🔍 BÚSQUEDA AVANZADA
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def buscar_productos(request):
    """
    Búsqueda avanzada con múltiples filtros
    """
    search = request.query_params.get('q', '')
    categoria_id = request.query_params.get('categoria', None)
    marca_id = request.query_params.get('marca', None)
    precio_min = request.query_params.get('precio_min', None)
    precio_max = request.query_params.get('precio_max', None)
    orden = request.query_params.get('orden', 'relevancia')
    
    productos = Producto.objects.filter(activo=True)
    
    # Búsqueda por texto
    if search:
        productos = productos.filter(
            Q(nombre__icontains=search) |
            Q(descripcion__icontains=search) |
            Q(descripcion_corta__icontains=search) |
            Q(sku__icontains=search)
        )
    
    # Aplicar filtros
    if categoria_id:
        productos = productos.filter(id_categoria=categoria_id)
    
    if marca_id:
        productos = productos.filter(id_marca=marca_id)
    
    if precio_min:
        productos = productos.filter(precio__gte=precio_min)
    
    if precio_max:
        productos = productos.filter(precio__lte=precio_max)
    
    # Ordenamiento
    if orden == 'precio_asc':
        productos = productos.order_by('precio')
    elif orden == 'precio_desc':
        productos = productos.order_by('-precio')
    elif orden == 'nombre':
        productos = productos.order_by('nombre')
    elif orden == 'nuevos':
        productos = productos.order_by('-created_at')
    else:  # relevancia por defecto
        productos = productos.order_by('-destacado', '-total_ventas', '-calificacion_promedio')
    
    serializer = ProductoSerializer(productos, many=True)
    
    return Response({
        'resultados': serializer.data,
        'total': productos.count(),
        'parametros': {
            'busqueda': search,
            'categoria': categoria_id,
            'marca': marca_id,
            'precio_min': precio_min,
            'precio_max': precio_max,
            'orden': orden
        }
    })

# 🏠 PRODUCTOS POR CATEGORÍA
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def productos_por_categoria(request, categoria_slug):
    """
    Obtener productos por slug de categoría
    """
    try:
        categoria = Categoria.objects.get(slug=categoria_slug, activa=True)
        productos = Producto.objects.filter(id_categoria=categoria, activo=True)
        
        # Aplicar filtros adicionales
        marca = request.query_params.get('marca', None)
        if marca:
            productos = productos.filter(id_marca=marca)
            
        orden = request.query_params.get('orden', None)
        if orden == 'precio_asc':
            productos = productos.order_by('precio')
        elif orden == 'precio_desc':
            productos = productos.order_by('-precio')
        elif orden == 'nombre':
            productos = productos.order_by('nombre')
        serializer = ProductoSerializer(productos, many=True)

        return Response({
            'categoria': CategoriaSerializer(categoria).data,
            'productos': serializer.data,
            'total': productos.count()
        })

    except Categoria.DoesNotExist:
        return Response({'error': 'Categoría no encontrada'}, status=status.HTTP_404_NOT_FOUND)

# 🔥 PRODUCTOS MÁS VENDIDOS
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def productos_mas_vendidos(request):
    """
    Obtener los productos más vendidos
    """
    
    limite = request.query_params.get('limite', 10)
    productos = Producto.objects.filter(
        activo=True, 
        total_ventas__gt=0
    ).order_by('-total_ventas')[:int(limite)]
    
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data)

#CARRITO DE COMPRAS

class CarritoViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    
    def get_carrito_actual(self, request):
        """Obtener o crear el carrito actual"""
        user = request.user if request.user.is_authenticated else None
        session_id = request.session.session_key
        
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        
        if user and user.is_authenticated:
            # Usuario autenticado
            carrito, created = Carrito.objects.get_or_create(id_usuario=user)
        else:
            # Usuario anónimo
            carrito, created = Carrito.objects.get_or_create(session_id=session_id)
        
        return carrito

    def list(self, request):
        """Obtener el carrito actual - GET /api/carrito/"""
        carrito = self.get_carrito_actual(request)
        serializer = CarritoSerializer(carrito)
        return Response(serializer.data)

    def create(self, request):
        """Agregar item al carrito - POST /api/carrito/"""
        carrito = self.get_carrito_actual(request)
        producto_id = request.data.get('id_producto')
        cantidad = int(request.data.get('cantidad', 1))
        
        try:
            producto = Producto.objects.get(id_producto=producto_id, activo=True)
        except Producto.DoesNotExist:
            return Response(
                {'error': 'Producto no encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Verificar stock
        if producto.stock < cantidad:
            return Response(
                {'error': f'Stock insuficiente. Disponible: {producto.stock}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Buscar o crear item
        item, created = CarritoItem.objects.get_or_create(
            id_carrito=carrito,
            id_producto=producto,
            defaults={
                'cantidad': cantidad,
                'precio_unitario': producto.precio
            }
        )
        
        if not created:
            item.cantidad += cantidad
            item.save()
        
        serializer = CarritoItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        """Actualizar cantidad - PATCH /api/carrito/{id_item}/"""
        try:
            item = CarritoItem.objects.get(id_item=pk)
        except CarritoItem.DoesNotExist:
            return Response(
                {'error': 'Item no encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        nueva_cantidad = request.data.get('cantidad')
        if nueva_cantidad is not None:
            nueva_cantidad = int(nueva_cantidad)
            
            # Verificar stock
            if item.id_producto.stock < nueva_cantidad:
                return Response(
                    {'error': f'Stock insuficiente. Disponible: {item.id_producto.stock}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if nueva_cantidad <= 0:
                item.delete()
                return Response({'message': 'Item eliminado del carrito'})
            
            item.cantidad = nueva_cantidad
            item.save()
        
        serializer = CarritoItemSerializer(item)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Eliminar item - DELETE /api/carrito/{id_item}/"""
        try:
            item = CarritoItem.objects.get(id_item=pk)
            item.delete()
            return Response({'message': 'Item eliminado del carrito'})
        except CarritoItem.DoesNotExist:
            return Response(
                {'error': 'Item no encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['delete'])
    def vaciar(self, request):
        """Vaciar carrito - DELETE /api/carrito/vaciar/"""
        carrito = self.get_carrito_actual(request)
        carrito.items.all().delete()
        return Response({'message': 'Carrito vaciado'})

# Vistas simples del carrito
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def obtener_carrito(request):
    """Obtener el carrito actual - GET /api/carrito/obtener/"""
    viewset = CarritoViewSet()
    return viewset.list(request)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def agregar_al_carrito(request):
    """Agregar producto al carrito - POST /api/carrito/agregar/"""
    viewset = CarritoViewSet()
    return viewset.create(request)

@api_view(['DELETE'])
@permission_classes([permissions.AllowAny])
def vaciar_carrito(request):
    """Vaciar carrito - DELETE /api/carrito/vaciar/"""
    viewset = CarritoViewSet()
    return viewset.vaciar(request)

#Favoritos y reseñas

# FAVORITOS Y RESEÑAS

class FavoritoViewSet(viewsets.ModelViewSet):
    serializer_class = FavoritoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorito.objects.filter(id_usuario=self.request.user)

    def perform_create(self, serializer):
        # Verificar si ya existe como favorito
        producto_id = self.request.data.get('id_producto')
        if Favorito.objects.filter(id_usuario=self.request.user, id_producto_id=producto_id).exists():
            raise serializers.ValidationError('Este producto ya está en tus favoritos')

        serializer.save(id_usuario=self.request.user)

    @action(detail=False, methods=['get'])
    def mis_favoritos(self, request):
        """Obtener todos los favoritos del usuario"""
        favoritos = self.get_queryset()
        serializer = self.get_serializer(favoritos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def toggle_favorito(self, request):
        """Agregar o quitar producto de favoritos"""
        producto_id = request.data.get('id_producto')
        
        try:
            producto = Producto.objects.get(id_producto=producto_id, activo=True)
        except Producto.DoesNotExist:
            return Response(
                {'error': 'Producto no encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )

        favorito = Favorito.objects.filter(id_usuario=request.user, id_producto=producto).first()
        
        if favorito:
            # Si ya existe, eliminarlo (toggle off)
            favorito.delete()
            return Response({
                'message': 'Producto eliminado de favoritos',
                'es_favorito': False
            })
        else:
            # Si no existe, crearlo (toggle on)
            Favorito.objects.create(id_usuario=request.user, id_producto=producto)
            return Response({
                'message': 'Producto agregado a favoritos',
                'es_favorito': True
            })

    @action(detail=False, methods=['get'])
    def verificar_favorito(self, request):
        """Verificar si un producto está en favoritos"""
        producto_id = request.query_params.get('producto_id')
        
        if not producto_id:
            return Response(
                {'error': 'Se requiere producto_id'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        es_favorito = Favorito.objects.filter(
            id_usuario=request.user, 
            id_producto_id=producto_id
        ).exists()
        
        return Response({'es_favorito': es_favorito})

class ResenaViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return CrearResenaSerializer
        return ResenaSerializer

    def get_queryset(self):
        queryset = Resena.objects.filter(aprobada=True)
        
        # Filtrar por producto si se especifica
        producto_id = self.request.query_params.get('producto_id')
        if producto_id:
            queryset = queryset.filter(id_producto_id=producto_id)
        
        return queryset

    def perform_create(self, serializer):
        # Verificar si el usuario ya reseñó este producto
        producto_id = self.request.data.get('id_producto')
        if Resena.objects.filter(id_usuario=self.request.user, id_producto_id=producto_id).exists():
            # Usar la excepción correcta para que DRF devuelva 400 con detalle
            raise serializers.ValidationError('Ya has reseñado este producto')

        serializer.save(id_usuario=self.request.user)

    def create(self, request, *args, **kwargs):
        """Crear reseña y devolver mensaje + reseña en la respuesta"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # perform_create comprobará duplicados y guardará el usuario
        self.perform_create(serializer)

        resena = getattr(serializer, 'instance', None)
        headers = self.get_success_headers(serializer.data)

        return Response(
            {
                'message': 'Producto reseñado exitosamente',
                'resena': ResenaSerializer(resena).data if resena is not None else serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    @action(detail=False, methods=['get'])
    def mis_resenas(self, request):
        """Obtener todas las reseñas del usuario autenticado"""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        resenas = Resena.objects.filter(id_usuario=request.user)
        serializer = ResenaSerializer(resenas, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def aprobar_resena(self, request, pk=None):
        """Aprobar una reseña (solo para admin/empleados)"""
        if request.user.rol not in ['admin', 'empleado']:
            return Response(
                {'error': 'No tienes permisos para esta acción'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            resena = self.get_object()
            resena.aprobada = True
            resena.save()
            
            # Actualizar estadísticas del producto
            producto = resena.id_producto
            reseñas_aprobadas = Resena.objects.filter(id_producto=producto, aprobada=True)
            
            # Calcular nueva calificación promedio
            calificacion_promedio = reseñas_aprobadas.aggregate(
                avg_calificacion=models.Avg('calificacion')
            )['avg_calificacion'] or 0.0
            
            producto.calificacion_promedio = round(calificacion_promedio, 1)
            producto.total_resenas = reseñas_aprobadas.count()
            producto.save()
            
            return Response({'message': 'Reseña aprobada exitosamente'})
            
        except Resena.DoesNotExist:
            return Response(
                {'error': 'Reseña no encontrada'}, 
                status=status.HTTP_404_NOT_FOUND
            )

# Vistas API para favoritos
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def obtener_favoritos(request):
    """Obtener todos los favoritos del usuario"""
    favoritos = Favorito.objects.filter(id_usuario=request.user)
    serializer = FavoritoSerializer(favoritos, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def toggle_favorito(request):
    """Agregar o quitar producto de favoritos"""
    producto_id = request.data.get('id_producto')
    
    try:
        producto = Producto.objects.get(id_producto=producto_id, activo=True)
    except Producto.DoesNotExist:
        return Response(
            {'error': 'Producto no encontrado'}, 
            status=status.HTTP_404_NOT_FOUND
        )

    favorito = Favorito.objects.filter(id_usuario=request.user, id_producto=producto).first()
    
    if favorito:
        favorito.delete()
        return Response({
            'message': 'Producto eliminado de favoritos',
            'es_favorito': False
        })
    else:
        Favorito.objects.create(id_usuario=request.user, id_producto=producto)
        return Response({
            'message': 'Producto agregado a favoritos',
            'es_favorito': True
        })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def verificar_favorito(request, producto_id):
    """Verificar si un producto está en favoritos"""
    es_favorito = Favorito.objects.filter(
        id_usuario=request.user, 
        id_producto_id=producto_id
    ).exists()
    
    return Response({'es_favorito': es_favorito})

# Vistas API para reseñas
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def obtener_resenas_producto(request, producto_id):
    """Obtener todas las reseñas aprobadas de un producto"""
    try:
        producto = Producto.objects.get(id_producto=producto_id, activo=True)
    except Producto.DoesNotExist:
        return Response(
            {'error': 'Producto no encontrado'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    resenas = Resena.objects.filter(id_producto=producto, aprobada=True)
    serializer = ResenaSerializer(resenas, many=True)
    
    return Response({
        'producto': producto.nombre,
        'calificacion_promedio': producto.calificacion_promedio,
        'total_resenas': producto.total_resenas,
        'resenas': serializer.data
    })

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def crear_resena(request):
    """Crear una nueva reseña"""
    serializer = CrearResenaSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
        # Obtener id del producto de forma segura (puede venir como instancia o como id)
        producto_field = serializer.validated_data.get('id_producto', None)
        if producto_field is None:
            producto_id = request.data.get('id_producto')
        else:
            producto_id = getattr(producto_field, 'id_producto', producto_field)

        # Verificar si el usuario ya reseñó este producto
        if Resena.objects.filter(id_usuario=request.user, id_producto_id=producto_id).exists():
            return Response({'error': 'Ya has reseñado este producto'}, status=status.HTTP_400_BAD_REQUEST)

        resena = serializer.save()

        # Si el usuario es admin/empleado, aprobar automáticamente
        if getattr(request.user, 'rol', None) in ['admin', 'empleado']:
            resena.aprobada = True
            resena.save()

        # Devolver mensaje y la reseña creada
        return Response(
            {'message': 'Producto reseñado exitosamente', 'resena': ResenaSerializer(resena).data},
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

<<<<<<< HEAD
# 🔧 FUNCIÓN AUXILIAR PARA MIGRAR CARRITO
def migrar_carrito_sesion_a_usuario(request, user):
    """Migrar carrito de sesión anónima a usuario autenticado"""
    session_id = request.session.session_key
    if session_id:
        carrito_sesion = Carrito.objects.filter(session_id=session_id).first()
        carrito_usuario, created = Carrito.objects.get_or_create(id_usuario=user)
        
        if carrito_sesion and carrito_sesion != carrito_usuario:
            # Migrar items del carrito de sesión al carrito del usuario
            for item_sesion in carrito_sesion.items.all():
                item_existente = carrito_usuario.items.filter(
                    id_producto=item_sesion.id_producto
                ).first()
                
                if item_existente:
                    item_existente.cantidad += item_sesion.cantidad
                    item_existente.save()
                else:
                    carrito_usuario.items.create(
                        id_producto=item_sesion.id_producto,
                        cantidad=item_sesion.cantidad,
                        precio_unitario=item_sesion.precio_unitario
                    )
            
            # Eliminar carrito de sesión
            carrito_sesion.delete()


# 🔐 VISTAS DE FAVORITOS
class FavoritoViewSet(viewsets.ModelViewSet):
    serializer_class = FavoritoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Favorito.objects.filter(usuario=self.request.user).select_related('producto')
    
    def create(self, request, *args, **kwargs):
        producto_id = request.data.get('producto')
        
        try:
            producto = Producto.objects.get(id_producto=producto_id)
        except Producto.DoesNotExist:
            return Response(
                {'error': 'Producto no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Verificar si ya existe
        favorito_existente = Favorito.objects.filter(
            usuario=request.user,
            producto=producto
        ).first()
        
        if favorito_existente:
            return Response(
                {'message': 'El producto ya está en favoritos'},
                status=status.HTTP_200_OK
            )
        
        # Crear favorito
        favorito = Favorito.objects.create(
            usuario=request.user,
            producto=producto
        )
        
        serializer = self.get_serializer(favorito)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        try:
            favorito = self.get_queryset().get(pk=kwargs['pk'])
            favorito.delete()
            return Response(
                {'message': 'Favorito eliminado'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Favorito.DoesNotExist:
            return Response(
                {'error': 'Favorito no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )    
=======
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def mis_resenas(request):
    """Obtener todas las reseñas del usuario"""
    resenas = Resena.objects.filter(id_usuario=request.user)
    serializer = ResenaSerializer(resenas, many=True)
    return Response(serializer.data)

# Productos con reseñas detalladas
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def producto_detallado(request, producto_id):
    """Obtener producto con todas sus reseñas"""
    try:
        producto = Producto.objects.get(id_producto=producto_id, activo=True)
    except Producto.DoesNotExist:
        return Response(
            {'error': 'Producto no encontrado'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = ProductoConResenasSerializer(producto)
    
    # Agregar información de favorito si el usuario está autenticado
    data = serializer.data
    if request.user.is_authenticated:
        data['es_favorito'] = Favorito.objects.filter(
            id_usuario=request.user, 
            id_producto=producto
        ).exists()
    
    return Response(data)

>>>>>>> origin/master

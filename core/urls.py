from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('productos', views.ProductoViewSet)
router.register('categorias', views.CategoriaViewSet)
router.register('marcas', views.MarcaViewSet)
router.register('carrito', views.CarritoViewSet, basename='carrito')
router.register('favoritos', views.FavoritoViewSet, basename='favoritos')
router.register('resenas', views.ResenaViewSet, basename='resena')
router.register('auth', views.AutenticacionViewSet, basename='auth')  

urlpatterns = [
    path('', include(router.urls)),
    
    # 🔐 AUTENTICACIÓN Y USUARIOS
    path('auth/registro/', views.AutenticacionViewSet.registro, name='registro'),
    path('auth/login/', views.AutenticacionViewSet.login, name='login'),
    path('auth/logout/', views.AutenticacionViewSet.logout, name='logout'),
    path('auth/perfil/', views.AutenticacionViewSet.perfil, name='perfil'),
    path('auth/actualizar-perfil/', views.AutenticacionViewSet.actualizar_perfil, name='actualizar_perfil'),
    path('auth/cambiar-password/', views.AutenticacionViewSet.cambiar_password, name='cambiar_password'),
    
    # 📦 PRODUCTOS Y BÚSQUEDAS
    path('destacados/', views.productos_destacados, name='productos_destacados'),
    path('ofertas/', views.productos_oferta, name='productos_oferta'),
    path('buscar/', views.buscar_productos, name='buscar_productos'),
    path('categoria/<str:categoria_slug>/', views.productos_por_categoria, name='productos_por_categoria'),
    path('mas-vendidos/', views.productos_mas_vendidos, name='productos_mas_vendidos'),
    
# ⭐ FAVORITOS 
    path('favoritos/obtener/', views.obtener_favoritos, name='obtener_favoritos'),
    path('favoritos/toggle/', views.toggle_favorito, name='toggle_favorito'),
    path('favoritos/verificar/<int:producto_id>/', views.verificar_favorito, name='verificar_favorito'),
    
    # 📝 RESEÑAS
    path('resenas/crear/', views.crear_resena, name='crear_resena'),
    path('resenas/mis-resenas/', views.mis_resenas, name='mis_resenas'),
    path('resenas/producto/<int:producto_id>/', views.obtener_resenas_producto, name='obtener_resenas_producto'),

    # 🛒 CARRITO (URLs simples)
    path('carrito/obtener/', views.obtener_carrito, name='obtener_carrito'),
    path('carrito/agregar/', views.agregar_al_carrito, name='agregar_al_carrito'),
]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('productos', views.ProductoViewSet)
router.register('categorias', views.CategoriaViewSet)
router.register('marcas', views.MarcaViewSet)
router.register('carrito', views.CarritoViewSet, basename='carrito')
router.register('favoritos', views.FavoritoViewSet, basename='favoritos')

urlpatterns = [
    path('', include(router.urls)),
    
    # 🔐 AUTENTICACIÓN Y USUARIOS
    path('auth/registro/', views.registro_usuario, name='registro'),
    path('auth/login/', views.login_usuario, name='login'),
    path('auth/logout/', views.logout_usuario, name='logout'),
    path('auth/perfil/', views.perfil_usuario, name='perfil'),
    path('auth/actualizar-perfil/', views.actualizar_perfil, name='actualizar_perfil'),
    path('auth/cambiar-password/', views.cambiar_password, name='cambiar_password'),
    
    # 📦 PRODUCTOS Y BÚSQUEDAS
    path('destacados/', views.productos_destacados, name='productos_destacados'),
    path('ofertas/', views.productos_oferta, name='productos_oferta'),
    path('buscar/', views.buscar_productos, name='buscar_productos'),
    path('categoria/<str:categoria_slug>/', views.productos_por_categoria, name='productos_por_categoria'),
    path('mas-vendidos/', views.productos_mas_vendidos, name='productos_mas_vendidos'),
    
    # 🛒 CARRITO (URLs simples)
    path('carrito/obtener/', views.obtener_carrito, name='obtener_carrito'),
    path('carrito/agregar/', views.agregar_al_carrito, name='agregar_al_carrito'),
]
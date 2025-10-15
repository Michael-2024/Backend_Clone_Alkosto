from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Crear el router
router = DefaultRouter()
router.register('productos', views.ProductoViewSet)
router.register('categorias', views.CategoriaViewSet)
router.register('marcas', views.MarcaViewSet)
router.register('carrito', views.CarritoViewSet, basename='carrito')

urlpatterns = [
    # Rutas del router
    path('', include(router.urls)),
    
    # Rutas simples
    path('login/', views.login_view, name='login'),
    path('destacados/', views.productos_destacados, name='productos_destacados'),
    path('ofertas/', views.productos_oferta, name='productos_oferta'),
    path('buscar/', views.buscar_productos, name='buscar_productos'),
    path('categoria/<str:categoria_slug>/', views.productos_por_categoria, name='productos_por_categoria'),
    path('mas-vendidos/', views.productos_mas_vendidos, name='productos_mas_vendidos'),
    
    # Rutas del carrito (simples)
    path('carrito/obtener/', views.obtener_carrito, name='obtener_carrito'),
    path('carrito/agregar/', views.agregar_al_carrito, name='agregar_al_carrito'),
]
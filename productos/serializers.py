from rest_framework import serializers
from .models import Producto, Categoria, Marca, ImagenProducto, Usuario, Carrito, CarritoItem
from django.contrib.auth import authenticate

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'

class ImagenProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenProducto
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='id_categoria.nombre', read_only=True)
    marca_nombre = serializers.CharField(source='id_marca.nombre', read_only=True)
    imagenes = ImagenProductoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Producto
        fields = [
            'id_producto', 'nombre', 'descripcion', 'descripcion_corta', 'sku',
            'precio', 'precio_original', 'descuento_porcentaje', 'stock',
            'id_categoria', 'categoria_nombre', 'id_marca', 'marca_nombre',
            'activo', 'destacado', 'en_oferta', 'calificacion_promedio',
            'total_resenas', 'imagenes'
        ]

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id_usuario', 'nombre', 'apellido', 'email', 'telefono', 'rol']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise serializers.ValidationError('Usuario inactivo')
            else:
                raise serializers.ValidationError('Credenciales inválidas')
        else:
            raise serializers.ValidationError('Email y contraseña requeridos')
        
        return data
    
#CARRITO DE COMPRAS

class CarritoItemSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='id_producto.nombre', read_only=True)
    producto_imagen = serializers.SerializerMethodField()
    producto_stock = serializers.IntegerField(source='id_producto.stock', read_only=True)
    subtotal = serializers.SerializerMethodField()
    
    class Meta:
        model = CarritoItem
        fields = [
            'id_item', 'id_producto', 'producto_nombre', 'producto_imagen',
            'producto_stock', 'cantidad', 'precio_unitario', 'subtotal'
        ]
    
    def get_producto_imagen(self, obj):
        imagen_principal = obj.id_producto.imagenproducto_set.filter(es_principal=True).first()
        return imagen_principal.url_imagen if imagen_principal else None
    
    def get_subtotal(self, obj):
        return obj.subtotal

class CarritoSerializer(serializers.ModelSerializer):
    items = CarritoItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Carrito
        fields = [
            'id_carrito', 'id_usuario', 'session_id', 
            'items', 'total_items', 'subtotal', 'created_at'
        ]
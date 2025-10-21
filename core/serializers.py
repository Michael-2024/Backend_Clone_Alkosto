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

# 🔐 SERIALIZERS PARA AUTENTICACIÓN Y USUARIOS
class UsuarioRegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'email', 'telefono', 'password', 'password_confirm']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = Usuario.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UsuarioLoginSerializer(serializers.Serializer):
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

class UsuarioPerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id_usuario', 'nombre', 'apellido', 'email', 'telefono', 
            'fecha_nacimiento', 'genero', 'rol', 'email_verificado',
            'fecha_ultimo_acceso', 'created_at'
        ]
        read_only_fields = [
            'id_usuario', 'email', 'rol', 'email_verificado', 
            'fecha_ultimo_acceso', 'created_at'
        ]

class UsuarioUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'telefono', 'fecha_nacimiento', 'genero']

class CambioPasswordSerializer(serializers.Serializer):
    password_actual = serializers.CharField(required=True)
    nuevo_password = serializers.CharField(required=True, min_length=6)
    confirmar_password = serializers.CharField(required=True, min_length=6)
    
    def validate(self, data):
        if data['nuevo_password'] != data['confirmar_password']:
            raise serializers.ValidationError("Los nuevos passwords no coinciden")
        return data
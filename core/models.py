from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=150)
    password = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=5, choices=[('M', 'Masculino'), ('F', 'Femenino'), ('Otro', 'Otro')], null=True, blank=True)
    rol = models.CharField(max_length=10, choices=[('cliente', 'Cliente'), ('empleado', 'Empleado'), ('admin', 'Admin')], default='cliente')
    activo = models.BooleanField(default=True)
    email_verificado = models.BooleanField(default=False)
    fecha_ultimo_acceso = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Campos requeridos para Django
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    objects = UsuarioManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellido']
    
    class Meta:
        db_table = 'usuarios'
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    slug = models.CharField(max_length=120, unique=True)
    imagen_url = models.CharField(max_length=500, null=True, blank=True)
    id_categoria_padre = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, db_column='id_categoria_padre')
    activa = models.BooleanField(default=True)
    orden_display = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'categorias'
    
    def __str__(self):
        return self.nombre

class Marca(models.Model):
    id_marca = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    logo_url = models.CharField(max_length=500, null=True, blank=True)
    sitio_web = models.CharField(max_length=200, null=True, blank=True)
    activa = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'marcas'
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(null=True, blank=True)
    descripcion_corta = models.CharField(max_length=500, null=True, blank=True)
    sku = models.CharField(max_length=100, unique=True)
    codigo_barras = models.CharField(max_length=50, null=True, blank=True)
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, db_column='id_categoria')
    id_marca = models.ForeignKey(Marca, on_delete=models.CASCADE, null=True, blank=True, db_column='id_marca')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    precio_original = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    descuento_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    stock = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=10)
    peso = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    dimensiones = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    talla = models.CharField(max_length=20, null=True, blank=True)
    garantia_meses = models.IntegerField(default=12)
    activo = models.BooleanField(default=True)
    destacado = models.BooleanField(default=False)
    en_oferta = models.BooleanField(default=False)
    fecha_lanzamiento = models.DateField(null=True, blank=True)
    calificacion_promedio = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    total_resenas = models.IntegerField(default=0)
    total_ventas = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'productos'
    
    def __str__(self):
        return self.nombre

class ImagenProducto(models.Model):
    id_imagen = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, db_column='id_producto')
    url_imagen = models.CharField(max_length=500)
    alt_text = models.CharField(max_length=200, null=True, blank=True)
    es_principal = models.BooleanField(default=False)
    orden_display = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'imagenes_producto'
    
    def __str__(self):
        return f"Imagen de {self.id_producto.nombre}"
    

    #CARRITO DE COMPRAS
class Carrito(models.Model):
    id_carrito = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True, db_column='id_usuario')
    session_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'carritos'
    
    def __str__(self):
        if self.id_usuario:
            return f"Carrito de {self.id_usuario.email}"
        else:
            return f"Carrito sesión {self.session_id}"
    
    @property
    def total_items(self):
        return self.items.aggregate(total=models.Sum('cantidad'))['total'] or 0
    
    @property
    def subtotal(self):
        return self.items.aggregate(
            total=models.Sum(models.F('cantidad') * models.F('precio_unitario'))
        )['total'] or 0

class CarritoItem(models.Model):
    id_item = models.AutoField(primary_key=True)
    id_carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items', db_column='id_carrito')
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, db_column='id_producto')
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'carrito_items'
        constraints = [
            models.UniqueConstraint(fields=['id_carrito', 'id_producto'], name='unique_carrito_producto')
        ]
    
    def __str__(self):
        return f"{self.cantidad} x {self.id_producto.nombre}"
    
    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario
    
    def save(self, *args, **kwargs):
        # Al guardar, actualizar el precio unitario con el precio actual del producto
        if not self.precio_unitario:
            self.precio_unitario = self.id_producto.precio
        super().save(*args, **kwargs)


# FAVORITOS
class Favorito(models.Model):
    id_favorito = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='favoritos', db_column='id_usuario')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, db_column='id_producto')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'favoritos'
        constraints = [
            models.UniqueConstraint(fields=['usuario', 'producto'], name='unique_usuario_producto_favorito')
        ]
    
    def __str__(self):
        return f"{self.usuario.email} - {self.producto.nombre}"
"""Script para corregir automáticamente el archivo test_productos.py"""

import re

# Leer el archivo
with open('core/tests/test_productos.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Contador de cambios
changes = 0

# 1. Agregar import para slugify
if 'from django.utils.text import slugify' not in content:
    content = content.replace(
        'from decimal import Decimal',
        'from decimal import Decimal\nfrom django.utils.text import slugify'
    )
    changes += 1

# 2. Reemplazar creación de categorías para incluir slug
patterns = [
    # Categorías sin slug
    (r"Categoria\.objects\.create\(\s*nombre='([^']+)'(?:\s*,\s*descripcion='[^']+')?\s*\)",
     lambda m: f"Categoria.objects.create(nombre='{m.group(1)}', slug=slugify('{m.group(1)}'), descripcion='{m.group(1)}')"),
]

for pattern, replacement in patterns:
    old_content = content
    content = re.sub(pattern, replacement, content)
    if content != old_content:
        changes += 1

# 3. Reemplazar nombres de campos en Producto.objects.create()
replacements = [
    ('categoria=self.', 'id_categoria=self.'),
    ('marca=self.', 'id_marca=self.'),
    ('categoria=categoria', 'id_categoria=categoria'),
    ('marca=marca', 'id_marca=marca'),
    ('categoria=Categoria', 'id_categoria=Categoria'),
    ('marca=Marca', 'id_marca=Marca'),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        changes += 1

# 4. Agregar campo sku a los productos que no lo tienen
# Buscar todas las creaciones de Producto sin sku
producto_creates = re.findall(
    r"Producto\.objects\.create\([^)]+\)",
    content,
    re.MULTILINE | re.DOTALL
)

for create_stmt in producto_creates:
    if 'sku=' not in create_stmt and 'nombre=' in create_stmt:
        # Extraer el nombre del producto
        nombre_match = re.search(r"nombre='([^']+)'", create_stmt)
        if nombre_match:
            nombre = nombre_match.group(1)
            # Generar un SKU simple
            sku = 'SKU-' + re.sub(r'[^A-Z0-9]', '-', nombre.upper())[:20]
            # Insertar el sku después del nombre
            new_create = create_stmt.replace(
                f"nombre='{nombre}',",
                f"nombre='{nombre}',\n            sku='{sku}',"
            )
            content = content.replace(create_stmt, new_create)
            changes += 1

print(f"Total de cambios realizados: {changes}")

# Escribir el archivo corregido
with open('core/tests/test_productos.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Archivo corregido exitosamente!")

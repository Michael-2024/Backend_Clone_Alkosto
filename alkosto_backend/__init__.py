"""
Inicialización del paquete del proyecto.

Registra PyMySQL como reemplazo de MySQLdb para evitar problemas
de compilación en Windows.
"""

try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

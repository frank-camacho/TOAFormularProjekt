import sqlite3
import os
from functools import lru_cache

# Obtener el path absoluto de la base de datos
def get_db_path():
    return os.path.join(os.path.dirname(__file__), '../rma.db')

# Crear una conexión genérica a la base de datos
def get_connection():
    db_path = get_db_path()  # Corregido para que no se llame como función
    return sqlite3.connect(db_path)

# Función para ejecutar una consulta genérica
def execute_query(query, params=None, fetch_all=True):
    """
    Ejecuta una consulta SQL genérica.
    :param query: La consulta SQL a ejecutar.
    :param params: Parámetros para la consulta (opcional).
    :param fetch_all: Indica si se deben devolver todos los resultados.
    :return: Resultados de la consulta o el cursor, dependiendo del caso.
    """
    conn = get_connection()
    try:
        c = conn.cursor()
        if params:
            c.execute(query, params)
        else:
            c.execute(query)
        conn.commit()
        return c.fetchall() if fetch_all else None
    except sqlite3.Error as e:
        print(f"Error ejecutando la consulta: {e}")
        return None
    finally:
        conn.close()

# Función para obtener todos los datos de una tabla con caché
@lru_cache(maxsize=10)  # Cachear los resultados para tablas estáticas
def get_table_data(table_name):
    """
    Obtiene todos los datos de una tabla.
    :param table_name: Nombre de la tabla.
    :return: Lista de filas en la tabla.
    """
    query = f"SELECT * FROM {table_name}"
    return execute_query(query)

# Ejemplo de uso para cargar empleados
def get_employees():
    """
    Devuelve todos los empleados.
    :return: Lista de empleados.
    """
    return get_table_data("employees")

# Verificar si la base de datos está accesible
def check_db_connection():
    """
    Verifica si la base de datos está accesible.
    :return: True si la conexión es exitosa, False en caso contrario.
    """
    try:
        conn = get_connection()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return False

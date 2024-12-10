import sqlite3
import os
from functools import lru_cache

# Obtener el path absoluto de las bases de datos
def get_db_path():
    """
    Devuelve la ruta de la base de datos de RMA.
    """
    return os.path.join(os.path.dirname(__file__), '../rma.db')

def get_users_db_path():
    """
    Devuelve la ruta de la base de datos de usuarios.
    """
    return os.path.join(os.path.dirname(__file__), '../users.db')

# Crear una conexión genérica a las bases de datos
def get_connection(db_type='rma'):
    """
    Crea una conexión genérica a la base de datos especificada.
    :param db_type: Tipo de base de datos ('rma' o 'users').
    :return: Conexión SQLite.
    """
    db_path = get_db_path() if db_type == 'rma' else get_users_db_path()
    return sqlite3.connect(db_path)

# Función para ejecutar una consulta genérica
def execute_query(query, params=None, fetch_all=True, db_type='rma'):
    """
    Ejecuta una consulta SQL genérica en la base de datos especificada.
    :param query: La consulta SQL a ejecutar.
    :param params: Parámetros para la consulta (opcional).
    :param fetch_all: Indica si se deben devolver todos los resultados.
    :param db_type: Tipo de base de datos ('rma' o 'users').
    :return: Resultados de la consulta o el cursor, dependiendo del caso.
    """
    conn = get_connection(db_type)
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
@lru_cache(maxsize=10)
def get_table_data(table_name, db_type='rma'):
    """
    Obtiene todos los datos de una tabla.
    :param table_name: Nombre de la tabla.
    :param db_type: Tipo de base de datos ('rma' o 'users').
    :return: Lista de filas en la tabla.
    """
    query = f"SELECT * FROM {table_name}"
    return execute_query(query, db_type=db_type)

# Ejemplo de uso para cargar empleados
def get_employees():
    """
    Devuelve todos los empleados.
    :return: Lista de empleados.
    """
    return get_table_data("users")

def get_users():
    """
    Devuelve todos los usuarios.
    :return: Lista de usuarios.
    """
    return get_table_data("users", db_type='users')

# Verificar si la base de datos está accesible
def check_db_connection(db_type='rma'):
    """
    Verifica si la base de datos está accesible.
    :param db_type: Tipo de base de datos ('rma' o 'users').
    :return: True si la conexión es exitosa, False en caso contrario.
    """
    try:
        conn = get_connection(db_type)
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos {db_type}: {e}")
        return False

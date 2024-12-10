import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sqlite3
import os
from utils.db_utils import get_db_path
from client_fields import CLIENT_FIELDS
from employee_fields import EMPLOYEE_FIELDS

def connect_to_db():
    """Establece una conexión a la base de datos."""
    try:
        conn = sqlite3.connect(get_db_path())
        print("Conexión exitosa a la base de datos.")
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

def inspect_table_structure(table_name):
    """Inspecciona la estructura de una tabla."""
    conn = connect_to_db()
    if not conn:
        return
    
    try:
        c = conn.cursor()
        c.execute(f"PRAGMA table_info({table_name})")
        columns = c.fetchall()
        print(f"Estructura de la tabla '{table_name}':")
        for column in columns:
            print(f"- {column[1]} ({column[2]}) {'PK' if column[5] else ''}")
        return [column[1] for column in columns]  # Devuelve los nombres de las columnas
    except sqlite3.Error as e:
        print(f"Error al inspeccionar la tabla '{table_name}': {e}")
    finally:
        conn.close()

def compare_fields_with_table(table_columns, fields):
    """Compara los campos definidos con las columnas existentes en la tabla."""
    field_names = [field['name'] for field in fields]
    missing_columns = set(field_names) - set(table_columns)
    if missing_columns:
        print("Faltan las siguientes columnas en la tabla:")
        for column in missing_columns:
            print(f"- {column}")
    else:
        print("Todos los campos definidos están presentes en la tabla.")

def check_sample_data(table_name, limit=5):
    """Consulta una muestra de datos de la tabla."""
    conn = connect_to_db()
    if not conn:
        return
    
    try:
        c = conn.cursor()
        c.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
        rows = c.fetchall()
        if rows:
            print(f"Muestra de datos en la tabla '{table_name}':")
            for row in rows:
                print(row)
        else:
            print(f"No se encontraron datos en la tabla '{table_name}'.")
    except sqlite3.Error as e:
        print(f"Error al consultar datos en la tabla '{table_name}': {e}")
    finally:
        conn.close()

def suggest_sql_commands_for_missing_columns(missing_columns):
    """Genera comandos SQL para añadir columnas faltantes."""
    print("Comandos SQL sugeridos para añadir las columnas faltantes:")
    for column in missing_columns:
        print(f"ALTER TABLE rma_requests ADD COLUMN {column} TEXT;")

if __name__ == "__main__":
    table_name = "rma_requests"

    # Inspeccionar la estructura de la tabla
    table_columns = inspect_table_structure(table_name)

    # Comparar con los campos definidos
    if table_columns:
        print("\nComparando con CLIENT_FIELDS...")
        compare_fields_with_table(table_columns, CLIENT_FIELDS)

        print("\nComparando con EMPLOYEE_FIELDS...")
        compare_fields_with_table(table_columns, EMPLOYEE_FIELDS)

    # Consultar datos de ejemplo
    print("\nConsultando muestra de datos...")
    check_sample_data(table_name)

import sqlite3
import os
from datetime import datetime

# Ruta de la base de datos
DB_PATH = os.path.join(os.path.dirname(__file__), '../rma.db')

def add_timestamp_column():
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Verificar si la columna 'timestamp' existe
        c.execute("PRAGMA table_info(rma_requests)")
        columns = [row[1] for row in c.fetchall()]
        
        if 'timestamp' in columns:
            print("✅ La columna 'timestamp' ya existe.")
        else:
            # Agregar la columna 'timestamp' sin valor predeterminado
            c.execute("ALTER TABLE rma_requests ADD COLUMN timestamp DATETIME")
            conn.commit()
            print("✅ Columna 'timestamp' agregada correctamente.")

            # Poblar la columna 'timestamp' para registros existentes
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            c.execute("UPDATE rma_requests SET timestamp = ? WHERE timestamp IS NULL", (current_time,))
            conn.commit()
            print("✅ Valores de 'timestamp' inicializados para registros existentes.")
        
        # Validar los cambios
        c.execute("SELECT id, modell, name, status, assigned_taller, timestamp FROM rma_requests LIMIT 5")
        rows = c.fetchall()
        print("Muestra de registros actualizados:")
        for row in rows:
            print(row)

    except sqlite3.Error as e:
        print(f"❌ Error al actualizar la base de datos: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    add_timestamp_column()

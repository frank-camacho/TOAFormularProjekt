import os
import sqlite3

# Ruta absoluta al archivo rma.db en el directorio raíz
DB_PATH = os.path.join(os.path.dirname(__file__), 'rma.db')

def initialize_database():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Crear tabla employees
    c.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    initialize_database()

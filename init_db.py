import os
import sqlite3

# Ruta absoluta al archivo rma.db en el directorio raíz
DB_PATH = os.path.join(os.path.dirname(__file__), 'rma.db')

def initialize_database():

    conn = sqlite3.connect(DB_PATH)

    c = conn.cursor()

    conn.commit()
    conn.close()

if __name__ == '__main__':
    initialize_database()

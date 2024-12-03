import sqlite3

def check_table_schema():
    conn = sqlite3.connect('rma.db')
    c = conn.cursor()

    # Verificar columnas existentes
    c.execute("PRAGMA table_info(rma_requests);")
    columns = c.fetchall()

    conn.close()
    print("Esquema actual de la tabla rma_requests:")
    for col in columns:
        print(col)

if __name__ == "__main__":
    check_table_schema()

def update_table_schema():
    conn = sqlite3.connect('rma.db')
    c = conn.cursor()

    # Intentar agregar nuevas columnas
    try:
        c.execute("ALTER TABLE rma_requests ADD COLUMN status TEXT DEFAULT 'Neu';")
        c.execute("ALTER TABLE rma_requests ADD COLUMN assigned_taller TEXT DEFAULT 'Unassigned';")
        print("Columnas agregadas exitosamente.")
    except sqlite3.OperationalError as e:
        print(f"Error al agregar columnas (posiblemente ya existen): {e}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_table_schema()

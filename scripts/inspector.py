import sqlite3

def inspect_database():
    conn = sqlite3.connect('../rma.db')  # Asegúrate de ajustar el path si es necesario
    c = conn.cursor()

    # Mostrar todas las tablas
    print("Tablas en la base de datos:")
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    for table in tables:
        print(f"- {table[0]}")

    # Inspeccionar la estructura de la tabla rma_requests
    print("\nEstructura de la tabla rma_requests:")
    c.execute("PRAGMA table_info(rma_requests);")
    columns = c.fetchall()
    for col in columns:
        print(f"- {col[1]} ({col[2]})")

    conn.close()

if __name__ == "__main__":
    inspect_database()

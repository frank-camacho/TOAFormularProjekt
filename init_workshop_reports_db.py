import sqlite3

def init_workshop_reports_db():
    db_path = "workshop_reports.db"
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Crear tabla para los reportes del taller
    c.execute('''
    CREATE TABLE IF NOT EXISTS workshop_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rma_id INTEGER NOT NULL,
        comments TEXT,
        cost REAL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

    print("Base de datos 'workshop_reports.db' inicializada correctamente.")

# Ejecutar el script
if __name__ == "__main__":
    init_workshop_reports_db()

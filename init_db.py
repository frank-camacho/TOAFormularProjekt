import sqlite3
from utils.db_utils import get_db_path

def create_tables():
    """
    Crea las tablas necesarias para la base de datos si no existen.
    """
    try:
        with sqlite3.connect(get_db_path()) as conn:
            c = conn.cursor()

            # Tabla para solicitudes RMA
            c.execute('''
                CREATE TABLE IF NOT EXISTS rma_requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    kundennummer TEXT NOT NULL,
                    projektreferenz TEXT,
                    modell TEXT NOT NULL,
                    seriennummer TEXT NOT NULL,
                    name TEXT NOT NULL,
                    adresse TEXT NOT NULL,
                    plz TEXT NOT NULL,
                    telefon TEXT NOT NULL,
                    email TEXT NOT NULL,
                    anmeldedatum TEXT NOT NULL,
                    fehlbeschreibung TEXT NOT NULL,
                    reparaturkosten REAL DEFAULT 0.0,
                    status TEXT DEFAULT 'Neu'
                )
            ''')
            print("[DEBUG] Tabla `rma_requests` creada o ya existía.")

            # Tabla para reportes del taller
            c.execute('''
                CREATE TABLE IF NOT EXISTS workshop_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    rma_id INTEGER NOT NULL,
                    report_date TEXT NOT NULL,
                    actions TEXT NOT NULL,
                    material_id INTEGER,
                    FOREIGN KEY (rma_id) REFERENCES rma_requests (id)
                )
            ''')
            print("[DEBUG] Tabla `workshop_reports` creada o ya existía.")

            # Tabla para la disponibilidad de materiales
            c.execute('''
                CREATE TABLE IF NOT EXISTS sap_material_availability (
                    material_id INTEGER PRIMARY KEY,
                    material_status TEXT NOT NULL
                )
            ''')
            print("[DEBUG] Tabla `sap_material_availability` creada o ya existía.")

            conn.commit()
    except sqlite3.Error as e:
        print(f"[ERROR] Error al crear las tablas: {e}")

if __name__ == "__main__":
    create_tables()
    print("[DEBUG] Inicialización de la base de datos completada.")

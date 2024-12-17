import sqlite3
import os
from datetime import datetime

def get_workshop_db_path():
    return os.path.join(os.path.dirname(__file__), "../workshop_reports.db")

def seed_extended_workshop_data():
    """Inserta datos de prueba en la tabla 'workshop_reports'."""
    db_path = get_workshop_db_path()
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # Datos de prueba para workshop_reports
        seed_data = [
            (12, "Techniker A", "In Arbeit", "Teil A, Teil B", 3.5, "Weitere Tests notwendig", "ZOR12345", "LS987654", "Reparatur begonnen", 100.0, datetime.now().strftime("%Y-%m-%d")),
            (12, "Techniker B", "Abgeschlossen", "Teil C", 5.0, "Reparatur abgeschlossen", "ZOR54321", "LS123456", "Endprüfung erfolgreich", 200.0, datetime.now().strftime("%Y-%m-%d")),
            (13, "Techniker C", "Wartend", "Teil D", 2.0, "Auf Ersatzteile warten", "ZOR67890", "LS567890", "Warten auf Material", 50.0, datetime.now().strftime("%Y-%m-%d"))
        ]

        # Insertar datos en la tabla
        c.executemany("""
            INSERT INTO workshop_reports (
                rma_id, technician_name, repair_status, used_parts, duration, next_steps, ZOR, Lieferscheinnummer, 
                comments, cost, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, seed_data)
        conn.commit()
        print("[SUCCESS] Datos extendidos de prueba insertados en 'workshop_reports'.")

    except sqlite3.Error as e:
        print(f"[ERROR] Error al insertar datos de prueba: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    seed_extended_workshop_data()

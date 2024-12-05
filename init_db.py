import sqlite3

# Definición de los encabezados y sus tipos de datos
FIELDS = {
    "rma": "INTEGER PRIMARY KEY AUTOINCREMENT",
    "kunde": "TEXT NOT NULL",
    "kundennr": "TEXT NOT NULL",
    "artikel": "TEXT NOT NULL",
    "seriennummer": "TEXT NOT NULL",
    "status": "TEXT NOT NULL",
    "globaler_status": "TEXT",
    "lager_status": "TEXT",
    "werkstatt_status": "TEXT",
    "management_status": "TEXT",
    "vergeben_am": "TEXT",
    "eingang_am": "TEXT",
    "abgeschlossen_am": "TEXT",
    "datum_reparatur": "TEXT",
    "ausgangsdatum": "TEXT",
    "adresse": "TEXT NOT NULL",
    "plz": "TEXT NOT NULL",
    "telefon": "TEXT NOT NULL",
    "email": "TEXT NOT NULL",
    "fehlerangabe_kunde": "TEXT NOT NULL",
    "reparaturmassnahme": "TEXT",
    "kommentar": "TEXT"
}

def initialize_database():
    # Conexión a la base de datos
    conn = sqlite3.connect('rma.db')
    c = conn.cursor()

    # Construcción dinámica del comando CREATE TABLE
    fields_definition = ", ".join([f"{name} {type}" for name, type in FIELDS.items()])
    create_table_query = f"CREATE TABLE IF NOT EXISTS rma_requests ({fields_definition});"
    
    # Creación de la tabla
    c.execute(create_table_query)
    conn.commit()
    conn.close()
    print("Base de datos inicializada correctamente con los encabezados correctos.")

if __name__ == "__main__":
    initialize_database()

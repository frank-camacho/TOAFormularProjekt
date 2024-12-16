import sqlite3
from utils.db_utils import get_db_path

def create_client_view():
    """
    Crea la vista `Client_View` en la base de datos.
    """
    view_query = """
    CREATE VIEW IF NOT EXISTS Client_View AS
    SELECT 
        rma.id AS RMA_ID,
        rma.kundennummer AS Customer_ID,
        rma.projektreferenz AS Project_Reference,
        rma.modell AS Model,
        rma.seriennummer AS Serial_Number,
        rma.status AS Status,
        rma.anmeldedatum AS Registration_Date,
        wr.report_date AS Last_Workshop_Update,
        wr.actions AS Workshop_Actions,
        sap.material_status AS Material_Availability_Status
    FROM RMA_DB rma
    LEFT JOIN Workshop_Reports wr ON rma.id = wr.rma_id
    LEFT JOIN SAP_Material_Availability sap ON wr.material_id = sap.material_id;
    """
    try:
        with sqlite3.connect(get_db_path()) as conn:
            c = conn.cursor()
            c.execute(view_query)
            conn.commit()
        print("[DEBUG] La vista `Client_View` ha sido creada o ya existía.")
    except sqlite3.Error as e:
        print(f"[ERROR] Error al crear la vista `Client_View`: {e}")

def get_client_data(kundennummer):
    """
    Consulta los datos de la vista `Client_View` para un cliente específico.
    :param kundennummer: ID del cliente (username).
    :return: Lista de datos filtrados por cliente.
    """
    query = """
    SELECT * 
    FROM Client_View
    WHERE Customer_ID = ?;
    """
    try:
        with sqlite3.connect(get_db_path()) as conn:
            c = conn.cursor()
            c.execute(query, (kundennummer,))
            results = c.fetchall()
        print(f"[DEBUG] Datos obtenidos para el cliente {kundennummer}: {results}")
        return results
    except sqlite3.Error as e:
        print(f"[ERROR] Error al consultar la vista `Client_View` para el cliente {kundennummer}: {e}")
        return []

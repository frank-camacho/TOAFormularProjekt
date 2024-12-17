from flask import Blueprint, render_template, request, redirect, g
import os
import sqlite3
from client_fields import CLIENT_FIELDS
from flask import jsonify
from utils.db_utils import get_db_path
from utils.routes_map import routes_map
from client_fields import CLIENT_FIELDS

# Crear un blueprint para las rutas de clientes
client_bp = Blueprint('client', __name__, url_prefix='/client')

@client_bp.route('/register_rma', methods=['GET', 'POST'])
def register_rma():
    try:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()

        if request.method == 'POST':
            # Recibir datos del formulario solo para los campos permitidos a los clientes
            data = {field['name']: request.form.get(field['name'], '') for field in CLIENT_FIELDS}

            # Insertar datos en la tabla rma_requests con valores predeterminados
            c.execute('''
                INSERT INTO rma_requests (
                    kundennummer, name, adresse, plz, telefon, email, anmeldedatum,
                    artikel, seriennummer, fehlbeschreibung, kommentar, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data['kundennummer'], data['name'], data['adresse'], data['plz'], data['telefon'],
                data['email'], data['anmeldedatum'], data['artikel'], data['seriennummer'],
                data['fehlbeschreibung'], data.get('kommentar', ''), "Neu"
            ))
            conn.commit()

            # Redirigir con un mensaje de éxito
            return render_template('confirmation.html', message="Ihre Reparaturanfrage wurde erfolgreich registriert!")

        # GET request: Renderizar el formulario vacío
        return render_template('register_rma.html', fields=CLIENT_FIELDS)

    except sqlite3.Error as e:
        print(f"[ERROR] Fehler bei der Datenbankabfrage: {e}")
        return f"Fehler bei der Datenbankabfrage: {e}", 500
    finally:
        conn.close()

@client_bp.route('/consulta', methods=['GET', 'POST'])
def consulta():
    try:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()

        if request.method == 'POST':
            # Obtener el número de cliente del formulario
            kundennummer = request.form.get('kundennummer', '').strip()

            if not kundennummer:
                return render_template('consulta.html', mensaje="Bitte geben Sie eine gültige Kundennummer ein.")

            # Consultar los registros que coinciden con el número de cliente
            c.execute('SELECT * FROM rma_requests WHERE kundennummer = ?', (kundennummer,))
            resultados = c.fetchall()

            if not resultados:
                return render_template('consulta.html', mensaje="Keine Ergebnisse gefunden.")

            # Obtener nombres de columnas reales desde la base de datos
            c.execute("PRAGMA table_info(rma_requests)")
            columnas = [info[1] for info in c.fetchall()]

            return render_template('consulta.html', resultados=resultados, columnas=columnas)

        # GET request: Renderizar la página de consulta vacía
        return render_template('consulta.html')

    except sqlite3.Error as e:
        return f"Fehler bei der Datenbankabfrage: {e}", 500
    finally:
        conn.close()

@client_bp.route('/client_dashboard', methods=['GET'])
def client_dashboard():
    if g.current_user['role'] != 'client':
        print("[ERROR] Acceso denegado al dashboard de clientes.")
        return redirect(routes_map['shared_login']())

    kundennummer = g.current_user['username']
    try:
        with sqlite3.connect(get_db_path()) as conn:
            c = conn.cursor()

            # Seleccionar columnas relevantes + 'id'
            column_names = ['id'] + [field['name'] for field in CLIENT_FIELDS]  # Agregamos 'id' al inicio
            column_labels = ['RMA ID'] + [field['label'] for field in CLIENT_FIELDS]  # Etiqueta para ID

            query = f"""
                SELECT {', '.join(column_names)}
                FROM rma_requests
                WHERE kundennummer = ?;
            """
            c.execute(query, (kundennummer,))
            rmas = c.fetchall()

        return render_template('client_dashboard.html', column_labels=column_labels, rmas=rmas)

    except sqlite3.Error as e:
        print(f"[ERROR] Error al consultar los registros: {e}")
        return render_template('client_dashboard.html', column_labels=[], rmas=[], error_message="Fehler bei der Datenbankabfrage.")

def get_workshop_db_path():
    return os.path.join(os.path.dirname(__file__), '../workshop_reports.db')

@client_bp.route('/repair_history/<int:rma_id>', methods=['GET'])
def get_repair_history(rma_id):
    """
    Devuelve el historial de reparaciones en formato JSON para un RMA específico.
    """
    try:
        print(f"[DEBUG] Obteniendo historial extendido para RMA ID: {rma_id}")
        with sqlite3.connect(get_workshop_db_path()) as conn:
            c = conn.cursor()
            c.execute("""
                SELECT rma_id, technician_name, repair_status, used_parts, duration, next_steps, ZOR, Lieferscheinnummer, 
                       comments, cost, created_at
                FROM workshop_reports
                WHERE rma_id = ?;
            """, (rma_id,))
            history = c.fetchall()

        # Convertir resultados a JSON
        history_data = [
            {
                "rma_id": row[0],
                "technician_name": row[1],
                "repair_status": row[2],
                "used_parts": row[3],
                "duration": row[4],
                "next_steps": row[5],
                "ZOR": row[6],
                "Lieferscheinnummer": row[7],
                "comments": row[8],
                "cost": row[9],
                "created_at": row[10]
            } 
            for row in history
        ]
        print(f"[DEBUG] Datos enviados al cliente: {history_data}")
        return jsonify(history_data)

    except sqlite3.Error as e:
        print(f"[ERROR] Error al obtener el historial extendido: {e}")
        return jsonify({"error": "Fehler bei der Abfrage"}), 500

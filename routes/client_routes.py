# routes/client_routes.py

from flask import Blueprint, render_template, request, redirect
import sqlite3
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
            # Recibir datos del formulario
            data = {field['name']: request.form.get(field['name'], '') for field in CLIENT_FIELDS}

            # Insertar datos en la tabla rma_requests con valores predeterminados
            c.execute('''
                INSERT INTO rma_requests (
                    kundennummer, modell, seriennummer, name, adresse, plz, telefon, email,
                    anmeldedatum, fehlbeschreibung, reparaturkosten, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.get('kundennummer', ''), data.get('product', ''), data.get('serial_number', ''),
                data.get('customer', ''), data.get('adresse', ''), data.get('plz', ''),
                data.get('telefon', ''), data.get('email', ''), data.get('anmeldedatum', ''),
                data.get('issue_description', ''), 0.0, "Neu"
            ))
            conn.commit()

            # Redirigir con un mensaje de éxito
            return render_template('confirmation.html', message="Ihre Reparaturanfrage wurde erfolgreich registriert!")

        # GET request: Renderizar el formulario vacío
        return render_template('register_rma.html', fields=CLIENT_FIELDS)

    except sqlite3.Error as e:
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

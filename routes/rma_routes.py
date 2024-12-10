# routes/rma_routes.py

from flask import Blueprint, render_template, request, redirect, g
from utils.routes_map import routes_map
import sqlite3
from utils.db_utils import get_db_path
from employee_fields import EMPLOYEE_FIELDS
from client_fields import CLIENT_FIELDS

# Crear un blueprint para las rutas RMA
rma_bp = Blueprint('rma', __name__, url_prefix='/rma')

@rma_bp.route('/new_rma', methods=['GET', 'POST'])
def new_rma():
    if not g.current_user:
        return redirect(routes_map['login']())

    if request.method == 'POST':
        try:
            conn = sqlite3.connect(get_db_path())
            c = conn.cursor()
            # Recopilar datos del formulario
            data = {field['name']: request.form.get(field['name'], '') for field in EMPLOYEE_FIELDS}
            c.execute('''
                INSERT INTO rma_requests (
                    kundennummer, modell, seriennummer, name, adresse, plz, telefon, email,
                    anmeldedatum, fehlbeschreibung, reparaturkosten, status, assigned_taller
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.get('kundennummer', ''), data.get('product', ''), data.get('serial_number', ''),
                data.get('customer', ''), data.get('adresse', ''), data.get('plz', ''),
                data.get('telefon', ''), data.get('email', ''), data.get('anmeldedatum', ''),
                data.get('issue_description', ''), float(data.get('repair_cost', 0)),
                data.get('status', 'Neu'), data.get('assigned_taller', '')
            ))
            conn.commit()
            return render_template('confirmation.html', message="Neues RMA erfolgreich erstellt!")
        except sqlite3.Error as e:
            return f"Error al guardar datos: {e}", 500
        finally:
            conn.close()

    return render_template('new_rma.html', fields=EMPLOYEE_FIELDS)

@rma_bp.route('/submit_rma', methods=['POST'])
def submit_rma():
    try:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='rma_requests';")
        if not c.fetchone():
            return "Error: La tabla 'rma_requests' no existe.", 500

        data = {field['name']: request.form.get(field['name'], '') for field in CLIENT_FIELDS}
        c.execute('''
            INSERT INTO rma_requests (
                kundennummer, modell, seriennummer, name, adresse, plz, telefon, email,
                anmeldedatum, fehlbeschreibung, reparaturkosten, zustimmung
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('kundennummer', ''), data.get('product', ''), data.get('serial_number', ''),
            data.get('customer', ''), data.get('adresse', ''), data.get('plz', ''),
            data.get('telefon', ''), data.get('email', ''), data.get('anmeldedatum', ''),
            data.get('issue_description', ''), float(data.get('repair_cost', 0)),
            data.get('zustimmung', 'Nein')
        ))
        conn.commit()
    except sqlite3.Error as e:
        return f"Error al guardar datos: {e}", 500
    finally:
        conn.close()

    return render_template('confirmation.html', message="RMA erfolgreich eingereicht!")

# Redirecciones a rutas existentes para evitar duplicidad de código
@rma_bp.route('/register_rma', methods=['GET', 'POST'])
def register_rma_redirect():
    return redirect(routes_map['register_rma']())

@rma_bp.route('/consulta', methods=['GET', 'POST'])
def consulta_redirect():
    return redirect(routes_map['consulta']())

@rma_bp.route('/update_status', methods=['POST'])
def update_status_redirect():
    return redirect(routes_map['update_status']())

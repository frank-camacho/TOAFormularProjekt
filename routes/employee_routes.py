# routes/employee_routes.py

from flask import Blueprint, render_template, request, redirect, g
import sqlite3
from utils.db_utils import get_db_path
from utils.routes_map import routes_map
from employee_fields import EMPLOYEE_FIELDS

# Crear un blueprint para las rutas de empleados
employee_bp = Blueprint('employee', __name__, url_prefix='/employee')

@employee_bp.route('/dashboard', methods=['GET'])
def employee_dashboard():
    if not g.current_user or g.current_user['role'] != 'employee':
        return redirect(routes_map['login']())

    try:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()

        # Obtener los primeros 5 registros con estado "Neu"
        c.execute("SELECT id, modell, name, status, assigned_taller FROM rma_requests WHERE status = 'Neu' LIMIT 5")
        requests = [
            {"id": row[0], "modell": row[1], "name": row[2], "status": row[3], "assigned_taller": row[4]}
            for row in c.fetchall()
        ]

        # Calcular estadísticas básicas
        c.execute("SELECT COUNT(*) FROM rma_requests")
        total_rmas = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM rma_requests WHERE status = 'Neu'")
        new = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM rma_requests WHERE status = 'In Arbeit'")
        in_progress = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM rma_requests WHERE status = 'Abgeschlossen'")
        completed = c.fetchone()[0]

        stats = {
            "total_rmas": total_rmas,
            "new": new,
            "in_progress": in_progress,
            "completed": completed,
        }

        return render_template('employee_dashboard.html', requests=requests, stats=stats)

    except sqlite3.Error as e:
        return f"Error al acceder a la base de datos: {e}", 500
    finally:
        conn.close()

@employee_bp.route('/new_requests', methods=['GET'])
def new_requests():
    if not g.current_user or g.current_user['role'] != 'employee':
        return redirect(routes_map['login']())

    try:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()

        # Obtener registros con estado "Neu"
        c.execute("SELECT id, modell, name, status, assigned_taller FROM rma_requests WHERE status = 'Neu'")
        requests = [
            {"id": row[0], "modell": row[1], "name": row[2], "status": row[3], "assigned_taller": row[4]}
            for row in c.fetchall()
        ]

        return render_template('new_requests.html', requests=requests)

    except sqlite3.Error as e:
        return f"Error al acceder a la base de datos: {e}", 500
    finally:
        conn.close()

@employee_bp.route('/edit_data/<int:rma_id>', methods=['GET', 'POST'])
def edit_data(rma_id):
    if not g.current_user or g.current_user['role'] != 'employee':
        return redirect(routes_map['login']())

    try:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()

        if request.method == 'POST':
            # Recibir datos del formulario
            data = {field['name']: request.form.get(field['name'], '') for field in EMPLOYEE_FIELDS}

            c.execute('''
                UPDATE rma_requests
                SET kundennummer = ?, modell = ?, seriennummer = ?, name = ?, adresse = ?, plz = ?, telefon = ?,
                    email = ?, anmeldedatum = ?, fehlbeschreibung = ?, reparaturkosten = ?, status = ?, assigned_taller = ?
                WHERE id = ?
            ''', (
                data.get('kundennummer', ''), data.get('product', ''), data.get('serial_number', ''),
                data.get('customer', ''), data.get('adresse', ''), data.get('plz', ''),
                data.get('telefon', ''), data.get('email', ''), data.get('anmeldedatum', ''),
                data.get('issue_description', ''), float(data.get('repair_cost', 0)),
                data.get('status', ''), data.get('assigned_taller', ''), rma_id
            ))
            conn.commit()
            return redirect(routes_map['employee_dashboard']())

        # Obtener datos de la RMA
        c.execute('SELECT * FROM rma_requests WHERE id = ?', (rma_id,))
        row = c.fetchone()

        if not row:
            return "Kein RMA gefunden", 404

        rma_data = {EMPLOYEE_FIELDS[i]['name']: row[i] for i in range(len(EMPLOYEE_FIELDS))}
        return render_template('edit_data.html', fields=EMPLOYEE_FIELDS, rma_data=rma_data, rma_id=rma_id)

    except sqlite3.Error as e:
        return f"Error al acceder a la base de datos: {e}", 500
    finally:
        conn.close()

@employee_bp.route('/update_status', methods=['POST'])
def update_status():
    if not g.current_user or g.current_user['role'] != 'employee':
        return redirect(routes_map['login']())

    try:
        rma_id = request.form['id']
        new_status = request.form['status']

        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        c.execute('UPDATE rma_requests SET status = ? WHERE id = ?', (new_status, rma_id))
        conn.commit()

        return redirect(routes_map['employee_dashboard']())
    except sqlite3.Error as e:
        return f"Error al actualizar el estado: {e}", 500
    finally:
        conn.close()

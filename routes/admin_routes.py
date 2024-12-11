# routes/admin_routes.py

from flask import Blueprint, render_template, request, redirect, g, session
from werkzeug.security import generate_password_hash
import sqlite3
from utils.db_utils import get_users_db_path
from utils.routes_map import routes_map

# Crear un blueprint para las rutas de administración
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Middleware para verificar si el usuario es administrador
@admin_bp.before_request
def admin_required():
    if not session.get('user_id') or session.get('role') != 'admin':
        return redirect(routes_map['shared_login']())

@admin_bp.route('/employees', methods=['GET'])
def manage_employees():
    try:
        conn = sqlite3.connect(get_users_db_path())
        c = conn.cursor()
        c.execute('SELECT id, username, role FROM users')
        users = c.fetchall()
        return render_template('admin_employees.html', users=users)
    except sqlite3.Error as e:
        return f"Fehler bei der Datenbankabfrage: {e}", 500
    finally:
        conn.close()

@admin_bp.route('/employees/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        role = request.form['role']

        # Validación básica
        if not username or not password or role not in ['admin', 'employee']:
            return render_template('add_employee.html', error_message="Ungültige Eingabe.")

        try:
            hashed_password = generate_password_hash(password)
            conn = sqlite3.connect(get_users_db_path())
            c = conn.cursor()
            c.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                      (username, hashed_password, role))
            conn.commit()
            return redirect(routes_map['admin_manage_employees']())
        except sqlite3.IntegrityError:
            return render_template('add_employee.html', error_message="Benutzername existiert bereits.")
        finally:
            conn.close()

    return render_template('add_employee.html')

@admin_bp.route('/employees/edit/<int:employee_id>', methods=['GET', 'POST'])
def edit_employee(employee_id):
    try:
        conn = sqlite3.connect(get_users_db_path())
        c = conn.cursor()

        if request.method == 'POST':
            username = request.form['username'].strip()
            password = request.form['password']
            role = request.form['role']

            # Validación básica
            if not username or not password or role not in ['admin', 'employee']:
                return render_template('edit_employee.html', error_message="Ungültige Eingabe.")

            hashed_password = generate_password_hash(password)
            c.execute('''
                UPDATE users SET username = ?, password = ?, role = ? WHERE id = ?
            ''', (username, hashed_password, role, employee_id))
            conn.commit()
            return redirect(routes_map['admin_manage_employees']())

        c.execute('SELECT id, username, role FROM users WHERE id = ?', (employee_id,))
        employee = c.fetchone()
        if not employee:
            return "Benutzer nicht gefunden.", 404

        return render_template('edit_employee.html', employee=employee)
    except sqlite3.Error as e:
        return f"Fehler beim Bearbeiten des Benutzers: {e}", 500
    finally:
        conn.close()

@admin_bp.route('/employees/delete/<int:employee_id>', methods=['POST'])
def delete_employee(employee_id):
    try:
        conn = sqlite3.connect(get_users_db_path())
        c = conn.cursor()
        c.execute('DELETE FROM users WHERE id = ?', (employee_id,))
        conn.commit()
        return redirect(routes_map['admin_manage_employees']())
    except sqlite3.Error as e:
        return f"Fehler beim Löschen des Benutzers: {e}", 500
    finally:
        conn.close()

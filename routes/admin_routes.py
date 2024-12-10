# routes/admin_routes.py

from flask import Blueprint, render_template, request, redirect, g
from werkzeug.security import generate_password_hash
import sqlite3
from utils.db_utils import get_db_path
from utils.routes_map import routes_map

# Crear un blueprint para las rutas de administración
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Middleware para verificar si el usuario es administrador
def admin_required():
    if not g.current_user or g.current_user['role'] != 'admin':
        return redirect(routes_map['login']())

@admin_bp.route('/employees', methods=['GET'])
def manage_employees():
    response = admin_required()
    if response:
        return response

    try:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        c.execute('SELECT id, username, role FROM employees')
        users = c.fetchall()
        return render_template('admin_employees.html', users=users)
    except sqlite3.Error as e:
        return f"Fehler bei der Datenbankabfrage: {e}", 500
    finally:
        conn.close()

@admin_bp.route('/employees/add', methods=['GET', 'POST'])
def add_employee():
    response = admin_required()
    if response:
        return response

    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        role = request.form['role']

        try:
            conn = sqlite3.connect(get_db_path())
            c = conn.cursor()
            c.execute('INSERT INTO employees (username, password, role) VALUES (?, ?, ?)',
                      (username, password, role))
            conn.commit()
            return redirect(routes_map['manage_employees']())
        except sqlite3.IntegrityError:
            return "Fehler: Der Benutzername existiert bereits.", 400
        finally:
            conn.close()

    return render_template('add_employee.html')

@admin_bp.route('/employees/edit/<int:employee_id>', methods=['GET', 'POST'])
def edit_employee(employee_id):
    response = admin_required()
    if response:
        return response

    try:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        if request.method == 'POST':
            username = request.form['username']
            password = generate_password_hash(request.form['password'])
            role = request.form['role']

            c.execute('''
                UPDATE employees SET username = ?, password = ?, role = ? WHERE id = ?
            ''', (username, password, role, employee_id))
            conn.commit()
            return redirect(routes_map['manage_employees']())

        c.execute('SELECT * FROM employees WHERE id = ?', (employee_id,))
        employee = c.fetchone()
        return render_template('edit_employee.html', employee=employee)
    except sqlite3.Error as e:
        return f"Fehler beim Bearbeiten des Benutzers: {e}", 500
    finally:
        conn.close()

@admin_bp.route('/employees/delete/<int:employee_id>', methods=['POST'])
def delete_employee(employee_id):
    response = admin_required()
    if response:
        return response

    try:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        c.execute('DELETE FROM employees WHERE id = ?', (employee_id,))
        conn.commit()
        return redirect(routes_map['manage_employees']())
    except sqlite3.Error as e:
        return f"Fehler beim Löschen des Benutzers: {e}", 500
    finally:
        conn.close()

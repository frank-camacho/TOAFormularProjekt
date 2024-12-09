from flask import render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from admin_module.models import admin_required
import sqlite3
import os
from datetime import datetime
from client_fields import CLIENT_FIELDS
from employee_fields import EMPLOYEE_FIELDS

# Construir el path absoluto de la base de datos
DB_PATH = os.path.join(os.path.dirname(__file__), '../rma.db')

def register_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            conn = sqlite3.connect('rma.db')
            c = conn.cursor()

            # Consultar la base de datos para verificar las credenciales
            c.execute('SELECT id, role FROM employees WHERE username = ? AND password = ?', (username, password))
            user = c.fetchone()
            conn.close()

            if user:
                # Almacenar información del usuario en la sesión
                session['user_id'] = user[0]
                session['role'] = user[1]

                # Redirigir al portal correspondiente
                if user[1] == 'admin':
                    return render_template('login.html', is_admin=True)
                else:
                    return redirect('/employee_dashboard')
            else:
                return render_template('login.html', error_message="Ungültige Anmeldedaten.")

        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.pop('employee_id', None)
        return redirect('/login')

    @app.route('/admin/employees', methods=['GET'])
    def manage_employees():
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute('SELECT id, username, role FROM employees')
            users = c.fetchall()
            return render_template('admin_employees.html', users=users)
        except sqlite3.Error as e:
            return f"Fehler bei der Datenbankabfrage: {e}", 500
        finally:
            conn.close()

    @app.route('/admin/employees/add', methods=['GET', 'POST'])
    def add_employee():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            role = request.form['role']
            try:
                conn = sqlite3.connect(DB_PATH)
                c = conn.cursor()
                c.execute('INSERT INTO employees (username, password, role) VALUES (?, ?, ?)', 
                        (username, password, role))
                conn.commit()
            except sqlite3.IntegrityError:
                return "Fehler: Der Benutzername existiert bereits.", 400
            finally:
                conn.close()
            return redirect(url_for('manage_employees'))

        return render_template('add_employee.html')

    @app.route('/admin/employees/edit/<int:employee_id>', methods=['GET', 'POST'])
    def edit_employee(employee_id):
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                role = request.form['role']

                c.execute('''
                    UPDATE employees SET username = ?, password = ?, role = ? WHERE id = ?
                ''', (username, password, role, employee_id))
                conn.commit()
                return redirect(url_for('manage_employees'))

            c.execute('SELECT * FROM employees WHERE id = ?', (employee_id,))
            employee = c.fetchone()
            return render_template('edit_employee.html', employee=employee)
        except sqlite3.Error as e:
            return f"Fehler beim Bearbeiten des Benutzers: {e}", 500
        finally:
            conn.close()

    @app.route('/admin/employees/delete/<int:employee_id>', methods=['POST'])
    def delete_employee(employee_id):
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute('DELETE FROM employees WHERE id = ?', (employee_id,))
            conn.commit()
            return redirect(url_for('manage_employees'))
        except sqlite3.Error as e:
            return f"Fehler beim Löschen des Benutzers: {e}", 500
        finally:
            conn.close()

    @app.route('/submit_rma', methods=['POST'])
    def submit_rma():
        try:
            conn = sqlite3.connect('rma.db')
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

    @app.route('/new_rma', methods=['GET', 'POST'])
    def new_rma():
        if request.method == 'POST':
            # Recopilar los datos del formulario
            data = {field['name']: request.form.get(field['name'], '') for field in EMPLOYEE_FIELDS}

            try:
                conn = sqlite3.connect('rma.db')
                c = conn.cursor()
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
            except sqlite3.Error as e:
                return f"Error al guardar los datos en la base de datos: {e}", 500
            finally:
                conn.close()

            return render_template('confirmation.html', message="Neues RMA erfolgreich erstellt!")
        
        return render_template('new_rma.html', fields=EMPLOYEE_FIELDS)

    @app.route('/consulta', methods=['GET', 'POST'])
    def consulta():
        if request.method == 'POST':
            # Obtener el número de cliente del formulario
            kundennummer = request.form.get('kundennummer', '').strip()
            
            if not kundennummer:
                return render_template('consulta.html', mensaje="Bitte geben Sie eine gültige Kundennummer ein.")

            # Conectar a la base de datos
            conn = sqlite3.connect('rma.db')
            c = conn.cursor()

            try:
                # Consultar los registros que coinciden con el número de cliente
                c.execute('SELECT * FROM rma_requests WHERE kundennummer = ?', (kundennummer,))
                resultados = c.fetchall()

                if not resultados:
                    return render_template('consulta.html', mensaje="Keine Ergebnisse gefunden.")

                # Obtener nombres de columnas reales desde la base de datos
                c.execute("PRAGMA table_info(rma_requests)")
                columnas = [info[1] for info in c.fetchall()]  # Obtener nombres de columnas directamente

                return render_template('consulta.html', resultados=resultados, columnas=columnas)

            except sqlite3.Error as e:
                return f"Fehler bei der Datenbankabfrage: {e}", 500

            finally:
                conn.close()

        # GET request: Renderizar la página de consulta vacía
        return render_template('consulta.html')

    @app.route('/register_rma', methods=['GET', 'POST'])
    def register_rma():
        try:
            conn = sqlite3.connect(DB_PATH)  # Utilizando la constante DB_PATH
            c = conn.cursor()

            if request.method == 'POST':
                # Recibir datos del formulario
                data = {field['name']: request.form.get(field['name'], '') for field in CLIENT_FIELDS}

                # Insertar datos en la tabla rma_requests
                placeholders = ', '.join('?' for _ in CLIENT_FIELDS)
                columns = ', '.join(field['name'] for field in CLIENT_FIELDS)
                query = f'INSERT INTO rma_requests ({columns}) VALUES ({placeholders})'
                c.execute(query, tuple(data.values()))
                conn.commit()

                # Redirigir con un mensaje de éxito
                return render_template('confirmation.html', message="Ihre Reparaturanfrage wurde erfolgreich registriert!")

            # GET request: Renderizar el formulario vacío
            return render_template('register_rma.html', fields=CLIENT_FIELDS)

        except sqlite3.Error as e:
            return f"Fehler bei der Datenbankabfrage: {e}", 500
        finally:
            conn.close()

    @app.route('/employee_dashboard', methods=['GET'])
    def employee_dashboard():
        conn = sqlite3.connect('rma.db')
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

        conn.close()
        return render_template('employee_dashboard.html', requests=requests, stats=stats)

    @app.route('/new_repair', methods=['GET', 'POST'])
    def new_repair():
        if request.method == 'POST':
            data = {field['name']: request.form.get(field['name'], '') for field in EMPLOYEE_FIELDS}
            try:
                conn = sqlite3.connect('rma.db')
                c = conn.cursor()
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
            except sqlite3.Error as e:
                return f"Error al guardar datos: {e}", 500
            finally:
                conn.close()

            return render_template('confirmation.html', message="Neue Reparatur erfolgreich registriert!", is_employee=True)

        return render_template('new_repair.html', fields=EMPLOYEE_FIELDS)

    @app.route('/new_requests', methods=['GET'])
    def new_requests():
        try:
            # Conexión a la base de datos
            conn = sqlite3.connect('rma.db')
            c = conn.cursor()

            # Obtener los registros con estado "Neu"
            c.execute("SELECT id, modell, name, status, assigned_taller FROM rma_requests WHERE status = 'Neu' LIMIT 5")
            rows = c.fetchall()

            # Convertir los registros a una lista de diccionarios
            requests = [
                {"id": row[0], "modell": row[1], "name": row[2], "status": row[3], "assigned_taller": row[4]}
                for row in rows
            ]
            conn.close()

            # Renderizar la plantilla con los datos obtenidos
            return render_template('new_requests.html', requests=requests)

        except sqlite3.Error as e:
            return f"Error al acceder a la base de datos: {e}", 500

    @app.route('/edit_data/<int:rma_id>', methods=['GET', 'POST'])
    def edit_data(rma_id):
        conn = sqlite3.connect('rma.db')
        c = conn.cursor()
        if request.method == 'POST':
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
            conn.close()
            return redirect('/employee_dashboard')

        c.execute('SELECT * FROM rma_requests WHERE id = ?', (rma_id,))
        row = c.fetchone()
        conn.close()

        if not row:
            return "Kein RMA gefunden", 404

        rma_data = {EMPLOYEE_FIELDS[i]['name']: row[i] for i in range(len(EMPLOYEE_FIELDS))}
        return render_template('edit_data.html', fields=EMPLOYEE_FIELDS, rma_data=rma_data, rma_id=rma_id)

    @app.route('/update_status', methods=['POST'])
    def update_status():
        rma_id = request.form['id']
        new_status = request.form['status']
        try:
            conn = sqlite3.connect('rma.db')
            c = conn.cursor()
            c.execute('UPDATE rma_requests SET status = ? WHERE id = ?', (new_status, rma_id))
            conn.commit()
        except sqlite3.Error as e:
            return f"Error al actualizar el estado: {e}", 500
        finally:
            conn.close()

        return redirect('/employee_dashboard')

    @app.route('/today', methods=['GET'])
    def today():
        fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return {"fecha_hora": fecha_hora_actual}

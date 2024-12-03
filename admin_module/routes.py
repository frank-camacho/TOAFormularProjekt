from flask import render_template, request, redirect, url_for
from .mock_data import get_new_requests, get_assigned_requests
import sqlite3
from datetime import datetime
import os
import pandas as pd
from .models import filtrar_datos_por_correo  # Importa la función desde models.py
from client_fields import CLIENT_FIELDS
from employee_fields import EMPLOYEE_FIELDS

def register_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/submit_rma', methods=['POST'])
    def submit_rma():
        try:
            conn = sqlite3.connect('rma.db')
            c = conn.cursor()

            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='rma_requests';")
            if not c.fetchone():
                return "Error: La tabla 'rma_requests' no existe. Por favor, inicializa la base de datos correctamente.", 500

            # Obtener los datos del formulario
            kundennummer = request.form['kundennummer']
            name = request.form['name']
            firma = request.form.get('firma', '')
            adresse = request.form['adresse']
            plz = request.form['plz']
            telefon = request.form['telefon']
            email = request.form['email']
            anmeldedatum = request.form['anmeldedatum']
            modell = request.form['modell']
            seriennummer = request.form['seriennummer']
            fehlbeschreibung = request.form['fehlbeschreibung']
            reparaturkosten = float(request.form['reparaturkosten'])
            zustimmung = request.form.get('zustimmung', 'Nein')

            c.execute('''
                INSERT INTO rma_requests (
                    kundennummer, name, firma, adresse, plz, telefon, email, anmeldedatum, 
                    modell, seriennummer, fehlbeschreibung, reparaturkosten, zustimmung
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (kundennummer, name, firma, adresse, plz, telefon, email, anmeldedatum,
                modell, seriennummer, fehlbeschreibung, reparaturkosten, zustimmung))
            
            conn.commit()
            return render_template('confirmation.html')

        except sqlite3.Error as e:
            return f"Error al acceder a la base de datos: {e}", 500

        finally:
            conn.close()

    @app.route('/consulta', methods=['GET', 'POST'])
    def consulta():
        if request.method == 'POST':
            correo = request.form['correo']
            conn = sqlite3.connect('rma.db')
            c = conn.cursor()

            c.execute('''
                SELECT * FROM rma_requests WHERE email = ?;
            ''', (correo,))
            resultados = c.fetchall()

            conn.close()

            if not resultados:
                return render_template('consulta.html', mensaje="Keine Ergebnisse gefunden.")

            columnas = ["ID", "Kundennummer", "Name", "Firma", "Adresse", "PLZ", "Telefon", 
                        "E-Mail", "Anmeldedatum", "Modell", "Seriennummer", 
                        "Fehlerbeschreibung", "Reparaturkosten", "Zustimmung"]
            return render_template('tabla.html', resultados=resultados, columnas=columnas)

        return render_template('consulta.html')

    @app.route('/register_rma', methods=['GET', 'POST'])
    def register_rma():
        if request.method == 'POST':
            data = {field['name']: request.form.get(field['name'], '') for field in CLIENT_FIELDS}
            # Lógica para guardar los datos en la base de datos
            return render_template('confirmation.html', message="Neue Anfrage erfolgreich registriert!")

        return render_template('register_rma.html', fields=CLIENT_FIELDS)

    @app.route('/rma_list', methods=['GET'])
    def rma_list():
        rma_data = get_new_requests() + get_assigned_requests()
        return render_template('tabla.html', resultados=rma_data, columnas=["ID", "Producto", "Cliente/Empleado", "Estado", "Fecha"])

    @app.route('/employee_dashboard', methods=['GET'])
    def employee_dashboard():
        conn = sqlite3.connect('rma.db')
        c = conn.cursor()
        c.execute("SELECT id, modell, name, status, assigned_taller FROM rma_requests")
        requests = [
            {"id": row[0], "modell": row[1], "name": row[2], "status": row[3], "assigned_taller": row[4]}
            for row in c.fetchall()
        ]
        conn.close()
        return render_template('employee_dashboard.html', requests=requests)

    @app.route('/new_rma', methods=['GET', 'POST'])
    def new_rma():
        if request.method == 'POST':
            product = request.form['product']
            serial_number = request.form['serial_number']
            customer = request.form['customer']
            issue_description = request.form['issue_description']

            print(f"Neues RMA hinzugefügt: {product}, {serial_number}, {customer}, {issue_description}")
            return render_template('confirmation.html', message="Neues RMA erfolgreich erstellt!", is_employee=True)

        return render_template('new_rma.html')

    @app.route('/new_requests', methods=['GET'])
    def new_requests_view():
        requests = get_new_requests()
        return render_template('new_requests.html', requests=requests)

    @app.route('/assign_request', methods=['POST'])
    def assign_request():
        request_id = int(request.form['id'])
        requests = get_new_requests()

        for req in requests:
            if req['id'] == request_id:
                requests.remove(req)
                req['employee'] = "Empleado Automático"
                req['status'] = "En Proceso"
                get_assigned_requests().append(req)
                break

        print(f"Pedido {request_id} asignado correctamente.")
        return redirect('/new_requests')

    @app.route('/assigned_requests', methods=['GET'])
    def assigned_requests_view():
        requests = get_assigned_requests()
        return render_template('assigned_requests.html', requests=requests)

    @app.route('/update_status', methods=['POST'])
    def update_status():
        request_id = request.form['id']
        new_status = request.form['status']
        print(f"Estado del pedido {request_id} actualizado a {new_status}.")
        return redirect('/assigned_requests')

    @app.route('/report', methods=['GET'])
    def report():
        rma_data = [
            {"status": "En Proceso", "count": 10},
            {"status": "Completado", "count": 15},
            {"status": "Pendiente", "count": 5},
        ]

        report_data = {item['status']: item['count'] for item in rma_data}
        return render_template('report.html', report_data=report_data)

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
                data['kundennummer'], data['product'], data['serial_number'], data['customer'], data['adresse'],
                data['plz'], data['telefon'], data['email'], data['anmeldedatum'], data['issue_description'],
                float(data.get('repair_cost', 0)), data['status'], data['assigned_taller'], rma_id
            ))
            conn.commit()
            conn.close()

            return redirect('/employee_dashboard')

        c.execute('SELECT * FROM rma_requests WHERE id = ?', (rma_id,))
        row = c.fetchone()
        conn.close()

        if not row:
            return "Error: Kein RMA gefunden", 404

        rma_data = {EMPLOYEE_FIELDS[i]['name']: row[i] for i in range(len(EMPLOYEE_FIELDS))}
        return render_template('edit_data.html', fields=EMPLOYEE_FIELDS, rma_data=rma_data, rma_id=rma_id)

    @app.route('/new_repair', methods=['GET', 'POST'])
    def new_repair():
        if request.method == 'POST':
            data = {field['name']: request.form.get(field['name'], '') for field in EMPLOYEE_FIELDS}

            conn = sqlite3.connect('rma.db')
            c = conn.cursor()
            c.execute('''
                INSERT INTO rma_requests (
                    kundennummer, modell, seriennummer, name, adresse, plz, telefon, email,
                    anmeldedatum, fehlbeschreibung, reparaturkosten, status, assigned_taller
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data['kundennummer'], data['product'], data['serial_number'], data['customer'],
                data['adresse'], data['plz'], data['telefon'], data['email'], data['anmeldedatum'],
                data['issue_description'], float(data.get('repair_cost', 0)), data['status'], data['assigned_taller']
            ))
            conn.commit()
            conn.close()

            return render_template('confirmation.html', message="Neue Reparatur erfolgreich registriert!", is_employee=True)

        return render_template('new_repair.html', fields=EMPLOYEE_FIELDS)

    @app.route('/today', methods=['GET'])
    def today():
        fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return {"fecha_hora": fecha_hora_actual}

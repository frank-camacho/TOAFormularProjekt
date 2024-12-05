from flask import render_template, request, redirect
import sqlite3
from datetime import datetime
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

    @app.route('/consulta', methods=['GET', 'POST'])
    def consulta():
        if request.method == 'POST':
            correo = request.form['correo']
            conn = sqlite3.connect('rma.db')
            c = conn.cursor()

            c.execute('SELECT * FROM rma_requests WHERE email = ?', (correo,))
            resultados = c.fetchall()
            conn.close()

            if not resultados:
                return render_template('consulta.html', mensaje="Keine Ergebnisse gefunden.")
            
            columnas = [field['label'] for field in CLIENT_FIELDS]
            return render_template('tabla.html', resultados=resultados, columnas=columnas)

        return render_template('consulta.html')

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

            return render_template('confirmation.html', message="Reparatur erfolgreich registriert!", is_employee=True)

        return render_template('new_repair.html', fields=EMPLOYEE_FIELDS)

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

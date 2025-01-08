# routes/employee_routes.py

from flask import Blueprint, render_template, request, redirect, session, g
from reportlab.pdfgen import canvas
from flask_mail import Message
from flask_extensions import mail
import sqlite3
from utils.db_utils import get_db_path
from utils.routes_map import routes_map
from employee_fields import EMPLOYEE_FIELDS

# Crear un blueprint para las rutas de empleados
employee_bp = Blueprint('employee', __name__, url_prefix='/employee')

# Middleware para verificar si el usuario es empleado
@employee_bp.before_request
def employee_required():
    if not session.get('user_id') or session.get('role') != 'employee':
        return redirect(routes_map['shared_login']())

@employee_bp.route('/dashboard', methods=['GET'])
def employee_dashboard():
    try:
        # Verificar sesión y cargar datos
        session_active = 'user_id' in session
        username = g.current_user['username'] if session_active else None

        # Conexión a la base de datos
        conn = sqlite3.connect(get_db_path())
        conn.row_factory = sqlite3.Row  # Permitir acceso a columnas por nombre
        c = conn.cursor()

        # Obtener los primeros 5 registros con estado "Neu"
        c.execute("""
            SELECT id, modell, name, status, assigned_taller, timestamp 
            FROM rma_requests 
            WHERE status = 'Neu' 
            ORDER BY timestamp DESC 
            LIMIT 5
        """)
        requests = [dict(row) for row in c.fetchall()]

        # Calcular estadísticas básicas con una sola consulta
        c.execute("""
            SELECT 
                COUNT(*) AS total_rmas,
                SUM(CASE WHEN status = 'Neu' THEN 1 ELSE 0 END) AS new,
                SUM(CASE WHEN status = 'In Arbeit' THEN 1 ELSE 0 END) AS in_progress,
                SUM(CASE WHEN status = 'Abgeschlossen' THEN 1 ELSE 0 END) AS completed
            FROM rma_requests
        """)
        stats = dict(c.fetchone())

        # Obtener todos los RMAs para la pestaña "Alle RMAs"
        c.execute("""
            SELECT id, modell, name, status, assigned_taller, timestamp 
            FROM rma_requests
            ORDER BY timestamp DESC
        """)
        rmas = [dict(row) for row in c.fetchall()]

        return render_template(
            'employee_dashboard.html',
            session_active=session_active,
            username=username,
            requests=requests,
            stats=stats,
            rmas=rmas
        )
    except sqlite3.Error as e:
        return f"Error al acceder a la base de datos: {e}", 500
    finally:
        if 'conn' in locals():
            conn.close()

@employee_bp.route('/new_requests', methods=['GET'])
def new_requests():
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

@employee_bp.route('/generate_report', methods=['GET'])
def generate_report():
    if not g.current_user or g.current_user['role'] != 'employee':
        return redirect(routes_map['login']())

    try:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()

        # Obtener los datos de los RMAs
        c.execute('SELECT id, seriennummer FROM rma_requests')
        rmas = [{"id": row[0], "seriennummer": row[1]} for row in c.fetchall()]

        # Obtener el conteo de RMAs por estado
        c.execute('SELECT status, COUNT(*) FROM rma_requests GROUP BY status')
        report_data = {row[0]: row[1] for row in c.fetchall()}

        return render_template('report.html', report_data=report_data, rmas=rmas)
    except sqlite3.Error as e:
        return f"Fehler bei der Berichterstellung: {e}", 500
    finally:
        conn.close()

@employee_bp.route('/view_reports/<int:rma_id>', methods=['GET'])
def view_reports(rma_id):
    if not g.current_user or g.current_user['role'] != 'employee':
        return redirect(routes_map['login']())

    try:
        # Conectar a la base de datos de RMA
        conn_rma = sqlite3.connect(get_db_path())  # Asegúrate de que apunta a `rma.db`
        c_rma = conn_rma.cursor()

        # Obtener datos del RMA
        c_rma.execute('SELECT id, seriennummer, status, fehlbeschreibung, reparaturkosten FROM rma_requests WHERE id = ?', (rma_id,))
        rma_data = c_rma.fetchone()
        conn_rma.close()

        if not rma_data:
            return "Keine Daten für diese RMA gefunden.", 404

        rma = {
            "id": rma_data[0],
            "seriennummer": rma_data[1],
            "status": rma_data[2],
            "fehlbeschreibung": rma_data[3],
            "reparaturkosten": rma_data[4],
        }

        # Conectar a la base de datos de reportes
        conn_reports = sqlite3.connect("workshop_reports.db")  # Ruta correcta de tu base de datos de reportes
        c_reports = conn_reports.cursor()

        # Obtener todos los reportes asociados al RMA
        c_reports.execute('SELECT id, comments, cost FROM workshop_reports WHERE rma_id = ?', (rma_id,))
        reports_data = c_reports.fetchall()
        conn_reports.close()

        # Estructurar los datos de los reportes
        reports = [{"id": row[0], "comments": row[1], "cost": row[2]} for row in reports_data]

        # Pasar los datos a la plantilla
        return render_template('view_reports.html', rma=rma, reports=reports)
    except sqlite3.Error as e:
        return f"Fehler bei der Abfrage: {e}", 500

# Crear solicitud
@employee_bp.route('/create_rma', methods=['GET', 'POST'])
def create_rma():
    if not g.current_user or g.current_user['role'] != 'employee':
        return redirect(routes_map['login']())

    if request.method == 'POST':
        data = {field['name']: request.form.get(field['name'], '') for field in EMPLOYEE_FIELDS}
        try:
            conn = sqlite3.connect(get_db_path())
            c = conn.cursor()
            c.execute('''
            INSERT INTO rma_requests (kundennummer, modell, seriennummer, name, adresse, plz, telefon, email, anmeldedatum, fehlbeschreibung, reparaturkosten, status, assigned_taller)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.get('kundennummer'), data.get('modell'), data.get('seriennummer'), data.get('name'),
                data.get('adresse'), data.get('plz'), data.get('telefon'), data.get('email'),
                data.get('anmeldedatum'), data.get('fehlbeschreibung'), float(data.get('reparaturkosten', 0)),
                'Neu', g.current_user.get('username')
            ))
            conn.commit()
            return redirect(routes_map['employee_dashboard']())
        except sqlite3.Error as e:
            return f"Error al crear la solicitud: {e}", 500
        finally:
            conn.close()

    return render_template('create_rma.html', fields=EMPLOYEE_FIELDS)

# El resto de las rutas (editar, eliminar) serían similares a las ya existentes.

@employee_bp.route('/create_report/<int:rma_id>', methods=['GET', 'POST'])
def create_report(rma_id):
    if not g.current_user or g.current_user['role'] != 'employee':
        return redirect(routes_map['login']())

    if request.method == 'POST':
        comments = request.form['comments']
        cost = float(request.form['cost'])

        try:
            conn = sqlite3.connect("workshop_reports.db")
            c = conn.cursor()
            c.execute('''
            INSERT INTO workshop_reports (rma_id, comments, cost)
            VALUES (?, ?, ?)
            ''', (rma_id, comments, cost))
            conn.commit()
            return redirect(routes_map['employee_dashboard']())
        except sqlite3.Error as e:
            return f"Error al crear el reporte: {e}", 500
        finally:
            conn.close()

    return render_template('create_report.html', rma_id=rma_id)

@employee_bp.route('/generate_accounting_report/<int:rma_id>')
def generate_accounting_report(rma_id):
    try:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        c.execute('''
        SELECT seriennummer, anmeldedatum, reparaturkosten FROM rma_requests WHERE id = ?
        ''', (rma_id,))
        rma_data = c.fetchone()

        if not rma_data:
            return "RMA no encontrado", 404

        seriennummer, anmeldedatum, reparaturkosten = rma_data

        # Generar PDF
        pdf_path = f"static/reports/accounting_report_{rma_id}.pdf"
        pdf = canvas.Canvas(pdf_path)
        pdf.drawString(100, 750, f"RMA #{rma_id} - Reporte de Contabilidad")
        pdf.drawString(100, 730, f"Serie: {seriennummer}")
        pdf.drawString(100, 710, f"Fecha de Ingreso: {anmeldedatum}")
        pdf.drawString(100, 690, f"Costo: {reparaturkosten} EUR")
        pdf.save()

        return f"Reporte generado en: {pdf_path}"
    except sqlite3.Error as e:
        return f"Error al generar el reporte: {e}", 500
    finally:
        conn.close()

@employee_bp.route('/send_client_report/<int:rma_id>')
def send_client_report(rma_id):
    try:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        c.execute('''
        SELECT seriennummer, anmeldedatum, reparaturkosten, email, comments FROM rma_requests
        LEFT JOIN workshop_reports ON rma_requests.id = workshop_reports.rma_id
        WHERE rma_requests.id = ?
        ''', (rma_id,))
        report_data = c.fetchone()

        if not report_data:
            return "Datos no encontrados", 404

        seriennummer, anmeldedatum, reparaturkosten, email, comments = report_data

        # Enviar correo
        msg = Message(f"Reporte RMA #{rma_id}", sender="your-email@example.com", recipients=[email])
        msg.body = f"""
        RMA #{rma_id} - Detalles:
        Serie: {seriennummer}
        Fecha de Ingreso: {anmeldedatum}
        Costo: {reparaturkosten} EUR
        Comentarios: {comments}
        """
        mail.send(msg)

        return "Reporte enviado al cliente."
    except sqlite3.Error as e:
        return f"Error al enviar el reporte: {e}", 500
    finally:
        conn.close()

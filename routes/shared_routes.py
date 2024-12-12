# routes/shared_routes.py

from flask import Blueprint, render_template, session, redirect, g, request
from utils.routes_map import routes_map
import sqlite3
from werkzeug.security import check_password_hash
from utils.db_utils import get_users_db_path

# Crear un blueprint para las rutas compartidas
shared_bp = Blueprint('shared', __name__)

# Middleware para cargar el usuario actual
@shared_bp.before_app_request
def load_current_user():
    user_id = session.get('user_id')
    if user_id:
        try:
            with sqlite3.connect(get_users_db_path()) as conn:
                c = conn.cursor()
                c.execute('SELECT id, username, role FROM users WHERE id = ?', (user_id,))
                user = c.fetchone()
                if user:
                    g.current_user = {'id': user[0], 'username': user[1], 'role': user[2]}
                else:
                    g.current_user = {'role': 'guest'}  # Visitante
        except sqlite3.Error:
            g.current_user = {'role': 'guest'}  # Manejar errores como visitante
    else:
        g.current_user = {'role': 'guest'}  # Usuario no autenticado por defecto

# Inyectar `current_user` en las plantillas
@shared_bp.app_context_processor
def inject_user():
    return {
        'current_user': g.get('current_user'),
        'routes_map': routes_map  # Inyectamos routes_map en el contexto de las plantillas
    }

# Ruta para la página principal
@shared_bp.route('/')
def index():
    """
    Página principal del sistema.
    Verifica si hay una sesión activa y muestra el estado correspondiente.
    """
    is_logged_in = 'user_id' in session  # Chequear si hay sesión activa
    if is_logged_in:
        # Si hay sesión activa, mostrar mensaje de bienvenida y botón de logout
        username = session.get('username', 'Usuario')
        return render_template('index.html', session_active=True, username=username)
    else:
        # Si no hay sesión activa, mostrar la página de bienvenida estándar
        return render_template('index.html', session_active=False)

# Ruta para el inicio de sesión
@shared_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Si ya hay una sesión activa, redirigir al dashboard correspondiente
    if session.get('user_id'):
        role = session.get('role')
        if role == 'admin':
            return redirect(routes_map['admin_manage_employees']())
        elif role == 'employee':
            return redirect(routes_map['employee_dashboard']())
        else:
            # Si el rol no es válido, limpiar sesión y redirigir al login
            session.clear()
            return render_template('login.html', error_message="Ungültige Sitzung. Bitte erneut anmelden.")

    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        try:
            # Conectar a la base de datos
            conn = sqlite3.connect(get_users_db_path())
            c = conn.cursor()

            # Consultar la base de datos para obtener el usuario
            c.execute('SELECT id, password, role FROM users WHERE username = ?', (username,))
            user = c.fetchone()
            conn.close()

            if user:
                user_id, hashed_password, role = user
                if check_password_hash(hashed_password, password):
                    # Almacenar información de sesión y establecerla como permanente
                    session['user_id'] = user_id
                    session['role'] = role
                    session['username'] = username  # Almacenar el nombre de usuario en sesión
                    session.permanent = True

                    # Redirigir al dashboard según el rol
                    if role == 'admin':
                        return redirect(routes_map['admin_manage_employees']())
                    elif role == 'employee':
                        return redirect(routes_map['employee_dashboard']())
                    else:
                        # Si el rol no es reconocido
                        session.clear()
                        return render_template('login.html', error_message="Unbekannte Benutzerrolle.")
                else:
                    return render_template('login.html', error_message="Ungültiges Passwort.")
            else:
                return render_template('login.html', error_message="Benutzername existiert nicht.")

        except sqlite3.Error as e:
            return render_template('login.html', error_message=f"Datenbankfehler: {e}")

    return render_template('login.html')

# Ruta para cerrar sesión
@shared_bp.route('/logout')
def logout():
    session.clear()
    return redirect(routes_map['shared_index']())

# Ruta para la fecha y hora actual (demostrativa)
@shared_bp.route('/today', methods=['GET'])
def today():
    from datetime import datetime
    fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"fecha_hora": fecha_hora_actual}

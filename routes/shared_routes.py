# routes/shared_routes.py

from flask import Blueprint, render_template, session, redirect, g, request, make_response
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

# Decorador para deshabilitar caché
def no_cache(view):
    """Decorador para deshabilitar caché en las respuestas."""
    def no_cache_decorator(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    return no_cache_decorator

# Ruta para la página principal
@shared_bp.route('/')
def index():
    """
    Página principal del sistema.
    Verifica si hay una sesión activa y muestra el estado correspondiente.
    """
    session_active = 'user_id' in session  # Solo verdadero si hay sesión activa
    username = session.get('username', None) if session_active else None

    return render_template('index.html', session_active=session_active, username=username)



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
                    session['user_id'] = user_id
                    session['role'] = role
                    session['username'] = username  # Almacenar el nombre de usuario en sesión
                    session.permanent = True

                    if role == 'admin':
                        return redirect(routes_map['admin_manage_employees']())
                    elif role == 'employee':
                        return redirect(routes_map['employee_dashboard']())
                    else:
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

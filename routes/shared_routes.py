# routes/shared_routes.py

from flask import Blueprint, render_template, session, redirect, g, request, make_response
from utils.routes_map import routes_map
import sqlite3
from werkzeug.security import check_password_hash
from utils.db_utils import get_users_db_path, get_db_path

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
                    print(f"[DEBUG] Usuario cargado en la sesión: {g.current_user}")
                else:
                    session.clear()
                    g.current_user = {'role': 'guest'}
                    print("[DEBUG] Usuario inválido. Sesión eliminada.")
        except sqlite3.Error as e:
            g.current_user = {'role': 'guest'}
            print(f"[ERROR] Error al cargar usuario actual: {e}")
    else:
        g.current_user = {'role': 'guest'}
        print("[DEBUG] No hay usuario autenticado en la sesión.")

# Inyectar `current_user` en las plantillas
@shared_bp.app_context_processor
def inject_user():
    return {
        'current_user': g.get('current_user'),
        'routes_map': routes_map  # Inyectamos routes_map en el contexto de las plantillas
    }

# Decorador para deshabilitar caché
def disable_cache_decorator(view):
    """Decorador para deshabilitar caché en las respuestas."""
    def wrapped_view(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    wrapped_view.__name__ = view.__name__
    return wrapped_view

# Ruta para la página principal
@shared_bp.route('/')
@disable_cache_decorator  # Deshabilitar caché
def index():
    session_active = 'user_id' in session
    username = session.get('username', None) if session_active else None
    print(f"[DEBUG] Estado de la sesión al acceder a '/': session_active={session_active}, username={username}")
    return render_template('index.html', session_active=session_active, username=username)

# Ruta para el inicio de sesión
@shared_bp.route('/login', methods=['GET', 'POST'])
@disable_cache_decorator
def login():
    if session.get('user_id'):
        role = session.get('role')
        print(f"[DEBUG] Usuario ya autenticado: role={role}")
        if role == 'admin':
            return redirect(routes_map['admin_manage_employees']())
        elif role == 'employee':
            return redirect(routes_map['employee_dashboard']())
        elif role == 'client':
            return redirect(routes_map['client_dashboard']())
        else:
            session.clear()
            print("[ERROR] Rol desconocido. Sesión eliminada.")
            return render_template('login.html', error_message="Ungültige Sitzung. Bitte erneut anmelden.")

    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        print(f"[DEBUG] Intento de inicio de sesión: username={username}")
        try:
            conn = sqlite3.connect(get_users_db_path())
            c = conn.cursor()
            c.execute('SELECT id, password, role FROM users WHERE username = ?', (username,))
            user = c.fetchone()
            conn.close()

            if user:
                user_id, hashed_password, role = user
                if check_password_hash(hashed_password, password):
                    session.clear()
                    session['user_id'] = user_id
                    session['role'] = role
                    session['username'] = username
                    session.permanent = True
                    print(f"[DEBUG] Inicio de sesión exitoso: username={username}, role={role}")
                    if role == 'admin':
                        return redirect(routes_map['admin_manage_employees']())
                    elif role == 'employee':
                        return redirect(routes_map['employee_dashboard']())
                    elif role == 'client':
                        return redirect(routes_map['client_dashboard']())
                else:
                    print("[ERROR] Contraseña incorrecta.")
                    return render_template('login.html', error_message="Ungültiges Passwort.")
            else:
                print("[ERROR] Usuario no encontrado.")
                return render_template('login.html', error_message="Benutzername existiert nicht.")

        except sqlite3.Error as e:
            print(f"[ERROR] Error en la base de datos durante el inicio de sesión: {e}")
            return render_template('login.html', error_message=f"Datenbankfehler: {e}")

    return render_template('login.html')

# Ruta para cerrar sesión
@shared_bp.route('/logout')
@disable_cache_decorator
def logout():
    print(f"[DEBUG] Cerrando sesión para el usuario: {session.get('username')}")
    session.clear()
    response = redirect(routes_map['shared_index']())
    response.set_cookie('session', '', expires=0)
    response.set_cookie('remember_token', '', expires=0)
    print("[DEBUG] Cookies de sesión eliminadas.")
    return response

# Ruta para validar la sesión
@shared_bp.route('/check_session', methods=['GET'])
@disable_cache_decorator
def check_session():
    session_active = 'user_id' in session
    print(f"[DEBUG] Verificación de sesión: session_active={session_active}")
    return {"session_active": session_active}


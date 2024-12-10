from flask import Flask
from flask_session import Session
from routes import register_routes
from utils.routes_map import routes_map
from datetime import timedelta

# Inicializar la aplicación Flask
app = Flask(__name__)

# Configurar la clave secreta para manejar sesiones
app.secret_key = 'tu-clave-super-secreta'  # Cambia esto por una clave segura y única

# Configuración de la sesión
app.config['SESSION_TYPE'] = 'filesystem'  # Las sesiones se almacenan en el sistema de archivos
app.config['SESSION_PERMANENT'] = True  # Las sesiones pueden ser permanentes
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Tiempo de inactividad para logout automático

# Inicializar Flask-Session
Session(app)

# Registrar todas las rutas
register_routes(app)

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)

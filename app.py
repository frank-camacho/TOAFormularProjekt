from flask import Flask
from flask_session import Session
from datetime import timedelta
from flask_extensions import mail
from routes import register_routes

# Inicializar la aplicación Flask
app = Flask(__name__)

# Configuración de correo
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'your-email@example.com'
app.config['MAIL_PASSWORD'] = 'your-password'
app.config['MAIL_USE_TLS'] = True

# Configuración de la sesión
app.secret_key = 'tu-clave-super-secreta'  # Cambia esto por una clave segura y única
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# Inicializar extensiones
mail.init_app(app)
Session(app)

# Registrar las rutas
register_routes(app)

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)

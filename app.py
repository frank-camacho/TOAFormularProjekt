import os
import shutil
from flask import Flask
from routes import register_routes
from flask_session import Session
from datetime import timedelta
from client_view import create_client_view  # Importar la función para crear la vista

# Ruta del directorio de sesiones
session_dir = './flask_session_files'

# Limpieza de contenido del directorio de sesiones antes de iniciar el servidor
if os.path.exists(session_dir):
    try:
        for filename in os.listdir(session_dir):
            file_path = os.path.join(session_dir, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Eliminar archivos o enlaces
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Eliminar subdirectorios
        print("[DEBUG] Contenido del directorio de sesiones eliminado correctamente.")
    except Exception as e:
        print(f"[ERROR] No se pudo limpiar el contenido del directorio de sesiones: {e}")
else:
    os.makedirs(session_dir)  # Crear el directorio si no existe
    print("[DEBUG] Directorio de sesiones creado.")

# Crear la aplicación Flask
app = Flask(__name__)

# Configuración de la clave secreta y las sesiones
app.secret_key = os.urandom(24)
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # La sesión expira en 30 minutos
app.config['SESSION_TYPE'] = 'filesystem'  # Las sesiones se almacenan en el servidor
app.config['SESSION_FILE_DIR'] = session_dir  # Directorio para almacenar sesiones
app.config['SESSION_FILE_THRESHOLD'] = 100  # Número máximo de sesiones almacenadas

# Crear la vista `Client_View` al iniciar la aplicación
print("[DEBUG] Creando la vista `Client_View` en la base de datos.")
create_client_view()  # Asegurar que la vista esté disponible

# Inicializar sesiones con Flask-Session
Session(app)

# Registrar las rutas compartidas y específicas
register_routes(app)

if __name__ == "__main__":
    app.run(debug=True)

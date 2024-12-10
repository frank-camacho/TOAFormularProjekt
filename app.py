from flask import Flask
from routes import register_routes
# Importa routes_map solo si planeas usar rutas centralizadas dentro de app.py (opcional)
from utils.routes_map import routes_map

# Inicializar la aplicación Flask
app = Flask(__name__)

# Configurar la clave secreta para manejar sesiones
app.secret_key = 'tu-clave-super-secreta'  # Cambia esto por una clave segura y única

# Registrar todas las rutas
register_routes(app)

# Ejecutar la aplicación
if __name__ == '__main__':
    # Nota: routes_map está disponible para referencias directas a rutas si es necesario.
    app.run(debug=True)

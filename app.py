from flask import Flask, session
from admin_module import routes

# Inicializar la aplicación Flask
app = Flask(__name__)

# Configurar la clave secreta para manejar sesiones
app.secret_key = 'tu-clave-super-secreta'  # Cambia esto por una clave segura y única

# Registrar rutas
routes.register_routes(app)

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)

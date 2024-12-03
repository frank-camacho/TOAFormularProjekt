from admin_module.routes import register_routes  # Importa las rutas desde el subdirectorio

from flask import Flask

app = Flask(__name__)

# Registra las rutas principales
register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask
from admin_module import routes  # Importa las rutas de admin_module

app = Flask(__name__)
app.secret_key = 'mi_clave_secreta'

# Inicializa las rutas, registrándolas con la app
routes.register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)

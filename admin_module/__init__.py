# admin_module/__init__.py

from flask import Flask
from .routes import register_routes  # Importa las rutas desde routes.py

def init_app(app: Flask):
    """Función para inicializar la aplicación con las rutas."""
    register_routes(app)

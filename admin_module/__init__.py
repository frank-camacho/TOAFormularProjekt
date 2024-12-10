from flask import Flask
from .routes import admin_bp  # Importamos el blueprint definido en routes.py

def init_admin_module(app: Flask):
    """
    Inicializa el módulo administrativo registrando su blueprint.
    """
    # Registrar el blueprint administrativo con su prefijo
    app.register_blueprint(admin_bp, url_prefix='/admin')

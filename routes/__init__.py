from flask import Flask
from .admin_routes import admin_bp
from .rma_routes import rma_bp
from .employee_routes import employee_bp
from .client_routes import client_bp
from .shared_routes import shared_bp
# Importar `routes_map` solo para documentación o funciones específicas que lo necesiten
from utils.routes_map import routes_map  

def register_routes(app: Flask):
    """Registra todos los blueprints del sistema."""
    # Blueprints principales
    app.register_blueprint(shared_bp)  # Rutas compartidas (login, logout, index)
    app.register_blueprint(admin_bp, url_prefix='/admin')  # Rutas administrativas
    app.register_blueprint(rma_bp, url_prefix='/rma')  # Rutas relacionadas con RMA
    app.register_blueprint(employee_bp, url_prefix='/employee')  # Rutas de empleados
    app.register_blueprint(client_bp, url_prefix='/client')  # Rutas de clientes

    # Información adicional sobre routes_map
    # Este módulo contiene un diccionario centralizado de rutas para referencia directa.

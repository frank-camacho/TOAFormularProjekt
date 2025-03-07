from flask import Flask
from routes.shared_routes import shared_bp
from routes.admin_routes import admin_bp
from routes.rma_routes import rma_bp
from routes.employee_routes import employee_bp
from routes.client_routes import client_bp

def register_routes(app: Flask):
    """Registra todos los blueprints del sistema."""
    app.register_blueprint(shared_bp)  # Rutas compartidas (login, logout, index)
    app.register_blueprint(admin_bp, url_prefix='/admin')  # Rutas administrativas
    app.register_blueprint(rma_bp, url_prefix='/rma')  # Rutas relacionadas con RMA
    app.register_blueprint(employee_bp, url_prefix='/employee')  # Rutas de empleados
    app.register_blueprint(client_bp, url_prefix='/client')  # Rutas de clientes

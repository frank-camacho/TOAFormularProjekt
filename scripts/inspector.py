import os
import sys

# Añadir el directorio raíz del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from utils.db_utils import execute_query  # Ahora funcionará correctamente

# Verificar si el rol `client` funciona
def test_client_access():
    # Ruta a la base de datos relativa a inspector.py
    db_path = os.path.join(os.path.dirname(__file__), "../users.db")

    # Probar inserción de cliente
    execute_query(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        params=("test_client", "test_password", "client"),
        fetch_all=False,
        db_type="users"
    )

    # Comprobar que el cliente existe
    result = execute_query(
        "SELECT username, role FROM users WHERE username = ?",
        params=("test_client",),
        db_type="users"
    )
    print(f"Resultados para el usuario creado: {result}")

    # Limpiar datos después de la prueba
    execute_query(
        "DELETE FROM users WHERE username = ?",
        params=("test_client",),
        fetch_all=False,
        db_type="users"
    )

if __name__ == "__main__":
    test_client_access()

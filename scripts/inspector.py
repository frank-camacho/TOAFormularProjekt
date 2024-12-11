from werkzeug.security import generate_password_hash
import sqlite3
import os

def get_users_db_path():
    """
    Devuelve la ruta absoluta de la base de datos 'users.db' ubicada en el directorio raíz del proyecto.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Ruta de la carpeta /scripts
    return os.path.join(current_dir, '../users.db')

def inspeccionar_usuario(username):
    """
    Verifica si un usuario existe en la tabla `users` y muestra sus detalles.
    :param username: El nombre de usuario a buscar.
    """
    try:
        # Conectarse a la base de datos
        db_path = get_users_db_path()
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # Consultar el usuario
        c.execute("SELECT id, username, password, role, last_login FROM users WHERE username = ?", (username,))
        user = c.fetchone()

        if user:
            print(f"Detalles del usuario '{username}':")
            print(f"ID: {user[0]}")
            print(f"Username: {user[1]}")
            print(f"Password (hash): {user[2]}")
            print(f"Role: {user[3]}")
            print(f"Last Login: {user[4]}")
        else:
            print(f"El usuario '{username}' no existe en la tabla 'users'.")

    except sqlite3.Error as e:
        print(f"Error al consultar la base de datos: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    # Preguntar al usuario qué acción realizar
    print("Inspección de usuario en la base de datos 'users.db'")
    usuario = input("Ingrese el nombre de usuario a inspeccionar: ").strip()
    inspeccionar_usuario(usuario)

def actualizar_password(username, new_password):
    """
    Actualiza la contraseña de un usuario en la base de datos.
    :param username: El nombre de usuario a actualizar.
    :param new_password: La nueva contraseña en texto plano.
    """
    try:
        db_path = get_users_db_path()
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # Generar el hash de la nueva contraseña
        hashed_password = generate_password_hash(new_password)

        # Actualizar la contraseña en la base de datos
        c.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_password, username))
        conn.commit()

        print(f"Contraseña para el usuario '{username}' actualizada exitosamente.")
    except sqlite3.Error as e:
        print(f"Error al actualizar la contraseña: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    print("Actualizar contraseña de usuario en 'users.db'")
    usuario = input("Ingrese el nombre de usuario a actualizar: ").strip()
    nueva_password = input(f"Ingrese la nueva contraseña para '{usuario}': ").strip()
    actualizar_password(usuario, nueva_password)

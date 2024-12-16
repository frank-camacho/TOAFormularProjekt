import sqlite3
import os

def init_users_db():
    # Ruta absoluta a la base de datos
    db_path = os.path.join(os.path.dirname(__file__), "users.db")
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # Verificar si la tabla `users` existe y necesita actualización
        c.execute("PRAGMA table_info(users);")
        columns = [col[1] for col in c.fetchall()]
        if "role" in columns:
            # Crear una tabla temporal con la nueva definición
            c.execute("PRAGMA foreign_keys = off;")
            c.execute('''
                CREATE TABLE IF NOT EXISTS users_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('admin', 'employee', 'client')),
                    last_login DATETIME
                )
            ''')
            # Copiar los datos de la tabla antigua
            c.execute('''
                INSERT INTO users_new (id, username, password, role, last_login)
                SELECT id, username, password, role, last_login FROM users
            ''')
            # Eliminar la tabla antigua y renombrar la nueva
            c.execute("DROP TABLE users;")
            c.execute("ALTER TABLE users_new RENAME TO users;")
            c.execute("PRAGMA foreign_keys = on;")
            print("Tabla `users` actualizada correctamente.")
        else:
            # Crear la tabla `users` si no existe
            c.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('admin', 'employee', 'client')),
                    last_login DATETIME
                )
            ''')
            print("Tabla `users` creada correctamente.")
    except sqlite3.Error as e:
        print(f"Error al inicializar la base de datos: {e}")
    finally:
        conn.commit()
        conn.close()

if __name__ == "__main__":
    init_users_db()

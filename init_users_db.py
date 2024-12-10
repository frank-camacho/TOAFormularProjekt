import sqlite3

def init_users_db():
    db_path = "users.db"  # Ruta de la nueva base de datos
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # Crear la tabla de usuarios
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin', 'employee')),
                last_login DATETIME
            )
        ''')

        print("Base de datos 'users.db' inicializada correctamente.")
    except sqlite3.Error as e:
        print(f"Error al inicializar la base de datos: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    init_users_db()

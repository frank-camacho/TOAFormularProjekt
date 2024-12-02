import sqlite3
import hashlib

# Inicializar la base de datos de usuarios
def init_db():
    conn = sqlite3.connect('usuarios.db', check_same_thread=False)  # Conexión con soporte para múltiples hilos
    conn.execute('PRAGMA journal_mode=WAL;')  # Habilitar el modo WAL para mayor concurrencia
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Registrar un nuevo usuario
def registrar_usuario(username, password):
    conn = sqlite3.connect('usuarios.db', check_same_thread=False)
    conn.execute('PRAGMA journal_mode=WAL;')
    cursor = conn.cursor()
    password_hash = hashlib.sha256(password.encode()).hexdigest()  # Encriptar contraseña
    try:
        # Registrar siempre con el rol "usuario"
        cursor.execute('INSERT INTO usuarios (username, password, role) VALUES (?, ?, ?)', (username, password_hash, 'usuario'))
        conn.commit()
    except sqlite3.IntegrityError:
        return False  # Usuario ya existe
    finally:
        conn.close()
    return True

# Autenticar usuario
def obtener_usuario(username, password):
    conn = sqlite3.connect('usuarios.db', check_same_thread=False)  # Conexión con soporte para múltiples hilos
    conn.execute('PRAGMA journal_mode=WAL;')  # Habilitar el modo WAL
    cursor = conn.cursor()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute('SELECT * FROM usuarios WHERE username = ? AND password = ?', (username, password_hash))
    user = cursor.fetchone()
    conn.close()
    return user

from flask import Flask, render_template, request, redirect, session
import pandas as pd
import os
import usuarios  # Importamos el módulo de usuarios

app = Flask(__name__)
app.secret_key = 'mi_clave_secreta'  # Agregar clave secreta para manejar sesiones

# Ruta principal con opciones de registro y login
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para el registro de usuarios
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        if usuarios.registrar_usuario(username, password, role):
            return "Usuario registrado exitosamente."
        else:
            return "Error: El usuario ya existe."
    return render_template('register.html')

# Ruta para el login de usuarios
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Pasar ambos argumentos (username y password) a la función obtener_usuario
        user = usuarios.obtener_usuario(username, password)
        
        if user:
            session['user_id'] = user[0]  # Asumiendo que el ID está en la primera columna
            session['role'] = user[3]    # Asumiendo que el rol está en la cuarta columna
            return redirect('/consulta')  # Redirige a la página de consulta
        else:
            return "Usuario o contraseña incorrectos"
    return render_template('login.html')

# Ruta para la consulta de datos
@app.route('/consulta', methods=['GET', 'POST'])
def consulta():
    if 'user_id' not in session:
        return redirect('/login')  # Redirige si no hay sesión activa

    is_empleado = session.get('role') == 'empleado'
    username = session.get('user_id')  # Obtén el nombre o ID del usuario

    if request.method == 'POST':
        correo = request.form['correo']  # Obtén el correo del formulario
        archivo_excel = os.path.join(os.path.dirname(__file__), 'reparaturen.xlsx')
        resultados = filtrar_datos_por_correo(archivo_excel, correo)

        if resultados.empty:
            # Si no hay resultados, regresa a consulta.html con un mensaje
            return render_template('consulta.html', mensaje="Keine Ergebnisse gefunden.", is_empleado=is_empleado, username=username)

        # Si hay resultados, pasa los datos a tabla.html
        columnas = resultados.columns.tolist()  # Obtén las columnas del DataFrame
        resultados_dict = resultados.to_dict(orient='records')  # Convierte los datos a lista de diccionarios
        return render_template('tabla.html', resultados=resultados_dict, columnas=columnas)

    # Si es una solicitud GET, carga consulta.html
    return render_template('consulta.html', is_empleado=is_empleado, username=username)

# Función que lee el archivo Excel por fragmentos y filtra por correo
def filtrar_datos_por_correo(archivo_excel, correo):
    df_filtrado = pd.DataFrame()
    xls = pd.ExcelFile(archivo_excel, engine='openpyxl')
    chunksize = 1000
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        for start in range(0, len(df), chunksize):
            chunk = df.iloc[start:start+chunksize]
            email_column = None
            for column in chunk.columns:
                if "E-Mail:" in column:
                    email_column = column
                    break
            if email_column:
                filtered_chunk = chunk[chunk[email_column] == correo]
                df_filtrado = pd.concat([df_filtrado, filtered_chunk], ignore_index=True)
    
    return df_filtrado

if __name__ == '__main__':
    app.run(debug=True)

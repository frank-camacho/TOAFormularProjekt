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
        
        user = usuarios.obtener_usuario(username)  # Supongamos que tenemos una función para obtener el usuario
        if user and user['password'] == password:
            session['user_id'] = user['id']
            session['role'] = user['role']
            return redirect('/consulta')  # Redirige a la página de consulta
        else:
            return "Usuario o contraseña incorrectos"
    return render_template('login.html')

# Ruta para la consulta de datos
@app.route('/consulta', methods=['GET', 'POST'])
def consulta():
    if 'user_id' not in session or session['role'] == 'empleado':
        return redirect('/login')  # Si no hay sesión o el usuario es empleado, redirige al login

    if request.method == 'POST':
        correo = request.form['correo']
        archivo_excel = os.path.join(os.path.dirname(__file__), 'reparaturen.xlsx')
        resultados = filtrar_datos_por_correo(archivo_excel, correo)
        
        if resultados.empty:
            return render_template('consulta.html', mensaje="No se encontraron resultados para ese correo.")
        
        columnas = resultados.columns.tolist()
        resultados_dict = resultados.to_dict(orient='records')
        
        return render_template('consulta.html', resultados=resultados_dict, columnas=columnas)

    return render_template('consulta.html')

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

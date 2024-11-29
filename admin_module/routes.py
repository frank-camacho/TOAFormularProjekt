from flask import render_template, request, redirect, session
from datetime import date
import os
import pandas as pd
from usuarios import registrar_usuario, obtener_usuario  # Importa las funciones necesarias
from .models import filtrar_datos_por_correo  # Importa la función desde models.py

def register_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            role = request.form['role']
            if registrar_usuario(username, password, role):
                return "Usuario registrado exitosamente."
            else:
                return "Error: El usuario ya existe."
        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            
            user = obtener_usuario(username, password)
            
            if user:
                session['user_id'] = user[0]  # Asumiendo que el ID está en la primera columna
                session['role'] = user[3]    # Asumiendo que el rol está en la cuarta columna
                return redirect('/consulta')  # Redirige a la página de consulta
            else:
                return "Usuario o contraseña incorrectos"
        return render_template('login.html')

    @app.route('/consulta', methods=['GET', 'POST'])
    def consulta():
        if 'user_id' not in session:
            return redirect('/login')  # Redirige si no hay sesión activa

        is_empleado = session.get('role') == 'empleado'
        username = session.get('user_id')  # Obtén el nombre o ID del usuario

        if request.method == 'POST':
            correo = request.form['correo']  # Obtén el correo del formulario
            archivo_excel = os.path.join(os.getcwd(), 'reparaturen.xlsx')
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

    @app.route('/today', methods=['GET'])
    def today():
        ya = date.today()
        print(ya)  # Esto imprimirá la fecha en la consola del servidor
        return render_template('consulta.html', ya=ya)
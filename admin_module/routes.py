from flask import render_template, request, redirect
from datetime import datetime
import os
import pandas as pd
from .models import filtrar_datos_por_correo  # Importa la función desde models.py

def register_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/consulta', methods=['GET', 'POST'])
    def consulta():
        if request.method == 'POST':
            correo = request.form['correo']  # Obtén el correo del formulario
            archivo_excel = os.path.join(os.getcwd(), 'reparaturen.xlsx')
            resultados = filtrar_datos_por_correo(archivo_excel, correo)

            if resultados.empty:
                # Si no hay resultados, regresa a consulta.html con un mensaje
                return render_template('consulta.html', mensaje="Keine Ergebnisse gefunden.")

            # Si hay resultados, pasa los datos a tabla.html
            columnas = resultados.columns.tolist()  # Obtén las columnas del DataFrame
            resultados_dict = resultados.to_dict(orient='records')  # Convierte los datos a lista de diccionarios
            return render_template('tabla.html', resultados=resultados_dict, columnas=columnas)

        # Si es una solicitud GET, carga consulta.html
        return render_template('consulta.html')

    @app.route('/today', methods=['GET'])
    def today():
        # Obtén la fecha y hora actuales
        fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return {"fecha_hora": fecha_hora_actual}

from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# Ruta principal con el formulario para ingresar el correo
@app.route('/')
def index():
    return render_template('index.html')

# Ruta que maneja el formulario y procesa el correo ingresado
@app.route('/procesar_correo', methods=['POST'])
def procesar_correo():
    correo = request.form['correo']
    
    # Ruta al archivo Excel (asumimos que está en la misma carpeta que app.py)
    archivo_excel = os.path.join(os.path.dirname(__file__), 'reparaturen.xlsx')
    
    # Filtrar los datos en fragmentos
    resultados = filtrar_datos_por_correo(archivo_excel, correo)
    
    # Si no hay resultados, enviar un mensaje de error
    if resultados.empty:
        return render_template('tabla.html', mensaje="No se encontraron resultados para ese correo.")
    
    # Obtener las columnas dinámicamente
    columnas = resultados.columns.tolist()
    
    # Convertir los datos filtrados a diccionario para pasarlos al template
    resultados_dict = resultados.to_dict(orient='records')
    
    return render_template('tabla.html', resultados=resultados_dict, columnas=columnas)

# Función que lee el archivo Excel por fragmentos y filtra por correo
def filtrar_datos_por_correo(archivo_excel, correo):
    # Inicializamos un DataFrame vacío para almacenar los resultados
    df_filtrado = pd.DataFrame()
    
    # Usamos pd.ExcelFile para manejar el archivo Excel y fragmentarlo manualmente
    xls = pd.ExcelFile(archivo_excel, engine='openpyxl')
    
    # Definir el tamaño del fragmento
    chunksize = 1000  # Cargar 1000 filas a la vez
    for sheet_name in xls.sheet_names:
        # Cargar cada hoja
        df = pd.read_excel(xls, sheet_name=sheet_name)
        
        # Procesar el DataFrame en fragmentos
        for start in range(0, len(df), chunksize):
            chunk = df.iloc[start:start+chunksize]
            
            # Buscar la columna que contiene "E-Mail:" (con espacio y dos puntos)
            email_column = None
            for column in chunk.columns:
                if "E-Mail:" in column:  # Verificar si el nombre de la columna contiene "E-Mail:"
                    email_column = column
                    break
            
            if email_column is not None:
                # Filtrar el fragmento usando el nombre dinámico de la columna
                filtered_chunk = chunk[chunk[email_column] == correo]
                df_filtrado = pd.concat([df_filtrado, filtered_chunk], ignore_index=True)
            else:
                print(f"No se encontró la columna de correo en la hoja {sheet_name}")
    
    return df_filtrado

if __name__ == '__main__':
    app.run(debug=True)

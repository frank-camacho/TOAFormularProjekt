import pandas as pd
from functools import wraps
from flask import session, redirect, url_for

def filtrar_datos_por_correo(archivo_excel, correo):
    """
    Filtra datos por correo en todas las hojas de un archivo Excel.

    Args:
        archivo_excel (str): Ruta al archivo Excel.
        correo (str): Correo electrónico para filtrar los datos.

    Returns:
        pd.DataFrame: DataFrame con los resultados filtrados. Vacío si no hay coincidencias.
    """
    try:
        # Usamos una lista para acumular los datos de todas las hojas
        df_filtrado = []
        
        # Cargar el archivo Excel
        xls = pd.ExcelFile(archivo_excel, engine='openpyxl')
        
        for sheet_name in xls.sheet_names:
            # Leer cada hoja del Excel
            df = pd.read_excel(xls, sheet_name=sheet_name)
            
            # Verificar si la columna "E-Mail:" existe
            if "E-Mail:" in df.columns:
                # Filtrar las filas que coincidan con el correo
                filtered_chunk = df[df["E-Mail:"].str.strip().str.lower() == correo.strip().lower()]
                df_filtrado.append(filtered_chunk)  # Agregar el resultado a la lista

        # Concatenar todos los fragmentos filtrados
        if df_filtrado:
            df_filtrado = pd.concat(df_filtrado, ignore_index=True)
        else:
            df_filtrado = pd.DataFrame()  # Retornar un DataFrame vacío si no se encontraron resultados

        return df_filtrado

    except Exception as e:
        # Loguear el error y retornar un DataFrame vacío
        print(f"Error al filtrar datos: {e}")
        return pd.DataFrame()

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verificar si el usuario tiene permisos de administrador
        if 'role' not in session or session['role'] != 'admin':
            return redirect(url_for('login'))  # Redirigir a la página de login si no es administrador
        return f(*args, **kwargs)
    return decorated_function
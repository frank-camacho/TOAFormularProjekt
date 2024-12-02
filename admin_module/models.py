import pandas as pd

def filtrar_datos_por_correo(archivo_excel, correo):
    df_filtrado = []  # Usamos una lista para acumular los datos

    # Cargar el archivo Excel
    xls = pd.ExcelFile(archivo_excel, engine='openpyxl')
    chunksize = 1000  # Tamaño del chunk

    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        
        # Verificar si la columna de "E-Mail:" existe en el DataFrame
        if "E-Mail:" in df.columns:
            # Filtrar las filas que coincidan con el correo
            filtered_chunk = df[df["E-Mail:"] == correo]
            df_filtrado.append(filtered_chunk)  # Agregar el resultado a la lista

    # Concatenar todos los fragmentos filtrados al final
    if df_filtrado:
        df_filtrado = pd.concat(df_filtrado, ignore_index=True)
    else:
        df_filtrado = pd.DataFrame()  # Retornar un DataFrame vacío si no se encontraron resultados
    
    return df_filtrado

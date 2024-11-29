import pandas as pd

def filtrar_datos_por_correo(archivo_excel, correo):
    df_filtrado = pd.DataFrame()

    # Cargar el archivo Excel
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

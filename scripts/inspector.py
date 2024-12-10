import os

def buscar_referencias_en_archivos(terminos, directorio='.'):
    """
    Busca referencias específicas en todos los archivos .py y .html de un directorio.
    
    Args:
        terminos (list): Lista de términos a buscar en los archivos.
        directorio (str): Directorio donde buscar los archivos.
        
    Returns:
        dict: Diccionario con el nombre del archivo como clave y las líneas que contienen referencias como valor.
    """
    referencias_encontradas = {}

    # Recorre el directorio para buscar archivos
    for root, _, files in os.walk(directorio):
        for file in files:
            # Solo procesar archivos .py y .html
            if file.endswith('.py') or file.endswith('.html'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for i, line in enumerate(lines, start=1):
                        # Busca términos en cada línea
                        for termino in terminos:
                            if termino in line:
                                if filepath not in referencias_encontradas:
                                    referencias_encontradas[filepath] = []
                                referencias_encontradas[filepath].append((i, line.strip()))

    return referencias_encontradas


if __name__ == '__main__':
    # Términos a buscar
    terminos_a_buscar = ['employees', 'c.execute', 'employee', 'users']
    
    # Directorio base del proyecto
    directorio_base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    # Buscar referencias
    resultados = buscar_referencias_en_archivos(terminos_a_buscar, directorio_base)
    
    # Mostrar resultados
    if resultados:
        print("Referencias encontradas:")
        for archivo, referencias in resultados.items():
            print(f"\n{archivo}:")
            for linea, contenido in referencias:
                print(f"  Línea {linea}: {contenido}")
    else:
        print("No se encontraron referencias.")

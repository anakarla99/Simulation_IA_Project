# import requests
# from bs4 import BeautifulSoup

# # URL de la página de la aplicación en Apklis
# url = 'https://www.apklis.cu/application/cu.geomix.taxis' # o la URL de Mobilweb urbanos

# # Realizar una solicitud GET a la URL
# response = requests.get(url)

# # Verifica que la solicitud fue exitosa
# if response.status_code == 200:
#     html_content = response.text
# else:
#     print("Error al obtener la página")

# # Parsear el contenido de la página con Beautiful Soup
# soup = BeautifulSoup(response.text, 'html.parser')

# # Encuentra el título de la aplicación (esto dependerá de la estructura HTML de la página)
# title = soup.find('h1', class_='app-title')
# print(title)

# # Aquí deberías buscar los elementos específicos que contienen la información que necesitas
# # Por ejemplo, si la información de las rutas está en una tabla, podrías hacer algo como:
# rutas = soup.find_all('div', class_='ruta') # Este es un ejemplo genérico, ajusta según la estructura real de la página

# # Procesar la información extraída
# for ruta in rutas:
#     print(ruta.text) # Imprime la información de cada ruta


# import networkx as nx

# # Crear un grafo dirigido
# G = nx.DiGraph()

# # Añadir vértices (paradas)
# G.add_node("Parada1")
# G.add_node("Parada2")

# # Añadir aristas (rutas)
# G.add_edge("Parada1", "Parada2")

# # Visualizar el grafo
# nx.draw(G, with_labels=True)

# import chardet

# # Detect the file's encoding
# with open('C:/Users/MPC/Downloads/cu.geomix.mwurbanos-v5/res/raw/cuba.map', 'rb') as file:
#     result = chardet.detect(file.read())
#     print(result)

# Open the file with the detected encoding
# with open('C:/Users/MPC/Downloads/cu.geomix.mwurbanos-v5/res/raw/cuba.map', 'r', encoding=result['encoding']) as file:
#     contenido = file.read()
#     print(contenido)

# import pandas as pd
# import sqlite3

# # Especifica la ruta completa a la base de datos
# db_path = r"C:\Users\MPC\Downloads\cu.geomix.mwurbanos-v5\res\raw\omnibus.db"

# # Conectar a la base de datos SQLite
# try:
#     conn = sqlite3.connect(db_path)
# except Exception as e:
#     print(e)

# # Obtener el nombre de las tablas
# cursor = conn.cursor()
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# print(f"Tablas disponibles: {cursor.fetchall()}")

# # Suponiendo que 'nombre_tabla' es el nombre de la tabla que contiene los datos de los mapas
# df = pd.read_sql_query('SELECT * FROM nombre_tabla', conn)
# conn.close()

# # Ahora puedes trabajar con el DataFrame 'df' para analizar los datos
# print(df.head())

def isSQLite3(filename):
    from os.path import isfile, getsize
    if not isfile(filename):
        return False
    if getsize(filename) < 100: # El encabezado de la base de datos SQLite es de 100 bytes
        return False

    with open(filename, 'rb') as fd:
        header = fd.read(100)

    return header[:16] == b'SQLite format 3\x00'

print(isSQLite3(r"C:\Users\MPC\Downloads\cu.geomix.mwurbanos-v5\res\raw\omnibus.db"))

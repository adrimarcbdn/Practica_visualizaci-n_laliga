import requests
from bs4 import BeautifulSoup
import pandas as pd
from unidecode import unidecode

######
##
## En el siguiente programa se cargaran las estadísticas de todos los jugadores de la liga española con sus respectivas estadísticas.
## Se creara una cabecera personalizada y filtraremos todos aquellos jugadores que hayan jugado almenos un partido. Los datos los guardaremos en un CSV
## 
####

# Realizamos la solicitud a la URL de los datos de la liga española. Posteriormente los parseamos con BeautifulSoup
url = 'https://www.futbolfantasy.com/laliga/estadisticas/jugador/2025/todos/total'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extramos todas las tabla y sus filas
table = soup.find('table')
rows = table.find_all('tr')

# Para facilitar el manejo y extracción de los datos, se crea un 'header' personalizado de todas las columnas
header_laliga = [
    "Jugador", "Partidos", "Minutos jugados", "Goles", "Asistencias", "Paradas", "Goles encajados",
    "Tiros", "Tiros a puerta", "Precision tiros (%)", "Centros", "Centros precisos", "Precision centros (%)",
    "Tiros al palo", "Corners forzados", "Faltas recibidas", "Faltas cometidas", "Pases interceptados",
    "Balones robados", "Balones robados al ultimo hombre", "Goles salvados bajos palos", "TA", "TR",
    "Penaltis cometidos", "Penaltis forzados", "Penaltis lanzados", "Penaltis anotados", "Penaltis parados",
    "Goles en propia meta", "Tiros bloqueados", "Errores en gol en contra", "Regates con exito", "Pases claves",
    "Precision de pases (%)", "Corners precisos (en corto)", "Faltas colgadas", "Faltas colgadas precisas",
    "Faltas directas", "Faltas directas a puerta", "Goles de falta", "Despejes efectivos"
]

# Realizamos el proceso de extracción de los datos 
# Creamos una lista para guardar los datos
data_estadisticas = []
for row in rows[1:]:  
    # Extraemos todas las celdas de la fila
    cells = row.find_all('td')
    fila_data = [cell.text.strip() for cell in cells]
    
    # Quitamos caracteres especiales y tildes de todos los nombre
    if fila_data:
        fila_data[0] = unidecode(fila_data[0])  # Quitar tildes solo del nombre
        
        # Para este caso solo añadimos los jugadores que hayan jugado almenos un partido
        if fila_data[1] == '0':
            continue  
    
    # Añadimos los datos
    data_estadisticas.append(fila_data)

# Creamos un DataFrame de pandas con los datos
df_estadistica_laliga = pd.DataFrame(data_estadisticas, columns=header_laliga[:len(data_estadisticas[0])])

# Lo guardamos en formato CSV
df_estadistica_laliga.to_csv('laliga_players.csv', index=False)

print("Archivo: 'laliga_players.csv' creado")

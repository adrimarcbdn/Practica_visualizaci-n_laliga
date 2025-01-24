import json
import csv
from fuzzywuzzy import process
######
##
## En el siguiente programa se cargaran las estadísticas de todos los jugadores de la liga española con sus respectivas estadísticas.
## Se creara una cabecera personalizada y filtraremos todos aquellos jugadores que hayan jugado almenos un partido. Los datos los guardaremos en un CSV
## 
####

# Cargamos los archivos en formato JSON y CSV
with open("equipos_laliga.json", mode="r", encoding="utf-8") as json_file:
    equipos_data = json.load(json_file)

data_futbolistas = []
with open("laliga_players.csv", mode="r", encoding="utf-8") as csv_file:
    csv_dic_reader = csv.DictReader(csv_file)
    data_futbolistas = list(csv_dic_reader)

# Originalmente en nuestro dataframe  los jugadores son registrados con las posiciones en inglés. En este caso traduciremos las posiciones al español.
posiciones_def = {
    'Left Winger': 'Extremo izquierdo',
    'Centre-Back': 'Defensa central',
    'Centre-Forward': 'Delantero centro',
    'Left-Back': 'Lateral izquierdo',
    'Right Winger': 'Extremo derecho',
    'Right-Back': 'Lateral derecho',
    'Attacking Midfield': 'Centrocampista ofensivo',
    'Central Midfield': 'Centrocampista',
    'Goalkeeper': 'Portero',
    'Defensive Midfield': 'Centrocampista defensivo',
    'Second Striker': 'Segundo delantero',
    'Right Midfield': 'Centrocampista derecho'
}

# Realizando un scraping de las paginas web de los equipos, hay algunos nombres que no corresponden con la realidad, por lo que los corregimos
equipos_correccion = {
    "Rel Betis Sevilla": "Real Betis",
    "Real Sociedad San Sebastian": "Real Sociedad"
}

# Construimos un diccionario con toda la información respecto a los jugadores
dic_jugadores = {
    jugador["Jugador"].lower(): {
        "Equipo": equipo,
        "Posición": jugador["Posición"]
    }
    for equipo, jugadores in equipos_data.items()
    for jugador in jugadores
}

# Guaradamos los nombres de los jugadores en una lista para realizar una futura busqueda difusa para la union
json_nombres = list(dic_jugadores.keys())


# Creamos una función para convertir valores a números y poder realizar operaciones sobre ellas
def transf_float(valor):
    try:
        if isinstance(valor, str) and "%" in valor:
            return float(valor.replace("%", ""))
        return float(valor)
    except ValueError:
        return 0 

# Creamos una lista para guardar todos los futbolistas
union_datos_futbolistas = []

# A partir de aqui, empieza la fusión de los datos
for fila in data_futbolistas:
    jugador_nombre = fila["Jugador"].lower()

    # Para realizar el estudio y evitar resultados difusos, solo seleccionaremos todos esos jugadores que hayan jugador más de 30 minutos
    minutos_jugados = int(fila["Minutos jugados"])
    if minutos_jugados <= 30:
        continue  

    # Si el jugador ya es identificable, añadimos su equipo y posición
    if jugador_nombre in dic_jugadores:
        equipo = dic_jugadores[jugador_nombre]["Equipo"]
        posicion = dic_jugadores[jugador_nombre]["Posición"]

    else: # Mas informaciond del proceso 'process': https://github.com/seatgeek/fuzzywuzzy/blob/master/fuzzywuzzy/process.py
        # En aquellos jugadores que no hemos encontrado una coincidencia exacta, realizamos una busqueda difusa y si el umbral es mayor de 0.85 lo añadimos
        mejor_match, score = process.extractOne(jugador_nombre, json_nombres)
        if score >= 85:  
            equipo = dic_jugadores[mejor_match]["Equipo"]
            posicion = dic_jugadores[mejor_match]["Posición"]
        else:
            # Si no hay coincidencia aplicamos NA
            equipo = 'NA'
            posicion = 'NA'
    
    # Traducimos los nombres y corregimos la posicion
    if posicion in posiciones_def:
        posicion = posiciones_def[posicion]
    if equipo in equipos_correccion:
        equipo = equipos_correccion[equipo]
    
    # Añadiremos las filas que contengan un equipo y posición
    if equipo != 'NA' and posicion != 'NA':
        nuevo_registro = {
            "Jugador": fila["Jugador"],
            "Equipo": equipo,
            "Posición": posicion,
        }

        # Para facilitar el manejo de los datos, nos aseguramos de que todos los datos sean float
        for key in fila:
            if key not in ["Jugador", "Equipo", "Posición"]:
                nuevo_registro[key] = transf_float(fila[key])

        # Añadimos el registro
        union_datos_futbolistas.append(nuevo_registro)

# Guardamos los datos en un CSV
with open("laliga_players_union.csv", mode="w", encoding="utf-8", newline="") as merged_file:
    # Añadimos todos los registros posibles
    fieldnames = ["Jugador", "Equipo", "Posición"] + [key for key in data_futbolistas[0].keys() if key not in ["Jugador", "Equipo", "Posición"]]
    dic_Writer = csv.DictWriter(merged_file, fieldnames=fieldnames)
    dic_Writer.writeheader()
    dic_Writer.writerows(union_datos_futbolistas)


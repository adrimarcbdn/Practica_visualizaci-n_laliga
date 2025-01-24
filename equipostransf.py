import sys
import requests
import json
from bs4 import BeautifulSoup
import re
from unidecode import unidecode  
######
##
## Dicho script cargara todos los equipos de la liga española y guardara los datos (jugadores y posiciones) en un archivo JSON.
## Para realizar el scraping usaremos la librería BeautifulSoup y la librería requests para hacer las solicitudes.
## Como la pagina web de transfermarkt bloquea solicitudes usaremos un header para evitarlo.
##
####

# Configuramos la codificación de la salida a UTF-8 
sys.stdout.reconfigure(encoding='utf-8')

# Lista de URLs de equipos pertenecientes a la liga española
equipos_urls = [
    "https://www.transfermarkt.com/real-madrid/startseite/verein/418/saison_id/2024",
    "https://www.transfermarkt.com/fc-barcelona/startseite/verein/131/saison_id/2024",
    "https://www.transfermarkt.com/atletico-madrid/startseite/verein/13/saison_id/2024",
    "https://www.transfermarkt.com/real-sociedad-san-sebastian/startseite/verein/681/saison_id/2024",
    "https://www.transfermarkt.com/athletic-bilbao/startseite/verein/621/saison_id/2024",
    "https://www.transfermarkt.com/fc-valencia/startseite/verein/1049/saison_id/2024",
    "https://www.transfermarkt.com/fc-villarreal/startseite/verein/1050/saison_id/2024",
    "https://www.transfermarkt.com/fc-girona/startseite/verein/12321/saison_id/2024",
    "https://www.transfermarkt.com/real-betis-sevilla/startseite/verein/150/saison_id/2024",
    "https://www.transfermarkt.com/fc-sevilla/startseite/verein/368/saison_id/2024",
    "https://www.transfermarkt.com/ud-las-palmas/startseite/verein/472/saison_id/2024",
    "https://www.transfermarkt.com/ca-osasuna/startseite/verein/331/saison_id/2024",
    "https://www.transfermarkt.com/rcd-mallorca/startseite/verein/237/saison_id/2024",
    "https://www.transfermarkt.com/deportivo-alaves/startseite/verein/1108/saison_id/2024",
    "https://www.transfermarkt.com/celta-vigo/startseite/verein/940/saison_id/2024",
    "https://www.transfermarkt.com/espanyol-barcelona/startseite/verein/714/saison_id/2024",
    "https://www.transfermarkt.com/fc-getafe/startseite/verein/3709/saison_id/2024",
    "https://www.transfermarkt.com/rayo-vallecano/startseite/verein/367/saison_id/2024",
    "https://www.transfermarkt.com/cd-leganes/startseite/verein/1244/saison_id/2024",
    "https://www.transfermarkt.com/real-valladolid/startseite/verein/366/saison_id/2024"
]

# Headers con la información del User-Agent
# Mas información del User-Agent usado en: https://www.zenrows.com/blog/web-scraping-headers
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0"
}

# Creamos un diccionario para guardar los datos procedentes de los equipos
data_equipos = {}

# Recorrer cada URL de equipo
for url in equipos_urls:
    # Realizar la solicitud GET a la URL del equipo y las parseamos con BeautifulSoup
    print(f"Scraping del equipo: {url}")
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # En este caso despues de hacer una exploración de la pagina web, observamos que los datos de los jugadores y sus posiciones están en tablas con la clase 'inline-table'
    tables = soup.find_all('table', class_='inline-table')

    # Creamos una lista para guardar los jugadores y sus posiciones
    jugadores = []

    # Recorremos las tablas para extraer los datos de los jugadores y sus posiciones
    for table in tables:
        jugador_celda = table.find('td', class_='hauptlink')
        if jugador_celda:
            nombre = jugador_celda.get_text(strip=True)
            
            # Limpiamos de tildes y caracteres inutiles
            nombre_abc = unidecode(nombre)
            
            # Buscamos la celda que contiene la posicion del jugador
            posicion_celda = table.find_all('td')[-1]  
            if posicion_celda:
                posicion = posicion_celda.get_text(strip=True)
                
                # Añadimos los jugadores y su posición a la lista	
                jugadores.append({"Jugador": nombre_abc, "Posición": posicion})

    # Obtenemos el nombre del equipo desde la url del equipo. Nos quedamos con el cuarto elemento de la url
    nombre_equipo = url.split('/')[3].replace('-', ' ').title()

    # Limpiamos el nombre igual que hicimos con los jugadores
    nombre_equipo_abc = unidecode(nombre_equipo)

    # Añadimos los jugadores y sus posiciones al diccionario de los equipos
    data_equipos[nombre_equipo_abc] = jugadores

# Guardamos los datos en un archivo JSON
with open("equipos_laliga.json", mode='w', encoding='utf-8') as json_file:
    json.dump(data_equipos, json_file, ensure_ascii=False, indent=4)

print("Data de la liga española guardado en: equipos_laliga.json")
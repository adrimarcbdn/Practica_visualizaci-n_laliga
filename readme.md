# Visualización de datos

En dicho proyecto se realiza la visualización de datos con un gráfico de radar para observar las estadisticas de los jugadores de la liga española

## Archivos

El repositorio contiene una serie de archivos con tal de ejecutar el desarrollo de la practica:

1. **equipostransf.py**: Obtenemos los jugadores y equipos de la liga española.
2. **futbolfantasy.py**: Contiene una lista con todos los jugadores de la liga española con sus respectivas estadísticas.
3. **merge.py**: Combina los datos de la plataforma de transfermaket y futbolfantasy.
4. **app.py**: Ejecuta la aplicación para mostrar el grafico de radar.

## Requisitos
En primer lugar para poder ejecutar los scripts, debemos asegurarnos de que tenemos todos los paquetes necesarios. En primer lugar debemos instalar y ejecutar el archivo `requirements.txt`


1. En primer lugar, ejecutamos 'pip install -r requirements.txt' 
2. En segundo lugar deberemos ejecutar el archivo futbolfantasy.py 'python futbolfantasy.py'
3. En tercer lugar ejecutamos el archivo equipostransf.py 'python equipostransf.py' 
4. En cuarto lugar ejecutamos el archivo correspondiente a la unión 'python merge.py'
5. Para acabar ejecutamos el archivo que corresponde a la generación del gráfico 'app.py'

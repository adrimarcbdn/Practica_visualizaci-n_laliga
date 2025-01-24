import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

######
##
## En el siguiente codigo se procedera a cargar los datos de los jugadores de la liga española y se creara un radar para mostrar toda la información de los jugadores y equipos
## 1) En primer lugar cargaremos los datos y categorizaremos las posiciones. Seleccionaremos las variables que se mostraran por posición y diseñaremos el layout de la aplicación
## 2) En esta segunda parte diseñaremos la interfaz del usuario. Mostraremos el titulo de la pagina. Crearemos un dropdown para seleccionar equipo o jugador.
##    También crearemos un contentendor para poner el nombre del jugador y otro para seleccionar el equipo y la posición. Ademas crearemos filtros para ver o no la media de la liga y el equipo
## 3) La tercera parte corresponde a la sección de los callbacks. Actualizaremos todos los elementos de la interfaz conforme el usuario vaya actualizando las entradas
## 4) La ultima corresponde a la creación de la función para su funcionamiento. Dicha función siempre se actualizara conforme el usuario escoga una opción o actualize
## 4) Filtraremos segun si escogemos equipo o jugador y a partir de ahi filtraremos los datos pertinentes. 
## 4) Para acabar llamaremos a la app para que haga la ejecucion
##
####

##
# 1a parte
##


# Cargamos los datos
datos_jugadores_laliga = pd.read_csv('laliga_players_union.csv')

# Categorizamos las posiciones para el analisis
posiciones_generales = {
    'Extremo izquierdo': 'Delantero',
    'Extremo derecho': 'Delantero',
    'Delantero centro': 'Delantero',
    'Segundo delantero': 'Delantero',
    'Defensa central': 'Defensa',
    'Lateral izquierdo': 'Defensa',
    'Lateral derecho': 'Defensa',
    'Portero': 'Portero',
    'Centrocampista': 'Mediocampo',
    'Centrocampista ofensivo': 'Mediocampo',
    'Centrocampista defensivo': 'Mediocampo',
    'Centrocampista derecho': 'Mediocampo'
}

# Mapeamos las posiciones
datos_jugadores_laliga['Cat_posiciones'] = datos_jugadores_laliga['Posición'].map(posiciones_generales)

# Mostramos que variables seran presenciadas por cada posicion
variables_posicion = {
    'Portero': ['Paradas', 'Goles encajados', 'Partidos', 'Minutos jugados', 'Penaltis parados'],
    'Defensa': ['Partidos', 'Minutos jugados', 'Balones robados', 'Balones robados al ultimo hombre',
                'Despejes efectivos', 'Pases interceptados', 'Tiros bloqueados', 'Precision de pases (%)',
                'Penaltis cometidos'],
    'Mediocampo': ['Partidos', 'Minutos jugados', 'Precision de pases (%)', 'Asistencias', 'Pases claves',
                   'Goles', 'Faltas cometidas'],
    'Delantero': ['Partidos', 'Minutos jugados', 'Goles', 'Asistencias', 'Tiros', 'Tiros a puerta',
                  'Precision tiros (%)', 'Centros', 'Centros precisos', 'Precision centros (%)', 'Regates con exito']
}

# Arrancamos la aplicación con opciones personalizadas de Bootstrap y con la supresión de excepciones. Ademas añadimos el estilo de la pagina principal
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        <div id="root">{%app_entry%}</div>
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <style>
            html, body {
                margin: 0;
                padding: 0;
                height: 100%;
                overflow: hidden;
            }
            #root {
                height: 100%;
            }
        </style>
    </body>
</html>
'''
##
# 2a parte
##
# Creamos la interfaz de usuario
app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(html.H1("Radar de LALIGA EA SPORTS 24/25", className="text-center my-4", style={'color': 'white'}), width=12)
    ),
    dbc.Col([  
        dbc.Row([
            dbc.Col([
                # Creamos el dropdown para seleccionar equipo o jugador
                html.Label("Selecciona 'Equipo' o 'Jugador':", className="form-label", style={'color': 'white'}),
                dcc.Dropdown(
                    id='tipo_eleccion',
                    options=[
                        {'label': 'Equipo', 'value': 'equipo'},
                        {'label': 'Jugador', 'value': 'jugador'}
                    ],
                    value='jugador',
                    style={
                        'box-shadow': 'none',
                        'border-radius': '10px',
                        'padding': '5px',
                        'width': '30%',
                        'color': 'black'
                    }
                )
            ], width=12, style={'padding-right': '5px'}),
        ], className="mb-3"),
        # Creamos el contenedor para el nombre del jugador
        html.Div(id='jugador_container', children=[
            dbc.Row([dbc.Col(html.Label("Escribe el nombre del jugador:", className="form-label", style={'color': 'white'}), width=12)]),
            dbc.Row([dbc.Col(dcc.Input(
                id='jugador_entrada',
                type='text',
                value='',
                style={
                    'border': '1px solid #ccc',
                    'box-shadow': 'none',
                    'border-radius': '10px',
                    'padding': '5px',
                    'width': '20%',
                    'color': 'black'
                }
            ), width=12)])
        ], style={
            'background': 'linear-gradient(to bottom, #0a0a0a, #1a1a1a)',
            'min-height': '100vh',
            'height': '100vh',
            'padding': '0',
            'margin': '0',
            'overflow': 'hidden'
        }),
        # Creamos el contendemos donde seleccionaremos el equio y la posición
        html.Div(id='equipo_container', children=[
            dbc.Row([
                dbc.Col([
                    html.Label("Selecciona un equipo:", className="form-label", style={'color': 'white'}),
                    dcc.Dropdown(
                        id='team-input',
                        options=[{'label': equipo, 'value': equipo} for equipo in datos_jugadores_laliga['Equipo'].unique()],
                        style={
                            'box-shadow': 'none',
                            'border-radius': '10px',
                            'padding': '5px',
                            'width': '90%',
                            'color': 'black'
                        }
                    )
                ], width=3),
                dbc.Col([
                    html.Label("Selecciona una posición:", className="form-label", style={'color': 'white'}),
                    dcc.Dropdown(
                        id='posicion_eleccion',
                        options=[{'label': posicion, 'value': posicion} for posicion in variables_posicion.keys()],
                        style={
                            'box-shadow': 'none',
                            'border-radius': '10px',
                            'padding': '5px',
                            'width': '90%',
                            'color': 'black'
                        }
                    )
                ], width=3)
            ])
        ], style={
            'display': 'none',
            'background': 'linear-gradient(to bottom, #0a0a0a, #1a1a1a)',
            'padding': '10px',
            'border-radius': '10px'
        }),
        dbc.Row(
            dbc.Col(
                # Creamos las checklist de las posiciones
                dbc.Checklist(
                    id='mostrar_fondo',
                    options=[
                        {'label': 'Media del equipo', 'value': 'mostrar_equipo'},
                        {'label': 'Media de la liga', 'value': 'mostrar_liga'}
                    ],
                    value=[],
                    inline=False,
                    switch=True,
                    style={'color': 'white'}
                ), width=12
            ), className="mb-3"
        ),
    ], width=12),
    dbc.Row(
        dbc.Col(html.Div(id='grafico_container'), width=12), className="mb-3"
    )
], fluid=True, style={
    'background': 'linear-gradient(to bottom, #0a0a0a, #1a1a1a)',
    'height': '100vh',
    'padding': '20px'
})

##
# 3a parte
##
# Creamos los callbacks
@app.callback(
    [Output('grafico_container', 'children'),
     Output('jugador_container', 'style'),
     Output('equipo_container', 'style'),
     Output('mostrar_fondo', 'options')], 
    [Input('tipo_eleccion', 'value'), Input('jugador_entrada', 'value'), Input('team-input', 'value'),
     Input('posicion_eleccion', 'value'), Input('mostrar_fondo', 'value')]
)

##
# 4a parte
##

# Creamos la funcion actualizar radar donde acutaliremos el radar segun la experencia del usuario
def actualizar_radar(tipo_seleccion, nombre_jugador, equipo_nombre, posicion_nombre, mostrar_fondo_pagina):
    # En primer lugar configuramos si seleccionamos un jugador
    if tipo_seleccion == 'jugador':
        opciones_filtros_activos = [
            {'label': 'Media del equipo', 'value': 'mostrar_equipo'},
            {'label': 'Media de la liga', 'value': 'mostrar_liga'}
        ]
        if not nombre_jugador or nombre_jugador not in datos_jugadores_laliga['Jugador'].values:
            return None, {'display': 'block'}, {'display': 'none'}, opciones_filtros_activos
        
        # Filtramos los datos del jugador
        datos_jugador = datos_jugadores_laliga[datos_jugadores_laliga['Jugador'] == nombre_jugador]
        posicion_categorica = datos_jugador['Cat_posiciones'].iloc[0]
        columna_activa = variables_posicion[posicion_categorica]
        datos_posicion = datos_jugadores_laliga[datos_jugadores_laliga['Cat_posiciones'] == posicion_categorica]
        
        # Normalizamos los datos
        datos_jugador_normalizados = datos_jugador.copy()
        for column in columna_activa:
            valor_minimo = datos_posicion[column].min()
            valor_maximo = datos_posicion[column].max()
            datos_jugador_normalizados[column] = (datos_jugador[column] - valor_minimo) / (valor_maximo - valor_minimo)

        valores_jugores_normalizados = datos_jugador_normalizados[columna_activa].iloc[0].tolist()

        # En este caso nos interesa tener el valor real de las estadisitcas del jugador, ya que al hacer el hoover mostraremos los valores reales
        valores_jugador_real = datos_jugador[columna_activa].iloc[0].tolist()

        fig = go.Figure()

        # Mostramos la información correspondiente a la media del equipo
        if 'mostrar_equipo' in mostrar_fondo_pagina:
            equipo_nombre = datos_jugador['Equipo'].iloc[0]
            datos_equipo = datos_jugadores_laliga[datos_jugadores_laliga['Equipo'] == equipo_nombre]
            equipos_media = datos_equipo[columna_activa].mean().tolist()
            equipos_medias_normalizadas = [(val - datos_posicion[col].min()) / (datos_posicion[col].max() - datos_posicion[col].min()) for val, col in zip(equipos_media, columna_activa)]

            fig.add_trace(go.Scatterpolar(
                r=equipos_medias_normalizadas + equipos_medias_normalizadas[:1],
                theta=columna_activa + [columna_activa[0]],
                fill='toself',
                name=f'Media del {equipo_nombre}',
                line=dict(color='rgba(0, 0, 255, 0.3)')
            ))

        fig.add_trace(go.Scatterpolar(
            r=valores_jugores_normalizados + valores_jugores_normalizados[:1],
            theta=columna_activa + [columna_activa[0]],
            text=valores_jugador_real + valores_jugador_real[:1],
            hoverinfo='text+theta',
            fill='toself',
            name=nombre_jugador,
            line=dict(color='rgba(255, 0, 0, 0.7)', width=2)
        ))

        # Mostramos la información correspondiente a la media de la liga.
        if 'mostrar_liga' in mostrar_fondo_pagina:
            media_liga = datos_posicion[columna_activa].mean().tolist()
            media_liga_normalizada = [(val - datos_posicion[col].min()) / (datos_posicion[col].max() - datos_posicion[col].min()) for val, col in zip(media_liga, columna_activa)]
            fig.add_trace(go.Scatterpolar(
                r=media_liga_normalizada + media_liga_normalizada[:1],
                theta=columna_activa + [columna_activa[0]],
                fill='toself',
                name='Media de la liga',
                line=dict(color='rgba(0, 255, 0, 0.3)')
            ))

        fig.update_layout(
            polar=dict(bgcolor='rgba(214, 214, 214)', radialaxis=dict(visible=True, range=[0, 1], tickvals=[], ticktext=[], linewidth=0)),
            height=400, 
            margin=dict(l=20, r=20, t=50, b=20),
            paper_bgcolor='rgba(0, 0, 0, 0)',
            plot_bgcolor='rgba(0, 2, 44, 0)',
            showlegend=True,
            title=dict(text=f"Rendimiento del jugador {nombre_jugador}", font=dict(color='white')),
            font=dict(color='white')
        )

        return dcc.Graph(figure=fig), {'display': 'block'}, {'display': 'none'}, opciones_filtros_activos

    # A continuación (como contraposición) configuramos si seleccionamos un equipo
    elif tipo_seleccion == 'equipo':
        # En este caso solo mostraremos la media de la liga unicamnte, pues no tiene sentido mostrar la media del equipo ya que es el visualización principal
        opciones_filtros_activos = [
            {'label': 'Media de la liga', 'value': 'mostrar_liga'}
        ]
        if not equipo_nombre or not posicion_nombre:
            return None, {'display': 'none'}, {'display': 'block'}, opciones_filtros_activos

        datos_equipo = datos_jugadores_laliga[(datos_jugadores_laliga['Equipo'] == equipo_nombre) & (datos_jugadores_laliga['Cat_posiciones'] == posicion_nombre)]
        if datos_equipo.empty:
            return None, {'display': 'none'}, {'display': 'block'}, opciones_filtros_activos

        # Procedemos a la normalización de los datos
        columna_activa = variables_posicion[posicion_nombre]
        datos_posicion = datos_jugadores_laliga[datos_jugadores_laliga['Cat_posiciones'] == posicion_nombre]
        
        equipos_media = [round(val, 2) for val in datos_equipo[columna_activa].mean().tolist()]
        equipos_medias_normalizadas = [(val - datos_posicion[col].min()) / (datos_posicion[col].max() - datos_posicion[col].min()) for val, col in zip(equipos_media, columna_activa)]

        fig = go.Figure()

        # Mostramos la información correspondiente a la media de la liga.
        if 'mostrar_liga' in mostrar_fondo_pagina:
            media_liga = datos_posicion[columna_activa].mean().tolist()
            media_liga_normalizada = [(val - datos_posicion[col].min()) / (datos_posicion[col].max() - datos_posicion[col].min()) for val, col in zip(media_liga, columna_activa)]
            fig.add_trace(go.Scatterpolar(
                r=media_liga_normalizada + media_liga_normalizada[:1],
                theta=columna_activa + [columna_activa[0]],
                fill='toself',
                name='Media de la liga',
                line=dict(color='rgba(0, 255, 0, 0.3)')
            ))

        fig.add_trace(go.Scatterpolar(
            r=equipos_medias_normalizadas + equipos_medias_normalizadas[:1],
            theta=columna_activa + [columna_activa[0]],
            text=equipos_media + equipos_media[:1],
            hoverinfo='text+theta',
            fill='toself',
            name=f"{equipo_nombre} ({posicion_nombre})",
            line=dict(color='rgba(212, 6, 103, 0.7)', width=2)
        ))

        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1], tickvals=[], ticktext=[], linewidth=0)),
            height=440, 
            paper_bgcolor='rgba(0, 0, 0, 0)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            showlegend=True,
            title=dict(text=f"Rendimiento del {equipo_nombre} - {posicion_nombre}", font=dict(color='white')),
            font=dict(color='white')
        )

        return dcc.Graph(figure=fig), {'display': 'none'}, {'display': 'block'}, opciones_filtros_activos
    
# Llamamos a la app para su ejecución
if __name__ == '__main__':
    app.run_server(debug=False, use_reloader=False)

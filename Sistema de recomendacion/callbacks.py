from dash.dependencies import Input, Output, State
import requests
import dash
from dash import html
import plotly.express as px
import pandas as pd
from motor_recomendacion import recomendacion
from translations import translations

def generate_cards(df,lat,lon):
        cards = []
    
        for index, row in df.iterrows():

            maps_link = f"https://www.google.com/maps/embed/v1/directions?key=AIzaSyAl0MF0V7fkoJuFFvxpTE7JioPh3hL3KRU&origin={lat},{lon}&destination={row['lat']},{row['lon']}"
        
            card_content = [
                html.H5(row['name'], className="card-title"),
                html.P(f"Address: {row['address']}", className="card-text"),
                html.P(f"Distance: {row['distance']} km", className="card-text"),
                html.A('Search in Google', href=f"https://www.google.com/search?q={row['name']}+restaurant", target="_blank", className="btn btn-primary google-btn"),
                html.Iframe(src=maps_link, style={'width': '100%', 'height': '300px'}),  # Añade el iframe aquí
                ]
            card = html.Div(
                card_content,
                className="card",
                style={
                    'width': '18rem',
                    'margin': '10px',
                    'backgroundColor': '#f5f5f5'  # gris clarito
                }
            )
            cards.append(card)

        return html.Div(cards, className="d-flex flex-wrap justify-content-around")

def register_callbacks(app, df):
    @app.callback(
    [Output('submit-address', 'className', allow_duplicate= True), 
     Output('submit-address', 'children', allow_duplicate= True),
     Output('recommendation-cards', 'children')],
    [Input('submit-address', 'n_clicks')],
    [State('address-input', 'value'),
     State('user-text-input', 'value'),
     State('submit-address', 'className')],
    prevent_initial_call=True
)
    def mark_address_on_map(n_clicks, address, user_input, current_class):
        
        if not address or not user_input:
            return dash.no_update, dash.no_update, dash.no_update

        # Si todo está en orden, realiza la solicitud:
        base_url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': address,
            'format': 'json'
        }
        response = requests.get(base_url, params=params)
        data = response.json()

        if not data:
            return dash.no_update, "Dirección no encontrada.", 'recommendation-button', 'Buscar recomendación'

        lat = float(data[0]['lat'])
        lon = float(data[0]['lon'])

        engine = recomendacion()
        df_recomendados = engine.main(user_input, (lat, lon))

        df_recomendados['lat'] = df_recomendados['coord'].apply(lambda x: x[0])
        df_recomendados['lon'] = df_recomendados['coord'].apply(lambda x: x[1])

         # Crear un DataFrame para los puntos del mapa (incluyendo el punto del usuario)
        df_map = pd.DataFrame({
        'lat': [lat] + df_recomendados['lat'].tolist(),
        'lon': [lon] + df_recomendados['lon'].tolist(),
        'text': ["Tu Ubicacion"] + df_recomendados['name'].tolist(),
        'color': ['blue'] + ['red'] * len(df_recomendados)
        })
       
        table_data = df_recomendados[['name','address','distance']].to_dict('records')

        cards = generate_cards(df_recomendados[['name','address','distance', 'lat', 'lon']], lat, lon)

        return 'recommendation-button', 'Buscar recomendación', cards

    
    @app.callback(
    Output('dropdown-menu', 'style'),
    Input('menu-icon', 'n_clicks')
    )
    def toggle_menu(n_clicks):
        if n_clicks % 2 == 0:  # Si es un número par de clics, oculta el menú
            return {'width': '0%'}
        else:  # Si es un número impar de clics, muestra el menú
            return {'width': '20%'}
    
    @app.callback(
        [
            Output('header-title', 'children'),
            Output('user-text-input', 'placeholder'),
            Output('address-input', 'placeholder'),
            Output('submit-address', 'className'),
            Output('submit-address', 'children')
        ],
        [
            Input('submit-address', 'n_clicks'),
            Input('language-store', 'data')
        ],
        [
            State('address-input', 'value'),
            State('user-text-input', 'value'),
            State('submit-address', 'className'),
        ],
        prevent_initial_call=True
    )
    def combined_callback(n_clicks, data, address, user_input, current_class):
        ctx = dash.callback_context
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        lang = data.get('language', 'es') if data else 'es'

        # Si el botón de enviar fue presionado
        if triggered_id == 'submit-address':
            if not address or not user_input:
                return (dash.no_update, dash.no_update, dash.no_update,
                        'recommendation-button error-animation', translations[lang]['error_message'])
            else:
                if 'rotating-button' not in current_class:
                    return (dash.no_update, dash.no_update, dash.no_update,
                            'recommendation-button rotating-button', translations[lang]['searching_message'])
            
        # Si el almacenamiento del idioma fue el que desencadenó el callback
        elif triggered_id == 'language-store':
            language = data['language']
            return (
                translations[language]['title'],
                translations[language]['placeholder_food'],
                translations[language]['placeholder_address'],
                dash.no_update,  # No actualizamos className
                translations[language]['btn_recommendation']
            )

        # En caso de que ningún input haya desencadenado el callback (no debería ocurrir, pero es una buena práctica tener esto)
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    @app.callback(
        Output('language-store', 'data'),
        [Input('lang-button-en', 'n_clicks'),
        Input('lang-button-es', 'n_clicks')],
        prevent_initial_call=True
    )
    def update_language_store(btn_en_clicks, btn_es_clicks):
        ctx = dash.callback_context
        if not ctx.triggered:
            return dash.no_update
        else:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if button_id == 'lang-button-en':
                return {'language': 'en'}
            elif button_id == 'lang-button-es':
                return {'language': 'es'}

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(
        id='world-map',
        figure=go.Figure(
            go.Scattergeo(
                lat=[],
                lon=[],
                mode='markers',
                projection=dict(type='natural earth'),  # Specify the projection type
                title="Haz clic en el mapa para obtener las coordenadas",
            )
        )
    ),
    html.Div(id='coordenadas')
])

@app.callback(
    [Output('world-map', 'figure'),
     Output('coordenadas', 'children')],
    [Input('world-map', 'clickData')]
)
def display_click_data(clickData):
    if clickData is not None:
        latitud = clickData['points'][0]['lat']
        longitud = clickData['points'][0]['lon']
        updated_fig = go.Figure(
            go.Scattergeo(
                lat=[latitud],
                lon=[longitud],
                mode='markers',
                projection=dict(type='natural earth'),  # Specify the projection type
                title=f'Coordenadas: Latitud={latitud}, Longitud={longitud}',
            )
        )
        updated_fig.update_geos(
            lonaxis=dict(range=[-180, 180]),
            lataxis=dict(range=[-90, 90]),
            resolution=50  # Adjust resolution for more detail
        )
        return updated_fig, f'Coordenadas: Latitud={latitud}, Longitud={longitud}'
    else:
        default_fig = go.Figure(
            go.Scattergeo(
                lat=[],
                lon=[],
                mode='markers',
                projection=dict(type='natural earth'),  # Specify the projection type
                title="Haz clic en el mapa para obtener las coordenadas",
            )
        )
        default_fig.update_geos(
            lonaxis=dict(range=[-180, 180]),
            lataxis=dict(range=[-90, 90]),
            resolution=50  # Adjust resolution for more detail
        )
        return default_fig, 'Haz clic en el mapa para obtener las coordenadas.'

if __name__ == '__main__':
    app.run_server(debug=True)

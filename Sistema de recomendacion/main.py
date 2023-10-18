import dash
import pandas as pd
import plotly.express as px
from layout import get_layout
from callbacks import register_callbacks
import dash_bootstrap_components as dbc

df = pd.DataFrame({
    'lat': [40.25],
    'lon': [-74.70],
    'city': ['New York'],
})

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = get_layout()

register_callbacks(app, df)

if __name__ == '__main__':
    app.run_server(debug=True)

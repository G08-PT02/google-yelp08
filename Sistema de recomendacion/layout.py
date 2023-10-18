from dash import dcc, html
from dash import dash_table
from translations import translations


def get_layout():
    return html.Div(className='background', children=[
        html.Link(href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap", rel="stylesheet"),
        
        html.Header(children=[
    html.Div('Sistema de recomendación de restaurantes', id='header-title', style={'margin-left': '32%', 'flex': 2, 'fontstyle': 'Roboto'}),

   html.Div([
    html.Button([
        html.Img(src='/assets/en_logo.png', style={'width': '40px', 'height': '40px', 'margin-right': '5px', 'background-color': 'transparent'})
    ], id="lang-button-en", className="language-button"),
    
    html.Button([
        html.Img(src='/assets/es_logo.png', style={'width': '40px', 'height': '40px', 'margin-right': '5px','background-color': 'transparent'})
    ], id="lang-button-es", className="language-button"),
    ], style={'margin-left': 'auto', 'margin-right': '10px','background-color': 'transparent'}),  # Mueve esta div a la derecha

], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'space-between', 'padding': '10px','background': 'linear-gradient(135deg, #839aff, #0859c4)', 'fontSize': '24px','box-shadow': '0px 4px 10px rgba(0, 0, 0, 0.2)'}),


        dcc.Store(id='language-store', data={'language': 'es'}),

        # Ícono del menú (barritas)
        html.Div(id="menu-icon", style={'margin-top':'10px'}, n_clicks=0, children=[
            html.Div(className="bar"),
            html.Div(className="bar"),
            html.Div(className="bar")
        ]),
        
        # Menú desplegable
        html.Div(id="dropdown-menu", style={'width': '0%'}, children=[
        html.A([
        html.Img(src="assets\powerbi.png", style={'width': '40px', 'height': '40px', 'margin-right': '5px'}),
        "Dashboard"
        ], href="https://app.powerbi.com/links/5XmzBHm1Jl?ctid=d4f48ae9-784c-4427-b85b-6610e6a41112&pbi_source=linkShare", className='custom-link'),
        html.A([
        html.Img(src="assets\GitHUbIcon.png", style={'width': '40px', 'height': '40px', 'margin-right': '5px'}),
        "GitHub"
        ], href="#", className='custom-link'),
        html.A([
        html.Img(src="assets\WhatsApp.png", style={'width': '40px', 'height': '40px', 'margin-right': '5px'}),
        "Contact Us"
        ], href="#", className='custom-link')
]),


        dcc.Interval(
        id='interval-component',
        interval=1*1000, # in milliseconds, checks every second
        n_intervals=0
        ),


        html.Div(
            style={
                'position': 'relative',
                'display': 'flex',
                'justifyContent': 'center',
                'alignItems': 'center',
                'width': '80%',
                'margin': '150px auto'
            },
            children=[
                # Marco de fondo
                html.Img(
                    src="/assets/Marco_Input.png",
                    style={
                        'position': 'absolute',
                        'width': '60%',  # o la anchura que desees para el marco
                        'zIndex': '1'
                    }
                ),
                # Cuadro de texto
                dcc.Input(
                    id='user-text-input', 
                    type='text', 
                    placeholder='¿Que se te antoja?', 
                    style={
                        'width': '34%',  # Ajusta el ancho para que la caja de texto quede dentro del marco
                        'padding': '10px',
                        'borderRadius': '15px',
                        'zIndex': '2',
                        'box-shadow': '0px 4px 10px rgba(0, 0, 0, 0.2)'  # Esto asegura que el cuadro de texto esté encima del marco
                    }
                )
            ]
        ),

        html.Div([
            dcc.Input(id='address-input', type='text', placeholder='Ingresa tu dirección', style={'width': '50%', 'padding': '10px', 'margin': '10px', 'borderRadius': '15px', 'box-shadow': '0px 4px 10px rgba(0, 0, 0, 0.2)'}),
            html.Button([
        html.Span('Buscar recomendación', className='button-text'),
        html.Span('Buscar... 🔍', className='button-icon')  # Usando el emoji de lupa para simplicidad, pero puedes usar &#128269; o íconos de bibliotecas
    ], id='submit-address', className='recommendation-button', style={'width': '15%', 'padding': '10px', 'marginTop': '5px', 'backgroundColor': '#007BFF', 'color': 'white', 'borderRadius': '15px'}), 
], style={'display': 'flex', 'justifyContent': 'center', 'padding': '5px'}),

        html.Div(id='recommendation-cards', className="d-flex flex-wrap justify-content-around", style={'width': 'auto', 'padding': '10px'}),
        html.Div(id='separador', style={'width': '100px','height' : '150px', 'padding': '10px'})
        ])


from flask import Flask, render_template_string, request
from geopy.distance import geodesic

app = Flask(__name__)

# Datos de muestra para restaurantes.
restaurantes = [
    {"nombre": "Restaurante A", "direccion": "123 Calle A", "coord": (40.720, -74.050)},
    {"nombre": "Restaurante B", "direccion": "456 Calle B", "coord": (40.710, -74.040)},
    {"nombre": "Restaurante C", "direccion": "789 Calle C", "coord": (40.700, -74.030)},
]

@app.route('/', methods=['GET', 'POST'])
def index():
    recomendacion = []

    if request.method == 'POST':
        lat = float(request.form.get('lat'))
        lon = float(request.form.get('lon'))
        comida_input = request.form.get('comida_input')

        print(f"Datos recibidos: lat={lat}, lon={lon}, comida_input={comida_input}")

        recomendacion = modelo_recomendacion(lat, lon, comida_input)

    return render_template_string("""
        <html>
            <head>
                <title>Mapa interactivo con Leaflet.js</title>
                <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css"/>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        padding: 50px;
                        text-align: center;
                    }
                    
                    #mapid { 
                        height: 400px; 
                        width: 80%; 
                        margin: 2% auto; 
                        border-radius: 8px;
                    }
                    
                    form {
                        margin-bottom: 20px;
                        background-color: #fff;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                    }
                    
                    label {
                        display: block;
                        margin-bottom: 10px;
                    }

                    input[type="text"] {
                        width: 100%;
                        padding: 10px;
                        margin-bottom: 10px;
                        border: 1px solid #ccc;
                        border-radius: 4px;
                    }

                    input[type="submit"] {
                        display: block;
                        width: 100%;
                        padding: 10px;
                        background-color: #007BFF;
                        border: none;
                        color: white;
                        border-radius: 4px;
                        cursor: pointer;
                    }

                    input[type="submit"]:hover {
                        background-color: #0056b3;
                    }

                    p {
                        background-color: #fff;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                    }
                </style>
            </head>
            <body>
                <form method="post">
                    <label for="comida_input">¿Qué deseas comer?</label>
                    <input type="text" id="comida_input" name="comida_input">
                    <input type="hidden" id="lat" name="lat">
                    <input type="hidden" id="lon" name="lon">
                    <input type="submit" value="Buscar">
                </form>
                {% if recomendaciones %}
                    <h2>Recomendaciones para ti</h2>
                    <ul>
                        {% for restaurante in recomendaciones %}
                            <li>
                                <strong>Nombre:</strong> {{ restaurante.nombre }}<br>
                                <strong>Dirección:</strong> {{ restaurante.direccion }}<br>
                                <strong>Distancia:</strong> {{ restaurante.distancia }} km<br>
                            </li>
                        {% endfor %}
                    </ul>
                {% endif %}
                <div id="mapid"></div>

                <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
                <script>
                    var map = L.map('mapid').setView([40.7128, -74.0060], 13);
                    var currentMarker;

                    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

                    map.on('click', function(e) {
                        if (currentMarker) {
                            map.removeLayer(currentMarker);
                        }

                        currentMarker = L.marker(e.latlng).addTo(map);
                        document.getElementById('lat').value = e.latlng.lat;
                        document.getElementById('lon').value = e.latlng.lng;
                    });
                </script>
            </body>
        </html>
    """, recomendaciones=recomendacion)

def modelo_recomendacion(lat, lon, comida_input):
    ubicacion_usuario = (lat, lon)
    
    lista_recomendaciones = []
    
    for restaurante in restaurantes:
        distancia = geodesic(ubicacion_usuario, restaurante["coord"]).kilometers
        lista_recomendaciones.append({
            "nombre": restaurante["nombre"],
            "direccion": restaurante["direccion"],
            "distancia": round(distancia, 2)
        })

    lista_recomendaciones.sort(key=lambda x: x["distancia"])

    print(f"Recomendaciones: {lista_recomendaciones}")

    return lista_recomendaciones[:3]

if __name__ == '__main__':
    app.run(debug=True)

# google-yelp08
Repositorio de Proyecto Final de Data Science Grupo 08 PT02

# Sistema de Recomendación

Este proyecto presenta una interfaz de usuario diseñada para interactuar con un modelo de recomendación. A través de esta interfaz, los usuarios pueden recibir recomendaciones basadas en diferentes criterios y parámetros que se ajusten a sus necesidades.

## Tabla de Contenidos
- [Descripción General](#descripción-general)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Características de la Interfaz](#características-de-la-interfaz)
- [Integración con el Modelo de Recomendación](#integración-con-el-modelo-de-recomendación)
- [Instrucciones de Instalación](#instrucciones-de-instalación) 
- [Contribuidores](#contribuidores)

# Descripción General

Descripción breve del propósito del sistema y su importancia.

# Tecnologías Utilizadas
- CUDA : Procesamiento en paralelo con chips de la marca NVIDIA
- NPL: Procesamiento de lenguaje natural con un modelo pre-entrenado

## Modelo de recomendacion
- Python: Lenguaje principal para el desarrollo del backend.
- Numpy: Utilizado para cálculos y manipulaciones de datos.
- Pandas: Es una librería de Python para trabajar con datos en forma de tablas flexibles llamadas DataFrames.
- PyTorch: Framework de Python para aprendizaje profundo.
- Math: Biblioteca de funciones matemáticas en Python.
- scikit-learn (sklearn): Biblioteca de Python para aprendizaje automático y minería de datos con herramientas sencillas y eficientes para análisis predictivo y modelado estadístico.

## Interfaz y despliegue

Para la creación de la interfaz de usuario (frontend) se optó por utilizar Dash, mientras que el backend se desarrolló principalmente en Python, haciendo uso de librerías como Numpy y diversas APIs de Google Cloud. El despliegue de la aplicación se realizó a través del servicio de virtualización de GCP. A continuación, se presenta un resumen de las principales herramientas y tecnologías implementadas:

- Python: Lenguaje principal para el desarrollo del backend.
- Numpy: Utilizado para cálculos y manipulaciones de datos.
- Nominatim: Biblioteca utilizada para transformar direcciones textuales en coordenadas geograficas.
- Dash: Herramienta escogida para el diseño de la interfaz de usuario.
- Google Cloud VM: Servicio utilizado para el despliegue de la aplicación.
- Cloud Translation API: Permite la traducción en tiempo real de ciertos elementos.
- Google Maps JavaScript API: Usada para integrar funcionalidades de mapas en la aplicación.
- SCP (Secure Copy Protocol) para transferir archivos entre la máquina local y la VM.


# Características de la Interfaz

La interfaz de nuestra aplicación ha sido diseñada pensando en la simplicidad y eficiencia para el usuario. Con un diseño amigable y una disposición intuitiva, garantizamos una experiencia de usuario fluida y agradable.

Características destacadas:

- Bilingüe: Nuestra interfaz es accesible y brinda soporte en dos idiomas principales: inglés y español. Esto nos permite alcanzar a una audiencia más amplia y garantizar que más usuarios puedan interactuar cómodamente con nuestra plataforma.

- Barra Lateral Deslizable: La barra lateral deslizable proporciona acceso directo a distintas secciones. Los usuarios pueden navegar fácilmente hacia los dashboards, acceder a nuestro repositorio en GitHub y contactarnos para cualquier consulta o comentario.

- Recomendaciones Personalizadas: En el corazón de nuestra interfaz se encuentra el sistema de recomendación. Aquí, los usuarios reciben sugerencias específicas basadas en sus preferencias y necesidades. Estas recomendaciones no solo son precisas sino también relevantes para garantizar la satisfacción del usuario.

- Integración con Google Maps: Para facilitar aún más la experiencia, hemos incorporado un iframe de Google Maps directamente en la interfaz. Esto permite a los usuarios obtener direcciones en tiempo real y saber cómo llegar a las ubicaciones recomendadas sin tener que abandonar la aplicación.

# Integración con el Modelo de Recomendación

La integración entre el frontend y el backend, específicamente con el modelo de recomendación, ha sido diseñada para ser fluida y eficiente, garantizando precisión y rapidez en las respuestas. A continuación, se detalla el proceso:

- Ingreso de Datos por el Usuario: La interfaz permite al usuario ingresar sus preferencias o requisitos para una recomendación. Esta entrada se realiza a través de campos de texto en el frontend donde pueden detallar lo que desean, así como proporcionar su dirección actual.

- Pre-procesamiento de Datos: Una vez recibido el input del usuario, el sistema inicia un proceso interno de transformación:

- Traducción: Si el input del usuario está en un idioma diferente al inglés, la aplicación utiliza la Cloud Translation API para traducir la entrada al inglés. Esta traducción garantiza que el sistema pueda entender y procesar correctamente la solicitud del usuario.

- Tokenización: Posterior a la traducción, el input se tokeniza en palabras clave. Este proceso permite al sistema identificar y clasificar las preferencias del usuario de manera efectiva, facilitando así la generación de recomendaciones precisas.

- Transformación de la Dirección: Paralelamente, la dirección proporcionada por el usuario se convierte en coordenadas geográficas. Para esto, se utiliza la bibilioteca "Nominatim" . Esta herramienta es esencial para transformar direcciones textuales en tuplas de coordenadas, facilitando así la integración con sistemas de mapeo y recomendación basados en ubicación.

- Consulta al Modelo de Recomendación: Con la entrada del usuario ya procesada y las coordenadas obtenidas, el sistema envia esta entrada al modelo de recomendación. Este modelo, entrenado con vastos datos, genera una lista de lugares o servicios que coinciden con las preferencias y la ubicación del usuario.

- Presentación de Resultados: Finalmente, las recomendaciones se presentan en la interfaz para que el usuario pueda visualizarlas, junto con opciones para ver cómo llegar a cada lugar recomendado gracias a la integración con Google Maps.

Esta integración entre la interfaz y el modelo de recomendación garantiza que los usuarios reciban sugerencias personalizadas y relevantes, todo en tiempo real y con la máxima precisión posible.

# Instrucciones de Instalación

Clona este repositorio en tu máquina local.
Navega al directorio del proyecto.
Instala las dependencias necesarias (proporciona un archivo requirements.txt si es posible).
Ejecuta el archivo principal para iniciar la aplicación.
(Adapta estos pasos según tu configuración específica)

# Contribuidores

- Interfaz, integracion con el modelo de recomendacion y deploy de la aplicacion - Matias da Silva  [👉 LinkedIn](https://www.linkedin.com/in/matiasdasilva92/)
- Modelo de recomendacion, normalizacion de datos para el modelo - Guillermo Gallo Garcia  [👉 LinkedIn](https://www.linkedin.com/in/guillermo-patricio-gallo-garcia-0a3bb3bb/)

# Licencia

Especifica la licencia bajo la cual estás distribuyendo tu software. Puede ser una licencia de código abierto o cualquier otra que elijas.


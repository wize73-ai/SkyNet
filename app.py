import os
import psycopg2  # PostgreSQL database adapter for Python
import redis  # Redis client for caching
from flask import Flask, render_template
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from dotenv import load_dotenv

# Load environment variables from .env file (if applicable)
load_dotenv()

# Flask app setup
server = Flask(__name__)

# Dash app setup with Flask server as the base
app = dash.Dash(__name__, server=server, url_base_pathname='/dash/')

# Connect to Redis for caching frequently accessed data
cache = redis.StrictRedis(host='localhost', port=6379, db=0)

# PostgreSQL database connection function
def get_db_connection():
    """Establishes and returns a connection to the PostgreSQL database."""
    conn = psycopg2.connect(
        dbname='skyviewdb',
        user='skyviewuser',
        password='your_password',  # Replace with your PostgreSQL password
        host='localhost'
    )
    return conn

# Dash Layout
app.layout = html.Div([
    html.H1("Sky View Rendering Application"),  # Main title
    dcc.Graph(id='sky-graph', config={'clickmode': 'event+select'}),  # 3D Graph
    dcc.Slider(
        id='wavelength-slider',
        min=0,
        max=6,
        step=1,
        marks={i: f'Layer {i}' for i in range(7)},  # Slider for electromagnetic spectrum layers
        value=0
    ),
    dcc.Slider(
        id='redshift-slider',
        min=0,
        max=10,
        step=0.1,
        marks={i: f'Redshift {i}' for i in range(11)},  # Slider for adjusting redshift
        value=0
    ),
    html.Div(id='hover-output', style={'marginTop': 20}),  # Placeholder for hover info
    html.Div(id='click-output', style={'marginTop': 20})  # Placeholder for click info
])

# Function to retrieve cached data from Redis
def get_cached_data(object_id):
    """Retrieve cached data from Redis."""
    cached_data = cache.get(object_id)
    return cached_data.decode('utf-8') if cached_data else None

# Function to cache data in Redis
def cache_data(object_id, data):
    """Cache data in Redis with a 1-hour expiration time."""
    cache.set(object_id, data, ex=3600)  # Cache the data for 1 hour

# Callback to update the 3D sky graph based on user inputs
@app.callback(
    Output('sky-graph', 'figure'),
    [Input('wavelength-slider', 'value'),
     Input('redshift-slider', 'value')]
)
def update_graph(wavelength, redshift):
    """
    Updates the 3D scatter plot based on the current slider values for 
    electromagnetic wavelength and redshift.
    """
    # Connect to PostgreSQL database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query celestial objects from PostgreSQL
    cursor.execute('''
    SELECT id, name, ra, dec, distance, em_data_path FROM celestial_objects
    WHERE redshift <= %s
    ''', (redshift,))

    # Fetch all results
    data = cursor.fetchall()
    conn.close()

    # If there is no data, return empty arrays
    if data:
        ids, names, ra_values, dec_values, distances, em_paths = zip(*data)
    else:
        ids, names, ra_values, dec_values, distances, em_paths = [], [], [], [], [], []

    # Prepare the 3D scatter plot with Plotly
    trace = go.Scatter3d(
        x=ra_values,  # Right Ascension (RA)
        y=dec_values,  # Declination (Dec)
        z=distances,  # Distance from Earth
        mode='markers',
        marker=dict(
            size=5,
            color='rgb(255, 255, 255)'  # Default white color
        ),
        text=names,  # Display names on hover
        hoverinfo='text',
        customdata=em_paths  # Store EM data paths for click/hover events
    )

    layout = go.Layout(
        margin=dict(l=0, r=0, b=0, t=0),
        scene=dict(
            xaxis_title='Right Ascension (RA)',
            yaxis_title='Declination (Dec)',
            zaxis_title='Distance (light-years)'
        )
    )

    return {'data': [trace], 'layout': layout}

# Callback to handle hover events on the 3D graph
@app.callback(
    Output('hover-output', 'children'),
    [Input('sky-graph', 'hoverData')]
)
def display_hover_data(hoverData):
    """Displays information when the user hovers over a celestial object."""
    if hoverData is None:
        return "Hover over a celestial object to see its image."

    # Extract the electromagnetic data path of the hovered object
    em_data_path = hoverData['points'][0]['customdata']
    # Construct the image URL (Placeholder URL for demo purposes)
    image_url = f"https://nasa.gov/{em_data_path}"  # Replace with actual image source

    return html.Img(src=image_url, style={'width': '200px', 'height': '200px'})  # Display the image

# Callback to handle click events on the 3D graph
@app.callback(
    Output('click-output', 'children'),
    [Input('sky-graph', 'clickData')]
)
def display_click_data(clickData):
    """Displays information when a celestial object is clicked."""
    if clickData is None:
        return "Click on a celestial object to see more information."

    # Extract the ID and image path of the clicked object
    em_data_path = clickData['points'][0]['customdata']
    # Construct the image URL (Placeholder URL for demo purposes)
    image_url = f"https://nasa.gov/{em_data_path}"  # Replace with actual image source

    return html.Div([
        html.Img(src=image_url, style={'width': '300px', 'height': '300px'}),
        html.P(f"Learn more about this object at: {image_url}")
    ])

# Route for the main Flask HTML template
@server.route('/')
def index():
    """Main route for the Flask application."""
    return render_template('index.html')

# Run the Flask/Dash server
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=5000, debug=True)

import os
import sqlite3
from flask import Flask, render_template
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Flask setup
server = Flask(__name__)

# Dash setup
app = dash.Dash(__name__, server=server, url_base_pathname='/dash/')

# Dash layout
app.layout = html.Div([
    html.H1("Sky View Rendering Application"),
    dcc.Graph(id='sky-graph', config={'clickmode': 'event+select'}),
    dcc.Slider(
        id='wavelength-slider',
        min=0,
        max=6,
        step=1,
        marks={i: f'Layer {i}' for i in range(7)},
        value=0
    ),
    dcc.Slider(
        id='redshift-slider',
        min=0,
        max=10,
        step=0.1,
        marks={i: f'Redshift {i}' for i in range(11)},
        value=0
    ),
    html.Div(id='click-output', style={'marginTop': 20})
])

# Callback to update the sky graph based on the current sliders
@app.callback(
    Output('sky-graph', 'figure'),
    [Input('wavelength-slider', 'value'),
     Input('redshift-slider', 'value')]
)
def update_graph(wavelength, redshift):
    # Connect to the SQLite database
    conn = sqlite3.connect('sky_data.db')
    cursor = conn.cursor()

    # Query celestial objects from the database
    cursor.execute('''
    SELECT id, name, ra, dec, distance FROM celestial_objects
    WHERE redshift <= ?
    ''', (redshift,))

    # Fetch data
    data = cursor.fetchall()
    conn.close()

    # Extract data for visualization
    if data:
        ids, names, ra_values, dec_values, distances = zip(*data)
    else:
        ids, names, ra_values, dec_values, distances = [], [], [], [], []

    # Prepare the 3D plot
    trace = go.Scatter3d(
        x=ra_values,
        y=dec_values,
        z=distances,
        mode='markers',
        marker=dict(
            size=5,
            color='rgb(255, 255, 255)'  # Adjust color based on wavelength slider if needed
        ),
        text=names,
        hoverinfo='text',
        customdata=ids  # Use custom data to store object IDs for click events
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

# Callback to handle clicks on celestial objects
@app.callback(
    Output('click-output', 'children'),
    [Input('sky-graph', 'clickData')]
)
def display_click_data(clickData):
    if clickData is None:
        return "Click on a celestial object to see more information."

    # Extract ID of the clicked celestial object
    clicked_id = clickData['points'][0]['customdata']

    # Connect to the SQLite database to get the object details
    conn = sqlite3.connect('sky_data.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT name, em_data_path FROM celestial_objects WHERE id = ?
    ''', (clicked_id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        name, em_data_path = result
        # Construct the URL to NASA or SDSS page (placeholder logic)
        link = f"https://example.com/{em_data_path}"  # Replace with actual logic for generating the link
        return html.A(f"Learn more about {name}", href=link, target="_blank")
    
    return "No information available for the selected object."

@server.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run_server(debug=True)

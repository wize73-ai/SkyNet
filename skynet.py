import plotly.express as px
from astroquery.sdss import SDSS
from astropy import coordinates as coords
import astropy.units as u
from ipywidgets import interact, Dropdown, FloatSlider
import pandas as pd

# Function to query SDSS based on redshift and magnitude range
def query_objects(ra, dec, radius, mag_min, mag_max, redshift_min, redshift_max):
    pos = coords.SkyCoord(ra, dec, unit=(u.deg, u.deg), frame='icrs')
    query = f"SELECT ra, dec, z, mag_g, mag_r FROM specObj WHERE ra BETWEEN {ra - radius} AND {ra + radius} \
              AND dec BETWEEN {dec - radius} AND {dec + radius} \
              AND z BETWEEN {redshift_min} AND {redshift_max} \
              AND mag_g BETWEEN {mag_min} AND {mag_max}"
    results = SDSS.query_sql(query)
    return results.to_pandas() if results is not None else pd.DataFrame()

# Function to plot objects using Plotly
def plot_objects(radius, mag_range, redshift_range):
    ra, dec = 180, 0  # North hemisphere (example center)
    mag_min, mag_max = mag_range
    redshift_min, redshift_max = redshift_range
    
    # Query SDSS for objects within range
    data = query_objects(ra, dec, radius, mag_min, mag_max, redshift_min, redshift_max)
    
    if not data.empty:
        # Use Plotly for an interactive scatter plot
        fig = px.scatter_3d(data, x='ra', y='dec', z='z', color='z', 
                            title=f'Objects: radius={radius} deg, mag={mag_min}-{mag_max}, redshift={redshift_min}-{redshift_max}')
        fig.update_traces(marker=dict(size=5), selector=dict(mode='markers'))
        fig.update_layout(scene=dict(
            xaxis_title='RA',
            yaxis_title='DEC',
            zaxis_title='Redshift (z)'
        ))
        fig.show()
    else:
        print("No objects found for the given parameters.")

# Interactive sliders and controls
radius_slider = FloatSlider(value=0.5, min=0.01, max=2.0, step=0.01, description='Radius (deg)')
redshift_range_slider = FloatSlider(value=0.1, min=0.0, max=5.0, step=0.01, description='Redshift Range')

# Set magnitude categories for different types of visibility
visibility_categories = {
    'Naked Eye': (0, 6),
    'Telescope': (6, 20),
    'Radio Telescope': (20, 40),
    'Beyond Visible': (20, 40)  # Example, may vary based on specific object types
}

visibility_dropdown = Dropdown(options=visibility_categories.keys(), description='Visibility')

# Function to map visibility to magnitude ranges
def update_visibility(visibility_type, radius, redshift_min, redshift_max):
    mag_min, mag_max = visibility_categories[visibility_type]
    plot_objects(radius, (mag_min, mag_max), (redshift_min, redshift_max))

# Combine into interactive interface
interact(update_visibility, 
         visibility_type=visibility_dropdown, 
         radius=radius_slider, 
         redshift_min=redshift_range_slider, 
         redshift_max=redshift_range_slider)

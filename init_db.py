import psycopg2
from datetime import datetime

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname='skyviewdb',
    user='skyviewuser',
    password='private',  # Replace with your PostgreSQL password
    host='localhost'
)
cursor = conn.cursor()

# Create table for celestial objects
cursor.execute('''
CREATE TABLE IF NOT EXISTS celestial_objects (
    id SERIAL PRIMARY KEY,
    name TEXT,
    ra FLOAT,            -- Right Ascension
    dec FLOAT,           -- Declination
    distance FLOAT,      -- Distance from Earth in light-years
    em_data_path TEXT,   -- Path to electromagnetic data or image link
    redshift FLOAT,      -- Redshift value
    object_type TEXT,    -- Type of celestial object (e.g., star, galaxy, nebula)
    cached_image TEXT,   -- Local path or URL to cached image
    last_fetched TIMESTAMP  -- Last time the image or data was fetched
)
''')

# Insert some sample celestial objects
sample_data = [
    ('Star A', 100.5, 30.7, 500.0, 'nasa_link/star_a', 0.01, 'star', None, None),
    ('Galaxy B', 102.1, 32.3, 1500.0, 'nasa_link/galaxy_b', 0.15, 'galaxy', None, None),
    ('Nebula C', 104.8, 28.5, 800.0, 'nasa_link/nebula_c', 0.05, 'nebula', None, None)
]

# Insert data into the table
cursor.executemany('''
INSERT INTO celestial_objects (name, ra, dec, distance, em_data_path, redshift, object_type, cached_image, last_fetched)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
''', sample_data)

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()

print("Database initialized and sample data inserted.")

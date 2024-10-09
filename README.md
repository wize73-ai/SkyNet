
Sky View Rendering Application
Overview
Hey there! This is my Sky View Rendering Application. It allows us to visualize the sky above any location on Earth in real-time using Python, Flask, Dash, and Plotly. I’ve also integrated PostgreSQL for the database and Redis for caching to improve performance. We can adjust the electromagnetic wavelength and redshift to simulate how celestial objects appear from different perspectives.

Here’s what I’ve set up and how it all works!

Features
3D Sky Visualization: You can see the sky rendered as a 3D scatter plot, showing stars, galaxies, nebulae, and more.
Location Selection: You can drop a pin on a map to select a location and see the sky from that position.
Adjustable Wavelength and Redshift: Sliders let you adjust the electromagnetic wavelength and redshift to explore the sky in different ways.
Caching with Redis: Celestial data and images are cached with Redis for faster performance.
PostgreSQL Database: This handles all the data about celestial objects (coordinates, types, images, etc.).
Interactive Click/Hover: When you hover over or click a celestial object, you get additional information, including images from NASA.
Requirements
Here’s what I’m using:

Raspberry Pi 4B running Raspbian Desktop
PostgreSQL for database management
Redis for caching
Flask, Dash, and Plotly for the front-end and back-end interaction
A 1TB HDD mounted on the Raspberry Pi for storage
Install Dependencies
Make sure you have these installed:

bash
Copy code
pip install flask dash plotly psycopg2 redis python-dotenv
Project Structure
Here’s how I’ve organized the project:

bash
Copy code
sky_view_app_python/
├── app.py               # Main application logic
├── init_db.py           # Database initialization script
├── index.html           # Main HTML file for the interface
├── styles.css           # CSS for styling
└── requirements.txt     # Python dependencies (optional)
Breakdown:
app.py: This is where all the Flask and Dash logic happens. It connects to PostgreSQL, handles Redis caching, and serves the interactive UI.
init_db.py: This script initializes the PostgreSQL database and adds some sample data.
index.html: The main HTML file, including the map and the containers for the 3D plot.
styles.css: Defines the layout and styling for the application.
Logic Ladder Diagram
Here’s how the application flows logically from start to end, including user interactions and the back-end processing.

Logic Ladder Diagram
plaintext
Copy code
Start
  |
  V
User opens browser and navigates to http://<raspberry-pi-ip>:5000
  |
  V
Flask server receives request -> Serves index.html + styles.css to browser
  |
  V
Browser loads the web page
  |
  +---> Initialize Leaflet map for location selection (JavaScript in index.html)
  |        |
  |        +---> User clicks on map -> Latitude and Longitude captured
  |
  V
Dash app and Python backend loads -> Dash serves layout
  |
  V
Dash renders 3D scatter plot using Plotly (initial data)
  |
  V
User interacts with sliders (Wavelength and Redshift)
  |
  +---> Dash callback triggered
  |        |
  |        +---> Connect to PostgreSQL database
  |        |        |
  |        |        +---> Query celestial objects from PostgreSQL based on redshift
  |        |
  |        +---> Check Redis cache for cached data (optional)
  |        |        |
  |        |        +---> If cached data exists -> Use cached data
  |        |        +---> Else -> Query PostgreSQL
  |        |
  |        +---> Celestial object data fetched -> Update Plotly scatter plot
  |
  V
User hovers or clicks on celestial objects
  |
  +---> Dash callback triggered for hover/click events
  |        |
  |        +---> Fetch additional object data (e.g., image URLs) from PostgreSQL or Redis
  |        +---> Display object image and details in HTML
  |
  V
Continue user interactions (map, sliders, hover/click) -> Dynamic updates
  |
  V
End
Explanation
The app is loaded in the browser after Flask serves the HTML, CSS, and initial Dash app.
The Leaflet map allows users to select locations, and the Dash app updates the 3D scatter plot based on the selected location, wavelength, and redshift.
Redis is used to cache frequently accessed celestial data and images for faster performance.
When users hover or click on celestial objects, detailed info is fetched from PostgreSQL or Redis and displayed on the screen.
How to Run
Here’s how to get the application up and running:

Mount the HDD: Make sure your 1TB HDD is mounted at /mnt/external_hdd.
Initialize the PostgreSQL Database:
Run the init_db.py script to create the tables and insert sample data:
bash
Copy code
python3 init_db.py
Run the Application:
Start the Flask server:
bash
Copy code
python3 app.py
The app will be accessible at http://<raspberry-pi-ip>:5000.
Future Enhancements
Here’s what I’m thinking of adding:

Real-time sky updates: Integrating real-time data feeds to keep the sky rendering up to date.
Augmented Reality (AR): Implementing AR to allow users to view the sky through their phone’s camera.
Educational Overlays: Displaying educational info about constellations and celestial objects directly on the sky map.
User Accounts: Adding user accounts to save favorite sky views or celestial objects.
Feel free to jump in, explore the sky, and tweak anything to suit your needs. Let me know if you have questions!














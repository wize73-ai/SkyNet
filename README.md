# SkyNet
Sky Visualization


https://github.com/wize73-ai/SkyNet.git

Query Data Based on Visibility: We will categorize objects by their brightness and type (stars, galaxies, radio sources, etc.).

Naked Eye: Objects with apparent magnitude 
𝑚
<
6
m<6.
Telescope: Fainter objects, 
6
<
𝑚
<
20
6<m<20.
Radio Telescope: For frequencies in the radio band (21cm HI line).
Beyond Visible: Ultraviolet, X-ray sources.
Redshift Control: We'll apply filters to only display objects within a specific redshift range, adjusting the view interactively.

Interactivity: Two sliders will be created:

One for object visibility type (radio, optical, etc.).
Another to adjust the redshift range, dynamically filtering objects based on the observed wavelength shift.

Dependencies:

astroquery for fetching data.
ipywidgets for interactive sliders. <- this depends on colab or jupyter  lets fix>
matplotlib for visualization

pip install astroquery ipywidgets matplotlib



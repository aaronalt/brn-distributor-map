import pandas as pd
import folium 
from folium.plugins import MarkerCluster

sheet_url = 'https://docs.google.com/spreadsheets/d/1BEXCT_VLp8FgnMxOHtblB7M7qArqthqqEYsSsL4mhZo/export?format=csv&id=1BEXCT_VLp8FgnMxOHtblB7M7qArqthqqEYsSsL4mhZo'

df = pd.read_csv(sheet_url, delimiter=",", sep='\t', header=0, encoding='latin-1')

csv = [tuple(x) for x in df.values]

clean_data = [data for data in csv if not pd.isnull(data[7]) if not pd.isnull(data[4])]

m = folium.Map(location=[38.4237, 27.1428], zoom_start = 5, min_zoom = 3, tiles = "CartoDB positron", world_copy_jump = True)

locations = []
for location in clean_data:
    coords = [location[0], location[1]]
    noapostrophe = location[4].replace("'","")
    locations.append({'company' : location[1], 'country' : location[2], 'products' : location[3], 'text': f"{location[3]}<br> {location[2]}<br> <a href={location[9]}>Website</a>", 'coordinates' : coords})

cluster = MarkerCluster().add_to(m)

for x in locations:
    folium.Marker(location = (x['coordinates']), popup = x['text'], icon=folium.Icon(color='red')).add_to(cluster)

m.save('index.html')


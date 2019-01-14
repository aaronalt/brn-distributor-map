import pandas as pd
import folium 
from folium.plugins import MarkerCluster
import html

#docs.google.com/spreadsheets/d/----->ID/export?format=csv&id=ID(replace 'ID' to export as csv)
sheet_url = 'https://docs.google.com/spreadsheets/d/1BEXCT_VLp8FgnMxOHtblB7M7qArqthqqEYsSsL4mhZo/export?format=csv&id=1BEXCT_VLp8FgnMxOHtblB7M7qArqthqqEYsSsL4mhZo' 

#create a blank map, add feature groups for each layer
m = folium.Map(location=[48.209619, 16.370439], zoom_start = 4, min_zoom = 2, tiles = "CartoDB positron", world_copy_jump = True, max_zoom = 15) 
fg_potential = folium.FeatureGroup(name="Potential Distributors")
fg_current = folium.FeatureGroup(name="Current Customers")
#read csv and create dataframe
df = pd.read_csv(sheet_url, delimiter=",", header=0, encoding='latin-1', engine='python') 
html.escape(df)
#turn dataframe from dict into a tuple
csv = [list(x) for x in df.values]



#organize data into array
    #location[14].strip(" ").split(";:,$./")
    #notes = ' '.join(map(str, location[14]))

locations = []
for location in csv:
    coords = [location[0], location[1]]
    
    try:
        locations.append({'company' : location[2], 'country' : location[3], 'products' : location[3], 'potential' : location[4], 'method' : location[13], 'hover': f"{location[3]}<br>{location[2]}", 'click': f"<a href={location[9]}>Website</a><br>{location[13]}<br>{location[14]}", 'coordinates' : coords})
    except SyntaxError:
        print("syntax error")
    

#add marker clusters for grouping markers 
current_cluster = MarkerCluster(options={'spiderfyOnMaxZoom' : True, 'disableClusteringAtZoom' : 8, 'zoomToBoundsOnClick' : False, 'spiderfyDistanceMultiplier' : 1.5})
potential_cluster = MarkerCluster(options={'spiderfyOnMaxZoom' : True, 'disableClusteringAtZoom' : 8, 'zoomToBoundsOnClick' : False, 'spiderfyDistanceMultiplier' : 1.5}) 
#iterate through the array, add marker for every distributor (row)
for x in locations:
    try:
        if x['potential'] == "Current Customer":
            folium.Marker(location = (x['coordinates']), popup = x['click'], tooltip = x['hover'], icon=folium.Icon(color='green')).add_to(current_cluster)
        else:
            folium.Marker(location = (x['coordinates']), popup = x['click'], tooltip = x['hover'], icon=folium.Icon(color='red')).add_to(potential_cluster)
    except SyntaxError:
        print("syntax error")


#add feature groups to marker clusters, layer control for selecting layers
fg_potential.add_child(potential_cluster)
fg_current.add_child(current_cluster)
m.add_child(fg_potential)
m.add_child(fg_current)
folium.LayerControl(position='topleft').add_to(m) 

#save to html file
m.save('index.html')

 
import pandas as pd
import folium 
from folium.plugins import MarkerCluster
import html
from branca.element import Template, MacroElement

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

#legend
template = """
{% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>BRN Distributor Map</title>
  <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
  
  <script>
  $( function() {
    $( "#maplegend" ).draggable({
                    start: function (event, ui) {
                        $(this).css({
                            right: "auto",
                            top: "auto",
                            bottom: "auto"
                        });
                    }
                });
});

  </script>
</head>
<body>

 
<div id='maplegend' class='maplegend' 
    style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
     border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>
     
<div class='legend-title'>Distributors</div>
<div class='legend-scale'>
  <ul class='legend-labels'>
    <li><span style='background:red;opacity:0.7;'></span>Potential</li>
    <li><span style='background:green;opacity:0.7;'></span>Current</li>

  </ul>
</div>
</div>
 
</body>
</html>

<style type='text/css'>
  .maplegend .legend-title {
    text-align: left;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 90%;
    }
  .maplegend .legend-scale ul {
    margin: 0;
    margin-bottom: 5px;
    padding: 0;
    float: left;
    list-style: none;
    }
  .maplegend .legend-scale ul li {
    font-size: 80%;
    list-style: none;
    margin-left: 0;
    line-height: 18px;
    margin-bottom: 2px;
    }
  .maplegend ul.legend-labels li span {
    display: block;
    float: left;
    height: 16px;
    width: 30px;
    margin-right: 5px;
    margin-left: 0;
    border: 1px solid #999;
    }
  .maplegend .legend-source {
    font-size: 80%;
    color: #777;
    clear: both;
    }
  .maplegend a {
    color: #777;
    }
</style>
{% endmacro %}"""

macro = MacroElement()
macro._template = Template(template)

m.get_root().add_child(macro)

#save to html file
m.save('index.html')

 
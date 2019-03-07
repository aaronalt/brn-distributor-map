#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 15:33:11 2019

@author: aaronalt
"""

import pandas as pd
import folium 
from folium.plugins import MarkerCluster
import numpy as np
from branca.element import Template, MacroElement

sheet_url = 'https://docs.google.com/spreadsheets/d/1qGnU-OE4mcVf-Gnc1iINpx2pqH5komEWk1_9shmX6nY/export?format=csv&id=1qGnU-OE4mcVf-Gnc1iINpx2pqH5komEWk1_9shmX6nY'

#create a blank map, add feature groups for each layer
m = folium.Map(location=[48.209619, 16.370439], zoom_start = 4, min_zoom = 2, tiles = "CartoDB positron", world_copy_jump = True, max_zoom = 15) 

fg_potential = folium.FeatureGroup(name="Potential Distributors")
fg_current   = folium.FeatureGroup(name="Current Customers")

#read csv and create dataframe
df = pd.read_csv(sheet_url, engine='python',header=0, delimiter=",", error_bad_lines=False, na_filter=False) 
to_drop = ['Company Size','SalesRep','BRN potential(y/n)']
df.drop(to_drop,inplace=True,axis=1)
df=df.fillna(' ')
df['Country']=df['Country'].str.replace(',','')
df['Products']=df['Products'].str.replace(',','')
df['Address']=df['Address'].str.replace(',',' ')
df['Web Site']=df['Web Site'].str.rstrip('/')
df['Notes']=df['Notes'].str.replace(',',' ')
df['lat']=df['lat'].apply(pd.to_numeric)
df['lon']=df['lon'].apply(pd.to_numeric)
df=df.dropna(subset=['lon'])
df=df.dropna(subset=['lat'])

df_list = [list(x) for x in df.values]
pot = []
for cell in df_list:
    try:
        coords = [cell[14],cell[15]]
        pot.append({
                'company':cell[0],
                'country':cell[1],
                'status':cell[2],
                'type':cell[3],
                'products':cell[4],
                'address':cell[5],
                'url':cell[6],
                'email':cell[7],
                'phone':cell[8],
                'source':cell[9],
                'contacted':cell[10],
                'contactDate':cell[11],
                'contactResults':cell[12],
                'notes':cell[13],
                'lat':cell[14],
                'lon':cell[15],
                'coords':coords,
                'hover':f"{cell[0]} ({cell[1]})<br>{cell[8]} {cell[7]}<br>{cell[4]}",
                'click':f"{cell[0]} ({cell[1]})<br><a href={cell[6]}>Website</a> | Contacted: {cell[10]} {cell[11]}<br>{cell[12]}<br>{cell[13]}"
                })
    except Exception as e:
        print(e)

current_cluster = MarkerCluster(options={
        'spiderfyOnMaxZoom' : True, 
        'disableClusteringAtZoom' : 8, 
        'zoomToBoundsOnClick' : False, 
        'spiderfyDistanceMultiplier' : 1.5
        })
potential_cluster = MarkerCluster(options={
        'spiderfyOnMaxZoom' : True, 
        'disableClusteringAtZoom' : 8, 
        'zoomToBoundsOnClick' : False, 
        'spiderfyDistanceMultiplier' : 1.5
        }) 

for x in pot:
    try:
        if x['status'] == "Current Customer":
            folium.Marker(location = (x['coords']), popup = x['click'], tooltip = x['hover'], icon=folium.Icon(color='green')).add_to(current_cluster)
        else:
            folium.Marker(location = (x['coords']), popup = x['click'], tooltip = x['hover'], icon=folium.Icon(color='red')).add_to(potential_cluster)
    except Exception as e:
        print(e)

fg_potential.add_child(potential_cluster)
fg_current.add_child(current_cluster)
m.add_child(fg_potential)
m.add_child(fg_current)
folium.LayerControl(position='topleft').add_to(m) 

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
        

        


        
    
    
    
    
    
    
    
    
    
    

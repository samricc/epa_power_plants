#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 22:05:57 2022

@author: samanthariccio
"""

import pandas as pd
import geopandas as gpd


#%%
coal_data = pd.read_csv("high_emmissions_coal_plants.csv")
coal_data["STATEFP"] = coal_data["FIPS State Code"]
coal_data = coal_data.drop(columns="FIPS State Code")
coal_data["STATEFP"] = coal_data["STATEFP"].astype(str)
mt_coal_data = coal_data.query("STATEFP == '30'")

x = mt_coal_data["Longitude"]
y = mt_coal_data["Latitude"]
geo = gpd.points_from_xy(x, y)
pt_layer = gpd.GeoDataFrame(geometry=geo, crs=4326)
pt_layer = pt_layer.to_crs( 32612 )

mt_coal_data = mt_coal_data.to_csv("mt_plant_data.csv")
pt_layer.to_file("mt_high_emissions.gpkg",layer="plant", index=False)


#%%

radius = [3, 10, 15, 20, 30, 40]
ring_layer = gpd.GeoDataFrame()
ring_layer["radius"] = radius
geo_list = []
last_buf = None
for r in radius:
    this_buf = pt_layer.buffer(r*1609)
    if len(geo_list) == 0:
        geo_list.append(this_buf[0])
    else:
        change = this_buf.difference(last_buf)
        geo_list.append(change[0])
    last_buf = this_buf
ring_layer["geometry"] = geo_list
ring_layer = ring_layer.set_crs(pt_layer.crs)
ring_layer.to_file("mt_high_emissions.gpkg", layer="rings", index=False)

ring_layer.to_csv("ring_data.csv",index=False)


#%%



#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 14:14:41 2022

@author: samanthariccio
"""

#import necessary modules and read in csv from previous script and Census
#shape file

import pandas as pd
import geopandas as gpd

mt_poc = pd.read_csv("3. MT Demographics/mt_poc.csv", dtype={"GEOID":str,"STATEFP":str})
census_data = gpd.read_file("cb_2021_30_bg_500k.zip",dtype={"GEOID":str})
#%%

#join the census data with the shape file for the state of Montana and calculate
#the percent people of color and average percent people of color. Write the file 
#to a GIS file with bg as the layer.                          

census_data = census_data.set_index("GEOID")
mt_poc = mt_poc.set_index("GEOID")
mt_poc = mt_poc.drop(columns = "STATEFP")

merged = census_data.join(mt_poc, how = "left")

merged["pct_pop"] = 100*(merged["pop_poc"]/merged["pop_total"])

merged["avg_pct_pop"] = merged["pct_pop"].sum()/900

merged.to_file("5. Rings & GIS/mt_high_emissions.gpkg", layer = "bg")

#%%

#read the GIS file that contains the rings and the demographic file of Montana. 
#merge the files in order to calculate the share of demographics within the rings.

rings = gpd.read_file("5. Rings & GIS/mt_high_emissions.gpkg", layer="rings")
pop = pd.read_csv("3. MT Demographics/mt_poc.csv",dtype={"GEOID":str})
pop = pop.set_index("GEOID")

bgs = gpd.read_file("cb_2021_30_bg_500k.zip")
keep_cols = ['GEOID', 'COUNTYFP', 'geometry']
bgs = bgs[keep_cols]
bgs = bgs.to_crs(rings.crs)
bgs['bg_area'] = bgs.area

bgs = bgs.merge(pop, on='GEOID', validate='1:1', indicator=True)
bgs = bgs.drop(columns="_merge")

slices = bgs.overlay(rings, how='union', keep_geom_type=True)
slices = slices.dropna(subset='radius')
slices["radius"] = slices["radius"].fillna(9999)
slices = slices.set_index(['GEOID','radius'])
slices["s_area"] = slices.area
area_share = slices["s_area"]/slices["bg_area"]

realloc = pd.DataFrame()
for v in pop.columns:
    realloc[v] = slices[v].mul(area_share, axis='index')
ring_info = realloc.groupby("radius").sum()

#%%

#calculate the share of different demographics within the rings and write
#to a csv file.

ring_info["pct_aian"] = 100*(ring_info["pop_aian"]/ring_info["pop_total"])
ring_info["pct_black"] = 100*(ring_info["pop_black"]/ring_info["pop_total"])
ring_info["pct_asian"] = 100*(ring_info["pop_asian"]/ring_info["pop_total"])
ring_info["pct_pacific"] = 100*(ring_info["pop_pacific"]/ring_info["pop_total"])
ring_info["pct_other"] = 100*(ring_info["pop_other"]/ring_info["pop_total"])
ring_info["pct_2"] = 100*(ring_info["pop_2"]/ring_info["pop_total"])
ring_info["pct_poc"] = 100*(ring_info["pop_poc"]/ring_info["pop_total"])

ring_info.to_csv("5. Rings & GIS/ring_info.csv",index=True)

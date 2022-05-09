#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 08:36:21 2022

@author: samanthariccio
"""
#import necessary modules
import pandas as pd
import requests
import numpy as np


#%% 

#identify the list of variables to pull from the 2021 census and then use
#the census api to pull in the columns and values. Set GEOID to the state,
#county, tract, and block group so it can be mapped later.

variables = {'B02001_001E':'pop_total', 
             'B02001_002E':'pop_white',
             'B02001_003E':'pop_black',
             'B02001_004E':'pop_aian',
             'B02001_005E':'pop_asian',
             'B02001_006E':'pop_pacific',
             'B02001_007E':'pop_other',
             'B02001_008E':'pop_2'}

var_list = variables.keys()

var_string = ",".join(var_list)

api = "https://api.census.gov/data/2020/acs/acs5"

get_clause = var_string
for_clause = 'block group:*'
in_clause = 'state:30 county:*'
key_value = "308a33cea90553fe218295a5c3588bc709b14031"
payload = {'get':get_clause,'for':for_clause,'in':in_clause,'key':key_value}
response = requests.get(api,payload)
row_list = response.json()
colnames = row_list[0]
datarows = row_list[1:]
mt_pop = pd.DataFrame(columns=colnames,data=datarows)
mt_pop = mt_pop.replace("-666666666",np.nan)
mt_pop = mt_pop.rename(columns=variables)
mt_pop["GEOID"] = mt_pop["state"]+ mt_pop["county"] + mt_pop["tract"] + mt_pop["block group"]
mt_pop = mt_pop.set_index("GEOID")

#%%

#calculate the share of non-white/people of color within Montana to clean
#up and to export to csv.

mt_pop["pop_total"] = mt_pop["pop_total"].astype(int)
mt_pop["pop_white"] = mt_pop["pop_white"].astype(int)
mt_pop["pop_poc"] = mt_pop["pop_total"] - mt_pop["pop_white"].astype(int)

mt_pop["STATEFP"] = mt_pop["state"]
keep_cols = ["pop_total","pop_white","pop_poc","STATEFP","county","pop_aian",
             "pop_black","pop_asian","pop_pacific","pop_other","pop_2"]
mt_pop = mt_pop[keep_cols]


mt_pop.to_csv("3. MT Demographics/mt_poc.csv",index=True)


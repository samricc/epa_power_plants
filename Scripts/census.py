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


#%% pull in api to identify national population and how they identify

variables = {'B02001_001E':'pop_total', 
             'B02001_002E':'pop_white'}

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
#mt_pop = mt_pop.drop(columns=["state","County"])

#%%

mt_pop["pop_total"] = mt_pop["pop_total"].astype(int)
mt_pop["pop_white"] = mt_pop["pop_white"].astype(int)
mt_pop["pop_poc"] = mt_pop["pop_total"] - mt_pop["pop_white"].astype(int)

mt_pop["STATEFP"] = mt_pop["state"]
keep_cols = ["pop_total","pop_white","pop_poc","STATEFP","county"]
mt_pop = mt_pop[keep_cols]


mt_pop.to_csv("mt_poc.csv",index=True)


# -*- coding: utf-8 -*-

#import necessary modules to read and clean up the csv file
#mark in the csv file which columns to keep by putting x in the column
#next to the name

import pandas as pd

varfile = pd.read_csv("columns_updated.csv")
varmap = varfile.dropna(subset=["new_column_name"])
varmap = varmap.set_index("old_column_name")

#%%

#read EPA file downloaded from the EJ screening site and update the columns
#based on the ones identified in the csv file of varmap.

epafile = "../Data/1.ALL_EPA_power_plants_and_communities.xlsx"
raw = pd.read_excel(epafile)
keep = [c for c in raw.columns if c in varmap.index]
print(len(varmap), len(keep))

clean = raw[keep].rename(varmap["new_column_name"])

#%%

#filter out all other types of energy plants besides coal.

cols = sorted(clean.columns)
fuel_col = "Plant primary coal/oil/gas/ other fossil fuel category"
print(clean[fuel_col].value_counts())

is_coal = clean[fuel_col]=="COAL"
print(is_coal.value_counts())
coal_plants = clean[is_coal]

coal_plants = coal_plants.rename(columns=varmap["new_column_name"])


#%%

#export to csv.

coal_plants.to_csv("1.Updated_CSV/coal_plants_communities.csv")



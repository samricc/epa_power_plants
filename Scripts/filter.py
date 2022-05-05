# -*- coding: utf-8 -*-

import pandas as pd

varfile = pd.read_csv("columns_updated.csv")
varmap = varfile.dropna(subset=["new_column_name"])
varmap = varmap.set_index("old_column_name")

#%%


epafile = "../Data/1.ALL_EPA_power_plants_and_communities.xlsx"
raw = pd.read_excel(epafile)
keep = [c for c in raw.columns if c in varmap.index]
print(len(varmap), len(keep))

clean = raw[keep].rename(varmap["new_column_name"])

#%%
cols = sorted(clean.columns)
fuel_col = "Plant primary coal/oil/gas/ other fossil fuel category"
print(clean[fuel_col].value_counts())

is_coal = clean[fuel_col]=="COAL"
print(is_coal.value_counts())
coal_plants = clean[is_coal]

coal_plants = coal_plants.rename(columns=varmap["new_column_name"])


#%%
coal_plants.to_csv("1. Updated CSV/coal_plants_communities.csv")



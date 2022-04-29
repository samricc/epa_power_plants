# -*- coding: utf-8 -*-

import pandas as pd

epafile = "../Data/1.ALL_EPA_power_plants_and_communities.xlsx"
raw = pd.read_excel(epafile)

col_names = pd.Series(raw.columns)
col_names.to_csv("columns.csv")

#%%








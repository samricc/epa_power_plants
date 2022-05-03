#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 11:06:17 2022

@author: samanthariccio
"""

import pandas as pd

plant_data = pd.read_csv("mt_plant_data.csv")
md_file = pd.read_excel("md_2011_by_fips.xlsx",dtype={'fips':int})
md_data = md_file.query("fips == 30087")
md_data = md_data.set_index("fips")

plant_data["fips"] = 30087
plant_data = plant_data.set_index("fips")

#%%

md_join = plant_data.join(md_data, how = "left")

md_join["total_md"] = md_join["PM25_2011"]* md_join["PM_Emissions"]/100

print(md_join["total_md"])

md_join.to_csv("md_mt_plant.csv",index=False)

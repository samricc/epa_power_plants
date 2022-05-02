#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  1 22:15:33 2022

@author: samanthariccio
"""
import pandas as pd
import matplotlib.pyplot as plt

coal_plants = pd.read_csv("coal_plants_communities.csv")

#%%


coal_plants["Net Generation"] = coal_plants["Net Generation"]/1e6 
coal_plants["Annual Net Gen"] = coal_plants["Annual Net Gen"]/1e6 

#%% PM EMISSIONS AND ANNUAL NET GEN SCATTER PLOT

fig1,ax1 = plt.subplots()

coal_plants.plot.scatter("Annual Net Gen", "PM_Emissions",ax=ax1)

ax1.set_ylabel = "Particulate Matter Emissions"
fig1.tight_layout()
fig1.savefig("Net_Gen_PM_Emissions.png")

#%%%

raw = pd.read_csv("coal_plants_communities.csv")
keep = raw.query("PM_Emissions >= 3000")
keep["Buffer Distance"] = 3
keep["Annual Net Gen"] = keep["Annual Net Gen"]/1e6 
(fig1, ax1) = plt.subplots()
keep.plot.scatter("Annual Net Gen", "Capacity Factor", ax=ax1)
keep.to_csv("high_emmissions_coal_plants.csv")



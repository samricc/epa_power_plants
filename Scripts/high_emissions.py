#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  1 22:15:33 2022

@author: samanthariccio
"""

#import necessary modules and read in csv file from previous script

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


coal_plants = pd.read_csv("1.Updated_CSVcoal_plants_communities.csv")

#%%

#divide columns by numbers in order to account for large values.

coal_plants["Net Generation"] = coal_plants["Net Generation"]/1e6 
coal_plants["Annual Net Gen"] = coal_plants["Annual Net Gen"]/1e6 

#%%

#create a scatter plot that looks at the regression of Annual Net Generation
#with PM Emissions and save to png.

fig1,ax1 = plt.subplots()

coal_plants.plot.scatter("Annual Net Gen", "PM_Emissions",ax=ax1)

ax1.set_ylabel = "Particulate Matter Emissions"
fig1.tight_layout()
fig1.savefig("4.Graphs/Net_Gen_PM_Emissions.png")


#%%

#create a box plot using bins to plot the relationship between coal plants
#and state percentile population of people of color and save as a png file.

coal_plants["bin"] = coal_plants["State pctile for POC Pop"].round(-1)

fig, ax1 = plt.subplots(dpi=300)
sns.boxenplot(data=coal_plants, x="bin", y="PM_Emissions",
              ax=ax1, showfliers=False)

ax1.set_xlabel("State Percentile of POC Population")
ax1.set_ylabel("PM Emissions")

fig.tight_layout()
fig.savefig("4.Graphs/State_pctile_poc_emissions.png")


#%%%

#read in file from previous script and filter out plants that are emitting
#more than 3000 PM emissions. Generate a scatter plot and save as png file. 

raw = pd.read_csv("1. Updated CSV/coal_plants_communities.csv")
keep = raw.query("PM_Emissions >= 3000")
keep["Buffer Distance"] = 3
keep["Annual Net Gen"] = keep["Annual Net Gen"]/1e6 
(fig1, ax1) = plt.subplots()
keep.plot.scatter("Annual Net Gen", "Capacity Factor", ax=ax1)
keep.to_csv("2.High_Emission_Plants/high_emmissions_coal_plants.csv")

#%%

#create a horizontal bar chart of the population of people of color within 
#the 3 mile radius of the plants to the state average people of color and save 
#as a png file.

keep = keep.set_index("Plant Name")

(fig1, ax1) = plt.subplots(dpi = 300)
bars = ["POC Pop","State avg for POC Pop"]
keep[bars].plot.barh(ax=ax1)

ax1.set_xlabel("% of POC Population")
fig1.tight_layout()
fig1.savefig("4.Graphs/POC_comparison.png")

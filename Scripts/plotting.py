#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:00:45 2022

@author: samanthariccio
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

coal_plants = pd.read_csv("coal_plants_communities.csv")
ring_data = pd.read_csv("ring_info.csv")


#%%

coal_plants["Net Generation"] = coal_plants["Net Generation"]/1e6 
coal_plants["Annual Net Gen"] = coal_plants["Annual Net Gen"]/1e6 

#%% POC BOX PLOT

coal_plants["bin"] = coal_plants["State pctile for POC Pop"].round(-1)

fig, ax1 = plt.subplots(dpi=300)
sns.boxenplot(data=coal_plants, x="bin", y="PM_Emissions",
              ax=ax1, showfliers=False)

ax1.set_xlabel("State Percentile of POC Population")
ax1.set_ylabel("PM Emissions")

fig.tight_layout()
fig.savefig("State_pctile_poc_emissions.png")


#%% LOW INCOME BOX PLOT

coal_plants["bin"] = coal_plants["State pctile for Low Inc Pop"].round(-1)

fig, ax1 = plt.subplots(dpi=300)
sns.boxenplot(data=coal_plants, x="bin", y="PM_Emissions",
              ax=ax1, showfliers=False)

ax1.set_xlabel("State Percentile of Low Income Population")
ax1.set_ylabel("Particulate Matter Emissions")

fig.tight_layout()
fig.savefig("State_pctile_low_inc_emissions.png")


#%% plotting poc population share in figure

ring_data["pop_poc"] = ring_data["pop_poc"].round()
ring_data["pct_poc"] = ring_data["pct_poc"].round()
ring_data["POC Share in Rings"] = ring_data["pct_poc"]

plt.rcParams['figure.dpi'] = 300

fg = sns.relplot(data=ring_data, x='pop_poc', y='radius', 
                 size="POC Share in Rings", 
                 sizes=(10,200),
                 facet_kws=
                 {'despine': False, 'subplot_kws': {'title': 'People of Color Inside Plants Radius'}})

fg.set_axis_labels('Population People of Color', 'Ring Radius (in miles)')

fg.tight_layout()
fg.savefig("POC_high_emissions.png")






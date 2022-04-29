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

raw = pd.read_csv("coal_plants_communities.csv")
keep = raw.query("PM_Emissions >= 3000")
keep["Buffer Distance"] = 3
keep["Annual Net Gen"] = keep["Annual Net Gen"]/1e6 
(fig1, ax1) = plt.subplots()
keep.plot.scatter("Annual Net Gen", "Capacity Factor", ax=ax1)
keep.to_csv("high_emmissions_coal_plants.csv")

#%%

coal_plants["Net Generation"] = coal_plants["Net Generation"]/1e6 
coal_plants["Annual Net Gen"] = coal_plants["Annual Net Gen"]/1e6 

#%% PM EMISSIONS AND ANNUAL NET GEN SCATTER PLOT

fig1,ax1 = plt.subplots()

coal_plants.plot.scatter("Annual Net Gen", "PM_Emissions",ax=ax1)

ax1.set_ylabel = "Particulate Matter Emissions"
fig1.tight_layout()
fig1.savefig("Net_Gen_PM_Emissions.png")

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

#%%
keep = keep.set_index("Plant Name")

(fig1, ax1) = plt.subplots(dpi = 300)
bars = ["POC Pop","State avg for POC Pop"]
keep[bars].plot.barh(ax=ax1)

ax1.set_xlabel("% of POC Population")
fig1.tight_layout()
fig1.savefig("POC_comparison.png")

#%% total population and population of low income near high polluting plants

tot_li_pop = keep["Low Income Pop"].sum()
tot_tot_pop = keep["Total Pop"].sum()
tot_coal_li_pop = 1e6*(tot_li_pop/tot_tot_pop)
keep["coal_li_ratio"] = 1e6*(keep["Low Income Pop"]/keep["Total Pop"])

#%% plotting low income population share in figure

plt.rcParams['figure.dpi'] = 300

fg = sns.relplot(data=keep, x='State', y='PM_Emissions', 
                 size='coal_li_ratio', 
                 sizes=(10,200),
                 facet_kws=
                 {'despine': False, 'subplot_kws': {'title': 'Ratio of Low Income Population Near High Emitting Plants'}})

fg.set_axis_labels('Share of Low Income Population', 'PM Emissions')

fg.tight_layout()
#fg.savefig("LI_high_emissions.png")


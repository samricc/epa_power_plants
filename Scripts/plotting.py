#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:00:45 2022

@author: samanthariccio
"""

#import necessary modules and read ring info csv from previous script.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ring_data = pd.read_csv("ring_info.csv")

#%%

#create a three variable figure that maps the people of color, the rings, and the
#share of people of color within the rings to export into png.

ring_data["pop_poc"] = ring_data["pop_poc"].round()
ring_data["pct_poc"] = ring_data["pct_poc"].round()
ring_data["POC Share in Rings"] = ring_data["pct_poc"]

plt.rcParams['figure.dpi'] = 300

fg = sns.relplot(data=ring_data, x='pop_poc', y='radius', 
                 size="POC Share in Rings", 
                 sizes=(10,200),
                 facet_kws=
                 {'despine': False, 'subplot_kws': {'title': 'People of Color Inside Plants Radius'}})


fg.tight_layout()
fg.savefig("POC_high_emissions.png")






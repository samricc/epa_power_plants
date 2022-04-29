#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 20:26:06 2022

@author: samanthariccio
"""

#import modules as necessary
import pandas as pd

#set the variable equal to the read csv file where it reads the information as
#a string
contrib = pd.read_csv("contrib_by_zip.zip",dtype=str)

contrib['amt'] = contrib['amt'].astype(float)

po = pd.read_csv("pocodes.csv")

po = po.drop(columns="name")

contrib = contrib.merge(po, left_on='STATE', right_on='PO', how='outer',
validate='m:1', indicator=True)

print(contrib['merge'].value_counts())
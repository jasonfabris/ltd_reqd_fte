# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import itertools

# set up variables

# num mths to simulate
mths = 1000

# number of covered lives
covered = 10000
# avg caseload, sub per 1000
caseload = 56  
sub_rate = 9.8
app_rate = 0.83
mean_dur = 9.6
block_size = np.zeros(shape=mths, dtype="int")

#how many claims will show up in each month?
##change to submission * approval rate, with variance

in_mu = np.floor(((covered/1000)*sub_rate)/12)

in_vol = stats.poisson.rvs(mu=in_mu,size=mths)

app_vol = in_vol * app_rate

out_vol = np.zeros(shape = mths, dtype="int")

mth_durs = []
clos_mth = []
clos_mths = []
for i in range(mths):
    mth_durs.append(np.array(stats.gamma.rvs(mean_dur, size=in_vol[i])))
    #closure month -- add current month + duration
    clos_mth = np.ceil(mth_durs[-1]) + i
    [clos_mths.append(j) for j in clos_mth]

#sum(clos_mth)                      

for i in range(1,mths): #first element remains 0
    out_vol[i] = sum(1 for x in clos_mths if x == i)
    block_size[i] = in_vol[i] + block_size[i-1] - out_vol[i]

[print(in_vol[i], out_vol[i], block_size[i]) for i in range(mths)]

#avg caseload
caseloads = stats.norm.rvs(loc=caseload, scale=5, size=mths)
num_fte = block_size / caseloads

data_f = pd.DataFrame({'ins': in_vol, 
                       'outs': out_vol, 
                       'block': block_size, 
                       'caseload': caseloads, 
                       'fte': num_fte})

data_f.to_csv(r"~\df_test.csv")    
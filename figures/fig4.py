#!/usr/bin/env python
import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pylab as plt
import matplotlib.gridspec as gridspec
print ("modules imported")

def load_pltdat(model, opt, target, nth_kfold=None):
    load=pd.read_csv("./_pltdata/"+model+opt+"_"+target+"_shap_kfold"+str(nth_kfold)+".dat",
                     header=0, index_col=0)
    return(load)

def pltdat(model, target, opt):
    #combine 5-cross validation
    for i in range(1):
        load=load_pltdat(model, opt, target, nth_kfold=i)
        if i==0: concat=load.copy()
        else:    concat=pd.concat([concat, load.copy()], ignore_index=True)

    #reorder by importance
    concat=concat.reindex(concat.median().sort_values().index, axis=1)
    return(concat)

def plt_shap(ax, pltshap, target):

    features=pltshap.columns
    plt_shap=[pltshap[x].values for x in features]
    positions=range(len(plt_shap))
    bph=plt.boxplot(plt_shap, positions=positions, widths=0.5,
                    showfliers=True, patch_artist=True, whis=[10,90],
                    boxprops=dict(facecolor='None', color='k'),
                    whiskerprops=dict(color='k'),
                    medianprops=dict(color='k'),
                    flierprops=dict(ms=.5), vert=False)
    plt.xticks(np.arange(0,14+1,2), np.arange(0,14+1,2), fontsize=8)
    plt.yticks(positions, ['AOD' if x =='aod443' else ('TEMP' if x=='t2m' else x.upper()) for x in features], fontsize=8)
    plt.xlabel("Mean(|SHAP value|)", fontsize=9, labelpad=10)
    if target=='PM10': plt.text(-.5,7,"a) PM10", fontsize=10, weight='bold')
    if target=='PM25': plt.text(-.5,7,"b) PM2.5", fontsize=10, weight='bold')


print("****** Input Importance *******")

###
model='rf'
opt=''
###

fig=plt.figure(figsize=(6,3))
gs = gridspec.GridSpec(1,2,
                       wspace=.4,
                       left=0.1, right=0.95, bottom=0.2, top=0.85)


###
target='PM10'
###

ax=fig.add_subplot(gs[0])
plt_shap(ax, pltdat(model, target, opt), target)

###
target='PM25'
###
ax=fig.add_subplot(gs[1])
plt_shap(ax, pltdat(model, target, opt), target)

plt.show()

#!/usr/bin/env python
import numpy as np
import pandas as pd
from scipy import stats

import matplotlib as mpl
import matplotlib.pylab as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.lines import Line2D
print ("modules imported")

def load_pltdat(model=None, target=None):
    load=pd.read_csv('./_pltdata/temporal_'+model+'.ungauged_'+target+'.dat',
                        header=0, index_col=None, na_values=-9999)
    return(load)

def load_pltdat0(model=None, target=None, opt=''):
    load=pd.read_csv('./_pltdata/temporal'+opt+'_model_perform_'+target+'.dat',
                        header=0, index_col=None, na_values=-9999)
    load=load[['lat','lon',model+'corr',model+'re']].copy()
    print(load.describe())
    return(load)

##### MAIN #####
fig= plt.figure(figsize=(7, 3), facecolor='w', edgecolor='k')
gs = gridspec.GridSpec(1, 3,
                       width_ratios=[1,.1,1], hspace=.1,
                       left=.1, bottom=.15, top=.9, right=.95)

#####
model='RF'
target='PM10'
pltdats=load_pltdat(model=model, target=target)
pltdats0=load_pltdat0(model=model, target=target, opt='') #at n=0
#####


ax = fig.add_subplot(gs[0])
ax.xaxis.set_label_position('top')

n=[0,1,2,4,8]
positions=range(len(n))
xx=[pltdats['corr'+str(x)] for x in n[1:]]

xx.insert(0, pltdats0[model+'corr'])

bph=plt.boxplot(xx, positions=positions, widths=0.6, whis=[10,90],
                showfliers=True, patch_artist=True,
                boxprops=dict(facecolor='None', color='k'),
                whiskerprops=dict(color='k'),
                medianprops=dict(color='k'),
                flierprops=dict(marker='+', markerfacecolor='r', markersize=3))

plt.xticks(positions,['gauged']+['n'+str(x) for x in n[1:]], fontsize=8)
plt.xlabel("# of neighboring stations", fontsize=9, labelpad=-190)
ax.axvspan(positions[0]-.5, positions[0]+.5, alpha=0.2, color='lightgrey')
plt.ylabel('corr. coeff.', fontsize=9, labelpad=5)
plt.yticks([0,.5,1], fontsize=8)
plt.ylim(0,1)
ax.text(-.5,1.05,'a)',fontsize=9, weight='bold')


ax = fig.add_subplot(gs[2])
ax.xaxis.set_label_position('top')
xx=[pltdats['re'+str(_n)] for _n in n[1:]]
xx.insert(0, pltdats0[model+'re'])
bph=plt.boxplot(xx, positions=positions, widths=0.6, whis=[20,80],
                showfliers=True, patch_artist=True,
                boxprops=dict(facecolor='None', color='k'),
                whiskerprops=dict(color='k'),
                medianprops=dict(color='k'),
                flierprops=dict(marker='+', markerfacecolor='r', markersize=3))

plt.xticks(positions,['gauged']+['n'+str(x) for x in n[1:]], fontsize=8)
plt.xlabel("# of neighboring stations", fontsize=9, labelpad=-190)
ax.axvspan(positions[0]-.5, positions[0]+.5, alpha=0.2, color='lightgrey')
plt.ylabel("mean relative error", fontsize=9, labelpad=5)
plt.yticks([0,.5,1], fontsize=8)
plt.ylim(0,1)
ax.text(-.5,1.05,'b)',fontsize=9, weight='bold')


plt.show()
print("End.")

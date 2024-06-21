#!/usr/bin/env python
import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pylab as plt
import matplotlib.gridspec as gridspec
print ("modules imported")

def load_pltdat():
    load=pd.read_csv('./_pltdata/temporal_RFmulti_perform_PM10.dat',
                        header=0, index_col=None, na_values=-9999)
    return(load)


##### MAIN #####
fig= plt.figure(figsize=(7, 3), facecolor='w', edgecolor='k')
gs = gridspec.GridSpec(1, 3,
                       width_ratios=[1,.1,1], hspace=.1,
                       left=.1, bottom=.1, top=.9, right=.95)

#####
pltdats=load_pltdat()
#####

ax = fig.add_subplot(gs[0])
ax.xaxis.set_label_position('top')

n=[0,1,2,4,8]
positions=range(len(n))
xx=[pltdats['corr'+str(x)] for x in n]
print(len(positions), len(xx))

bph=plt.boxplot(xx, positions=positions, widths=0.6, whis=[10,90],
                showfliers=True, patch_artist=True,
                boxprops=dict(facecolor='None', color='k'),
                whiskerprops=dict(color='k'),
                medianprops=dict(color='k'),
                flierprops=dict(marker='+', markerfacecolor='r', markersize=3))

plt.xticks(positions,['n'+str(x) for x in n], fontsize=8)
ax.axvspan(positions[0]-.5, positions[0]+.5, alpha=0.2, color='lightgrey')
plt.ylabel('corr. coeff. [-]', fontsize=9, labelpad=5)
plt.yticks([0,.5,1], fontsize=8)
plt.ylim(0,1)
ax.text(-.5,1.05,'(a)',fontsize=9, weight='bold')


ax = fig.add_subplot(gs[2])
ax.xaxis.set_label_position('top')
xx=[pltdats['slp'+str(_n)] for _n in n]
bph=plt.boxplot(xx, positions=positions, widths=0.6, whis=[10,90],
                showfliers=True, patch_artist=True,
                boxprops=dict(facecolor='None', color='k'),
                whiskerprops=dict(color='k'),
                medianprops=dict(color='k'),
                flierprops=dict(marker='+', markerfacecolor='r', markersize=3))

plt.xticks(positions,['n'+str(x) for x in n], fontsize=8)
ax.axvspan(positions[0]-.5, positions[0]+.5, alpha=0.2, color='lightgrey')
plt.ylabel("slope [-]", fontsize=9, labelpad=5)
plt.yticks([0,0.6,1.2], fontsize=8)
plt.ylim(0,1.2)
ax.text(-.5,1.25,'(b)',fontsize=9, weight='bold')

plt.show()
print("End.")

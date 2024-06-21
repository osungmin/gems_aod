#!/usr/bin/env python
import numpy as np
import pandas as pd

from scipy import stats

import matplotlib as mpl
import matplotlib.pylab as plt
import matplotlib.gridspec as gridspec
import matplotlib.colors as mcolors
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.lines import Line2D
print ("modules imported")

def plt_imshow(ax, var):

    if var=='diff':
        pltdat_predict=pd.read_csv('./_pltdata/dirunal.PM10_yhat.dat',
                            header=0, index_col=0,
                            parse_dates=True,
                            na_values=-9999)
        pltdat_obs=pd.read_csv('./_pltdata/dirunal.PM10.dat',
                            header=0, index_col=0,
                            parse_dates=True,
                            na_values=-9999)
        pltdat=pltdat_predict-pltdat_obs

    else:
        pltdat=pd.read_csv('./_pltdata/dirunal.'+var+'.dat',
                            header=0, index_col=0,
                            parse_dates=True,
                            na_values=-9999)
    print(" *", var)

    if var=='PM10':
        vmin, vmax, int = 0, 60, 20
        clabel= '[${\mu}g/m^{3}$]'
        ylabel= True
    if var=='PM10_yhat':
        vmin, vmax, int = 0, 60, 20
        clabel = '[${\mu}g/m^{3}$]'
        ylabel= False
    if var=='diff':
        vmin, vmax, int = -10, 10, 5
        clabel = '[${\mu}g/m^{3}$]'
        ylabel= False

    if var=='diff': cmap = mpl.cm.coolwarm
    else:           cmap = mpl.cm.YlOrBr
    cmap.set_bad('whitesmoke')

    print(pltdat)
    ###
    im=ax.imshow(pltdat, cmap=cmap, vmin=vmin, vmax=vmax,
                 interpolation='none', extent=[0,15,0,12])

    plt.xticks(np.linspace(.1,15,24)[::4],np.arange(0,24,4),fontsize=8)
    if var in ['PM10','temporalRF']:
        plt.yticks(np.arange(.5,12,1),['J','F','M','A','M','J','J','A','S','O','N','D'],fontsize=7)
    else:
        plt.yticks(np.arange(.5,12,1),['']*len(np.arange(.5,12,1)))

    if ylabel: plt.ylabel("Month", fontsize=9, labelpad=6)
    plt.xlabel("Local time [hr]", fontsize=9, labelpad=6)

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)

    if var=='diff': cbar=fig.colorbar(im, cax=cax, extend='both')
    else: cbar=fig.colorbar(im, cax=cax, extend='max')
    cbar.set_ticks(np.arange(vmin, vmax+.1, int))
    cbar.ax.tick_params(labelsize=8)
    cbar.set_label(clabel, fontsize=9)


##### MAIN #####
fig= plt.figure(figsize=(9, 3), facecolor='w', edgecolor='k')
gs = gridspec.GridSpec(1, 3,
                       width_ratios=[1,1,1], wspace=.3,
                       left=.05, bottom=.1, top=.95, right=.92)

### diurnal cycle of MEASURED PM
ax = fig.add_subplot(gs[0])
# plot
plt_imshow(ax,'PM10')
ax.text(0,13,"(a) measured PM$_{10}$", fontsize=9, weight='bold')

### diurnal cycle of ESTIMATED PM
ax = fig.add_subplot(gs[1])
#plot
plt_imshow(ax, 'PM10_yhat')
ax.text(0,13,"(b) estimated PM$_{10}$", fontsize=9, weight='bold')

### diurnal cycle of PM DIFFERENCES
ax = fig.add_subplot(gs[2])
plt_imshow(ax, 'diff')
ax.text(0,13,"(c) estimated - measured PM$_{10}$", fontsize=9, weight='bold')

plt.show()
print("End.")

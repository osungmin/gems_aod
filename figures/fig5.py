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

def plt_imshow(ax, var, target, opt):

    if var=='diff':
        pltdat_predict=pd.read_csv('./_pltdata/dirunal.'+target+'_yhat'+opt+'.dat',
                            header=0, index_col=0,
                            parse_dates=True,
                            na_values=-9999)
        pltdat_obs=pd.read_csv('./_pltdata/dirunal.'+target+opt+'.dat',
                            header=0, index_col=0,
                            parse_dates=True,
                            na_values=-9999)
        pltdat=pltdat_predict-pltdat_obs

    else:
        pltdat=pd.read_csv('./_pltdata/dirunal.'+var+opt+'.dat',
                            header=0, index_col=0,
                            parse_dates=True,
                            na_values=-9999)

    if var=='PM10':
        vmin, vmax, int = 0, 80, 20
        clabel= '[${\mu}g/m^{3}$]'
        ylabel= True
    if var=='PM25':
        vmin, vmax, int = 0, 40, 10
        clabel= '[${\mu}g/m^{3}$]'
        ylabel= True
    if var=='PM10_yhat':
        vmin, vmax, int = 0, 80, 20
        clabel = '[${\mu}g/m^{3}$]'
        ylabel= False
    if var=='PM25_yhat':
        vmin, vmax, int = 0, 40, 10
        clabel = '[${\mu}g/m^{3}$]'
        ylabel= False
    if var=='diff':
        vmin, vmax, int = -10, 10, 5
        clabel = '[${\mu}g/m^{3}$]'
        ylabel= False

    if var=='diff': cmap = mpl.cm.coolwarm
    else:           cmap = mpl.cm.YlOrBr
    cmap.set_bad('whitesmoke')

    ###
    im=ax.imshow(pltdat, cmap=cmap, vmin=vmin, vmax=vmax,
                 interpolation='none', extent=[0,15,0,12])

    plt.xticks(np.linspace(.1,15,24)[::4],np.arange(0,24,4),fontsize=8)
    if var in ['PM10','PM25','temporalRF','temporalXGB']:
        plt.yticks(np.arange(.5,12,1),['J','F','M','A','M','J','J','A','S','O','N','D'],fontsize=7)
    else:
        plt.yticks(np.arange(.5,12,1),['']*len(np.arange(.5,12,1)))

    if ylabel: plt.ylabel("Month", fontsize=9, labelpad=6)
    if target=='PM25': plt.xlabel("Local time [hr]", fontsize=9, labelpad=6)

    plt.xlim(4,12)

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="10%", pad=0.05)

    if var=='diff': cbar=fig.colorbar(im, cax=cax, extend='both')
    else: cbar=fig.colorbar(im, cax=cax, extend='max')
    cbar.set_ticks(np.arange(vmin, vmax+.1, int))
    cbar.ax.tick_params(labelsize=8)
    cbar.set_label(clabel, fontsize=9)

#####
model='rf'
opt=''

##### MAIN #####
fig= plt.figure(figsize=(7, 5), facecolor='w', edgecolor='k')
gs = gridspec.GridSpec(3, 3,
                       width_ratios=[1,1,1], wspace=.2,
                       height_ratios=[1,.2,1],
                       left=.05, bottom=.1, top=.9, right=.95)

###
print(" \n**** DIURNAL CYCLE", model, opt)

###
targetvar='PM10'

### diurnal cycle of MEASURED PM
ax = fig.add_subplot(gs[0])
plt_imshow(ax, 'PM10', targetvar, opt=opt)
ax.text(0,13.5,"a) measured PM$_{10}$", fontsize=9, weight='bold')

### diurnal cycle of ESTIMATED PM
ax = fig.add_subplot(gs[1])
plt_imshow(ax, 'PM10_yhat', targetvar, opt=opt)
ax.text(0,13.5,"b) estimated PM$_{10}$", fontsize=9, weight='bold')

### diurnal cycle of PM DIFFERENCES
ax = fig.add_subplot(gs[2])
plt_imshow(ax, 'diff', targetvar, opt=opt)
ax.text(0,13.5,"c) estimated - measured PM$_{10}$", fontsize=9, weight='bold')


###
targetvar='PM25'

### diurnal cycle of MEASURED PM
ax = fig.add_subplot(gs[6])
plt_imshow(ax, 'PM25', targetvar, opt=opt)
ax.text(0,13.5,"d) measured PM$_{2.5}$", fontsize=9, weight='bold')

### diurnal cycle of ESTIMATED PM
ax = fig.add_subplot(gs[7])
plt_imshow(ax, 'PM25_yhat', targetvar, opt=opt)
ax.text(0,13.5,"e) estimated PM$_{2.5}$", fontsize=9, weight='bold')

### diurnal cycle of PM DIFFERENCES
ax = fig.add_subplot(gs[8])
plt_imshow(ax, 'diff', targetvar, opt=opt)
ax.text(0,13.5,"f) estimated - measured PM$_{2.5}$", fontsize=9, weight='bold')


plt.show()
print("End.")

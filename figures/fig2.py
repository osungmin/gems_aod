#!/usr/bin/env python
import numpy as np
import pandas as pd

from scipy import stats

import matplotlib as mpl
import matplotlib.pylab as plt
import matplotlib.gridspec as gridspec
print ("modules imported")

def load_meta():
    meta=pd.read_csv('./_pltdata/meta_airkorea_fin.csv',
                     header=0, index_col=0)
    return(meta[:5])

def plt_scatter(ax, yvar=None, opt=None):

    print(" >>>", opt)
    ##
    meta=load_meta()

    xx, yy= [], []

    i=0
    for l in meta.index:
        if i%25==0: print(" ...", i, "out of", len(meta))

        if opt=='AOD':
            df=pd.read_csv('./_pltdata/concat_'+str(l)+'.dat',
                            header=0, index_col=0, parse_dates=True,
                            na_values=-9999)
            df=df.dropna(subset=['PM10',yvar])
        if opt=='RF':
            df=pd.read_csv('./_pltdata/pred.PM10.RF_'+str(l)+'.dat',
                           header=0, index_col=0, parse_dates=True,
                           na_values=-9999)
            df=df.dropna(subset=['PM10',yvar])

        xx.extend(df['PM10'].values)
        yy.extend(df[yvar].values)
        i+=1

    ## Model Performance - temporal
    xmin = np.array(xx).min()
    xmax = np.array(xx).max()
    ymin = np.array(yy).min()
    ymax = np.array(yy).max()

    if opt=='AOD':
        cmap='plasma_r'
        ymax=4
        yticks=np.arange(0,4.1,1)
    if opt=='RF':
        cmap='YlOrBr'
        ymax=400
        yticks=np.arange(0,401,100)

    ###m main plot
    hb = ax.hexbin(xx, yy, gridsize=25,
                   bins='log', cmap=cmap,
                   mincnt=1)

    plt.xlim(0,400)
    plt.ylim(0,ymax)
    plt.xticks(np.arange(0,401,100), fontsize=8)
    plt.yticks(yticks, fontsize=8)

    cb = fig.colorbar(hb, ax=ax)
    cb.set_label('counts', fontsize=9)
    cb.ax.tick_params(labelsize=8)

    print(" - Plotting scatter")
    plt.xlabel('measured PM$_{10}$ [${\mu}g/m^{3}$]', fontsize=9)
    if opt=='AOD': plt.ylabel('GEMS AOD [-]', fontsize=9)
    if opt=='RF': plt.ylabel('estimated PM$_{10}$ [${\mu}g/m^{3}$]', fontsize=9)

    print(" - Adding mean lines")
    ax.axvline(x=np.median(xx),ymin=0,ymax=ymax,color='dimgrey',lw=.5)
    ax.axhline(y=np.median(yy),xmin=0,xmax=400,color='dimgrey',lw=.5)

    print(" - Adding regression line")
    slp, intercept, r_value, p_value, std_err = stats.linregress(xx,yy)
    xseq=np.linspace(0, 400, num=100)
    ax.plot(xseq, intercept + slp * xseq, color="k", lw=1)
    ax.plot(xseq, xseq, color="darkgrey", linestyle=':', lw=1)

    if opt=='AOD':
        ax.text(220,np.median(yy)+.02,'median='+str(round(np.median(yy),1)),fontsize=7.5,color='dimgrey')
        ax.text(np.median(xx)+.5,2.64,'median='+str(round(np.median(xx),1)),fontsize=7.5,color='dimgrey',rotation=270)
        ax.text(185, 3.55, 'r-value='+str(round(r_value,2)), color='k', fontsize=9)
        ax.text(185, 3.3, 'slp=0.21x$10^{-2}$',color='k', fontsize=9) #slope value from slp
        ax.text(185, 3.05, 'N='+str(len(xx)), color='k', fontsize=9)
        ax.text(0, 4.2, 'a)', fontsize=10, weight="bold")
    if opt=='RF':
        ax.text(220,np.median(yy)+2,'median='+str(round(np.median(yy),1)),fontsize=7.5,color='dimgrey')
        ax.text(np.median(xx)+.5,264,'median='+str(round(np.median(xx),1)),fontsize=7.5,color='dimgrey',rotation=270)
        ax.text(185, 355, 'r-value='+str(round(r_value,2)), color='k', fontsize=9)
        ax.text(185, 330, 'slp='+str(round(slp,2)), color='k', fontsize=9)
        ax.text(185, 305, 'N='+str(len(xx)), color='k', fontsize=9)
        ax.text(0, 420, 'b)', fontsize=10, weight="bold")


print("**********")
print("***** working with sample data from five stations *****")
print("**********")

##### MAIN #####
fig= plt.figure(figsize=(7, 3), facecolor='w', edgecolor='k')
gs = gridspec.GridSpec(1, 3,
                       width_ratios=[1,.15,1],
                       left=.1, bottom=.15, top=.9, right=.95)

## PM VS AOD
ax = fig.add_subplot(gs[0])
plt_scatter(ax, yvar='aod443', opt='AOD')

## PM VS ESTIMATED PM
ax = fig.add_subplot(gs[2])
plt_scatter(ax, yvar='PM10_yhat', opt='RF')

plt.show()
print("End.")

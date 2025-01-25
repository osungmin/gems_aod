#!/usr/bin/env python
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib as mpl
import matplotlib.pylab as plt
import matplotlib.gridspec as gridspec
print ("modules imported")

def load_meta():
    ##### load meta cleaned version #####
    meta=pd.read_csv('./_pltdata/meta_airkorea_v2_fin.csv',
                     header=0, index_col=0)
    return(meta)

def prep_pltdat(target=None, yvar=None, model=None):
    ##
    print("\n\n *** Preparing plot data (xx and yy) ***")
    ##
    meta=load_meta()

    xx, yy= [], []

    i=0
    for l in meta.index:
        if i%100==0: print(" ...", i, "out of", len(meta))

        if model=='AOD':
            df=pd.read_csv('./_pltdata/concat_'+str(l)+'_v2.dat',
                            header=0, index_col=0, parse_dates=True,
                            na_values=-9999)
            df=df.dropna(subset=[target,yvar])
            df=df[(df[target]>0)].copy()

        if (model=='RF')|(model=='XGB'):
            df=pd.read_csv('./_pltdata/'+'pred.'+target+'.'+model+'_'+str(l)+'.dat',
                           header=0, index_col=0, parse_dates=True,
                           na_values=-9999)
            df=df.dropna(subset=[target,yvar])
            df=df[(df[target]>0)].copy()

        xx.extend(df[target].values)
        yy.extend(df[yvar].values)

        i+=1

    ## Model Performance - temporal
    xmin = np.array(xx).min()
    xmax = np.array(xx).max()
    ymin = np.array(yy).min()
    ymax = np.array(yy).max()
    return(xx, yy)

def plt_scatter(ax, xx, yy, target=None, model=None):
    ##
    print("\n\n *** PLOTTING  ***")
    ##

    if model=='AOD':
        cmap='plasma_r'
        ymax=4
        xmin, xmax=0,400
        ymin, ymax=0,4
        xticks=np.arange(0,401,100)
        yticks=np.arange(0,4.1,1)


    if (model=='RF')|(model=='XGB'):
        cmap='YlOrBr'
        xmin, xmax=3,650
        ymin, ymax=3,650
        xticks=[10,50,100,300]
        yticks=[10,50,100,300]

    hb = plt.scatter(xx,yy,s=.5,c='lightgrey',alpha=.1)

    if target=='PM10':
        plt.xlabel('measured PM$_{10}$ [${\mu}g/m^{3}$]', fontsize=9)
        if model=='AOD': plt.ylabel('GEMS AOD [-]', fontsize=9)
        else: plt.ylabel('estimated PM$_{10}$ [${\mu}g/m^{3}$]', fontsize=9)
    if target=='PM25':
        plt.xlabel('measured PM$_{2.5}$ [${\mu}g/m^{3}$]', fontsize=9)
        if model=='AOD': plt.ylabel('GEMS AOD [-]', fontsize=9)
        else: plt.ylabel('estimated PM$_{2.5}$ [${\mu}g/m^{3}$]', fontsize=9)

    ax.axvline(x=np.median(xx),ymin=0,ymax=ymax,color='dimgrey',lw=.5)
    ax.axhline(y=np.median(yy),xmin=0,xmax=400,color='dimgrey',lw=.5)

    #####
    if model=='AOD':
        slp, intercept, r_value, p_value, std_err = stats.linregress(x=np.log(xx),y=np.log(yy))
        xseq=np.linspace(xmin, xmax, num=50)
        ax.plot(xseq, intercept + slp * xseq, color="k", lw=1)
        ax.plot(xseq, xseq, color="darkgrey", linestyle=':', lw=1)

        ax.text(235,np.median(yy)+.02,'median='+str(round(np.median(yy),1)),fontsize=7.5,color='dimgrey')
        ax.text(np.median(xx)+.5,2.54,'median='+str(round(np.median(xx),1)),fontsize=7.5,color='dimgrey',rotation=270)
        ax.text(210, 3.55, 'N='+str(len(xx)), color='k', fontsize=9)
        ax.text(210, 3.3, 'r-value='+str(round(r_value,2)), color='k', fontsize=9)
        if target=='PM10': ax.text(-20, 4.2, 'a)', fontsize=10, weight="bold")
        if target=='PM25': ax.text(-20, 4.2, 'd)', fontsize=10, weight="bold")

    if (model=='RF')|(model=='XGB'):

        ax.set_xscale('symlog', linthresh=1)
        ax.set_yscale('symlog', linthresh=1)

        # Log-log transformation
        log_xx = np.log(xx)
        log_yy = np.log(yy)

        slp, intercept, r_value, p_value, std_err = stats.linregress(x=log_xx,y=log_yy)
        xseq = np.linspace(xmin, xmax, 100)  # Range of xx values
        ax.plot(xseq, np.exp(intercept) * xseq**slp, color="k", lw=1) # Back-transformed regression line
        ax.plot(xseq, xseq, color="darkgrey", linestyle=':', lw=1)

        slp, intercept, r_value, p_value, std_err = stats.linregress(x=xx,y=yy)
        ax.text(95,np.median(yy)+2,'median='+str(round(np.median(yy),1)),fontsize=7.5,color='k')
        ax.text(np.median(xx)+.5,95,'median='+str(round(np.median(xx),1)),fontsize=7.5,color='k',rotation=270)
        ax.text(80, 4, 'r-value='+str(round(r_value,2)),
                color='k', fontsize=9)
        ax.text(80, 5.5, 'N='+str(len(xx)),
                color='k', fontsize=9)
        if target=='PM10': ax.text(2, 800, 'b)', fontsize=10, weight="bold")
        if target=='PM25': ax.text(2, 800, 'e)', fontsize=10, weight="bold")

    plt.xlim(xmin,xmax)
    plt.ylim(ymin,ymax)
    plt.xticks(xticks, xticks, fontsize=8)
    plt.yticks(yticks, yticks, fontsize=8)
    plt.grid(alpha=0.3)


def plt_err(ax, xx, yy, target=None):
    ##
    print("\n\n *** PLOTTING RE ERROR***")
    ##

    percentiles = np.percentile(xx, np.linspace(0, 100, 11))

    midpoints_x, midpoints_y = [],[]
    lower_y, upper_y = [], []

    xx, yy = np.array(xx), np.array(yy)

    data_num= []
    for i in range(len(percentiles) - 1):
        mask = (xx >= percentiles[i]) & (xx < percentiles[i + 1])
        midpoints_x.append((percentiles[i] + percentiles[i + 1]) / 2)
        re=(yy[mask]-xx[mask])/xx[mask]
        midpoints_y.append(np.median(re))
        lower_y.append(np.percentile(re, 25))  # 하위 25%
        upper_y.append(np.percentile(re, 75))  # 상위 75%

        data_num.append(len(yy[mask]))

    plt.plot(midpoints_x, midpoints_y, ms=2, color="k", marker="o")
    plt.fill_between(midpoints_x, lower_y, upper_y, color='lightgrey', alpha=0.5)

    ax.set_xscale('symlog', linthresh=1)

    plt.xticks([10,50,100,300],[10,50,100,300],fontsize=8)
    plt.yticks(np.arange(-1,3.1,1),np.arange(-1,3.1,1),fontsize=8)
    plt.ylabel('Relative error', fontsize=9)
    plt.grid(alpha=0.3)

    plt.xlim(3,650)
    plt.ylim(-1,3)

    ax.axhline(y=0,xmin=0,xmax=650,c='k',linestyle=':',lw=1)

    if target=='PM10':
        ax.text(3.2,.1,'overestimated',fontsize=7.5,color='k')
        ax.text(3.2,-.2,'underestimated',fontsize=7.5,color='k')
        plt.xlabel('measured PM$_{10}$ [${\mu}g/m^{3}$]', fontsize=9)
        plt.text(2, 3.2, 'c)', fontsize=10, weight="bold")
    if target=='PM25':
        plt.xlabel('measured PM$_{2.5}$ [${\mu}g/m^{3}$]', fontsize=9)
        plt.text(2, 3.2, 'f)', fontsize=10, weight="bold")

##### MAIN #####
fig= plt.figure(figsize=(9, 6), facecolor='w', edgecolor='k')
gs = gridspec.GridSpec(2, 5,
                       width_ratios=[1,.15,1,.15,1],
                       height_ratios=[1,1], hspace=.4,
                       left=.07, bottom=.1, top=.9, right=.98)

###
target='PM10'
model='RF'
###

## PM VS AOD
ax = fig.add_subplot(gs[0])
xx,yy =prep_pltdat(target=target, yvar='aod443', model='AOD')
plt_scatter(ax, xx, yy, target=target, model='AOD')

## PM VS ESTIMATED PM
ax = fig.add_subplot(gs[2])
xx,yy =prep_pltdat(target=target, yvar=target+'_yhat', model=model)
plt_scatter(ax, xx, yy, target=target, model=model)

## PM VS ESTIMATED PM
ax = fig.add_subplot(gs[4])
plt_err(ax, xx, yy, target=target)


###
target='PM25'
###

## PM VS AOD
ax = fig.add_subplot(gs[5])
xx,yy =prep_pltdat(target=target, yvar='aod443', model='AOD')
plt_scatter(ax, xx, yy, target=target, model='AOD')

## PM VS ESTIMATED PM
ax = fig.add_subplot(gs[7])
xx,yy =prep_pltdat(target=target, yvar=target+'_yhat', model=model)
plt_scatter(ax, xx, yy, target=target, model=model)

## PM VS ESTIMATED PM
ax = fig.add_subplot(gs[9])
plt_err(ax, xx, yy, target=target)

plt.show()
print("End.")

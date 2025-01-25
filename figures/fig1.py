#!/usr/bin/env python
import numpy as np
import pandas as pd
from scipy import stats

import matplotlib as mpl
import matplotlib.pylab as plt
import matplotlib.gridspec as gridspec
import matplotlib.colors as mcolors
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.basemap import Basemap
from matplotlib.ticker import FormatStrFormatter
from matplotlib.colors import LinearSegmentedColormap
print ("modules imported")


def load_meta():
    load=pd.read_csv('./_pltdata/meta_aeronet_v2_fin.csv',
                        header=0, index_col=0)
    return(load)

def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = LinearSegmentedColormap.from_list(
        f'trunc({cmap.name},{minval},{maxval})',
        cmap(np.linspace(minval, maxval, n))
    )
    return new_cmap

def plt_map(ax, meta):
    print("\n\n ***** PLOTTING THE MAP")
    #####
    lats=meta['lat'].values
    lons=meta['lon'].values
    #####

    llcrnrlat, urcrnrlat, llcrnrlon, urcrnrlon= 33, 40.01, 124, 130.5
    m = Basemap(llcrnrlon=llcrnrlon, llcrnrlat=llcrnrlat, urcrnrlon=urcrnrlon, urcrnrlat=urcrnrlat,
                resolution='i', projection='mill', ax=ax)

    m.drawmapboundary(fill_color='white', zorder=-1)
    m.fillcontinents(color='0.9', lake_color='white', zorder=0)

    m.drawcoastlines(color='0.6', linewidth=0.5)
    m.drawcountries(color='0.6', linewidth=0.5)

    m.drawparallels(np.arange(25., 180., 5.), labels=[1,0,0,1], dashes=[1,1], linewidth=0.25, color='0.5', fontsize=8)
    m.drawmeridians(np.arange(0., 360., 5.), labels=[1,0,0,1], dashes=[1,1], linewidth=0.25, color='0.5', fontsize=8)

    ## Model Performance - Spatial
    corr=[]
    distances=[]
    i=0
    for l in meta.index:
        df=pd.read_csv("./_pltdata/concat_"+str(l)+".dat",
                       header=0, index_col=0,
                       parse_dates=True, na_values=-9999)
        df=df[(df['AOD_440nm']>=0)&(df['aod443']>=0)].copy()
        df=df[df['distance']<5].copy()  #5 km limit
        corr.append(stats.pearsonr(df['AOD_440nm'].values, df['aod443'].values).statistic)
        distances.append(np.max(df['distance']))
        i+=1

    ##
    cmap=plt.cm.get_cmap("viridis",5)

    for i in range(len(meta)):
        x, y = m(lons[i], lats[i])
        plt.scatter(x, y, c=corr[i], vmin=0, vmax=1,
                    s=5, marker='o', cmap=cmap)

    #title
    x, y= m(124,40.4)
    ax.text(x, y, 'a)', fontsize=10, weight="bold")

    cb = plt.colorbar(ax=ax, fraction=0.055, pad=0.04)
    cb.set_ticks(np.arange(0,1.1,.2))
    cb.ax.tick_params(labelsize=8)
    cb.set_label('corr. coeff. [-]', fontsize=9)


def plt_scatter(ax, meta):
    print("\n\n ***** PLOTTING SCATTOR")
    xx, yy= [], []

    i=0
    for l in meta.index:
        df=pd.read_csv("./_pltdata/concat_"+str(l)+".dat",
                       header=0, index_col=0,
                       parse_dates=True, na_values=-9999)
        df=df[(df['AOD_440nm']>0)&(df['aod443']>0)].copy()
        df=df[df['distance']<5].copy() #5 km limit
        xx.extend(df['AOD_440nm'].values)
        yy.extend(df['aod443'].values)
        i+=1

    ## Model Performance - temporal
    xmin = np.array(xx).min()
    xmax = np.array(xx).max()
    ymin = np.array(yy).min()
    ymax = np.array(yy).max()


    cmap = truncate_colormap(plt.get_cmap('hot_r'), minval=.3, maxval=1)
    hb = ax.hexbin(xx, yy, gridsize=55,
                   cmap=cmap,
                   mincnt=1)

    plt.xticks(np.arange(0,2.6,.5), fontsize=8)
    plt.yticks(np.arange(0,2.6,.5), fontsize=8)

    cb = fig.colorbar(hb, ax=ax, fraction=0.046, pad=0.04, extend='max')
    cb.set_label('counts', fontsize=9)
    cb.set_ticks(np.arange(0,301,100))
    cb.ax.tick_params(labelsize=8)

    plt.xlabel('AERONET AOD (440 nm)', fontsize=9)
    plt.ylabel('GEMS AOD (443 nm)', fontsize=9)

    ax.axvline(x=np.mean(xx),ymin=0,ymax=2.5,color='dimgrey',lw=.5)
    ax.axhline(y=np.mean(yy),xmin=0,xmax=2.5,color='dimgrey',lw=.5)

    ax.text(1.4,np.mean(yy)+.03,'median='+str(round(np.median(yy),2)),fontsize=8,color='dimgrey')
    ax.text(np.mean(xx),1.5,'median='+str(round(np.median(xx),2)),fontsize=8,color='dimgrey',rotation=270)

    #regression
    slp, intercept, r_value, p_value, std_err = stats.linregress(xx,yy)
    xseq=np.linspace(0, 2.5, num=25)
    ax.plot(xseq, intercept + slp * xseq, color="brown", lw=1)
    ax.plot(xseq, xseq, color="darkgrey", linestyle=':', lw=1)

    ax.text(1.3, 2.3, 'r-value='+str(round(r_value,2)),
            color='k', fontsize=9)
    ax.text(1.3, 2.1, 'slp='+str(round(slp,2)),
            color='k', fontsize=9)
    ax.text(1.3, 1.9, 'n='+str(len(xx)),
            color='k', fontsize=9)

    ax.text(0, 2.77, 'b)', fontsize=10, weight="bold")

    ax.set_xlim(0,2.5)
    ax.set_ylim(0,2.5)


def plt_err(ax, meta):
    print("\n\n ***** PLOTTING ERROR")

    xx, yy= [], []

    i=0
    for l in meta.index:
        df=pd.read_csv("./_pltdata/concat_"+str(l)+".dat",
                       header=0, index_col=0,
                       parse_dates=True, na_values=-9999)
        df=df[(df['AOD_440nm']>0)&(df['aod443']>0)].copy()
        df=df[df['distance']<5].copy()  #5 km limit
        xx.extend(df['AOD_440nm'].values)
        yy.extend(df['aod443'].values)
        i+=1

    ## Model Performance - temporal
    xmin = np.array(xx).min()
    xmax = np.array(xx).max()
    ymin = np.array(yy).min()
    ymax = np.array(yy).max()

    xvar=np.array(xx)
    yvar=np.array(yy)

    percentiles = np.percentile(xvar, np.linspace(0, 100, 6))

    midpoints_x = []
    midpoints_y = []
    upper_y = []
    lower_y = []

    for i in range(len(percentiles) - 1):
        mask = (xvar >= percentiles[i]) & (xvar < percentiles[i + 1])
        midpoints_x.append((percentiles[i] + percentiles[i + 1]) / 2)

        re=(yvar[mask]-xvar[mask])/xvar[mask]
        ###re=np.corrcoef(yvar[mask],xvar[mask])[0,1]
        midpoints_y.append(np.median(re))
        lower_y.append(np.percentile(re, 25))
        upper_y.append(np.percentile(re, 75))


    plt.plot(midpoints_x, midpoints_y, ms=2, color="k", marker="o")
    plt.fill_between(midpoints_x, lower_y, upper_y, color='lightgrey', alpha=0.5)

    ax.set_xscale('symlog', linthresh=1)

    plt.xticks([0,.5,1,2],[0,.5,1,2],fontsize=8)
    plt.yticks(np.arange(-.8,0.81,.4),np.arange(-.8,0.81,.4),fontsize=8)
    plt.ylabel('Relative error', fontsize=9)
    plt.xlabel('AERONET AOD (440 nm)', fontsize=9)
    plt.grid(alpha=0.3)
    ax.set_xlim(0,2.5)
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

    ax.text(0, .93, 'c)', fontsize=10, weight="bold")


##### ================ MAIN ================ #####
fig= plt.figure(figsize=(9, 3), facecolor='w', edgecolor='k')
gs = gridspec.GridSpec(1, 5,
                       width_ratios=[.9,.3,1,.3,.9],
                       left=.05, bottom=.15, top=.9, right=.98)


## FIG 1-1. the map of corr. coeff.
ax = fig.add_subplot(gs[0])
plt_map(ax, load_meta())

## FIG 1-2. scatter comparison
ax = fig.add_subplot(gs[2])
plt_scatter(ax, load_meta())
ax.axes.set_aspect('equal')

## FIG 1-3. error analysis
ax = fig.add_subplot(gs[4])
plt_err(ax, load_meta())
ax.set_aspect(1)

##### ================ MAIN ================ #####

plt.show()
print("End.")

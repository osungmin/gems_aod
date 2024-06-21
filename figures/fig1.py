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
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.patches import Polygon
from matplotlib.patches import ConnectionPatch
from matplotlib.ticker import FormatStrFormatter
print ("modules imported")


def load_data(opt=None):
    if opt=='rf':
        load=pd.read_csv('./_pltdata/temporal_model_perform_PM10.dat',
                        header=0, index_col=None, na_values=-9999)
        load=load[['lat','lon','RFcorr']].copy()
    if opt=='obs':
        load=pd.read_csv('../_pltdata/PM10_overlap.dat',
                          header=0, index_col=None)
        load=load[['lat','lon','PM10mean_overlap','PM10_yhat_mean_overlap']].copy()
    return(load)

def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = mcolors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap

def draw_screen_poly(m, opt=None):
    if opt=='gems':
       plats = [-5, 45, 45,-5]
       plons = [75, 75, 145, 145]

       x, y = m(plons, plats)
       xy = zip(x,y)
       poly = Polygon(list(xy), color='lightgrey', fill=True, alpha=.5)
       plt.gca().add_patch(poly)

    if opt=='korea':
       plats = [32.5, 39.5, 39.5, 32.5]
       plons = [123, 123, 132, 132]

       x, y = m(plons, plats)
       xy = zip(x,y)
       poly = Polygon(list(xy), fill=False, alpha=1, linewidth=.5)
       plt.gca().add_patch(poly)

def get_bins(x_bins, xpdf_bins, bins, statmode):

    bincals, binedges, binnumber = stats.binned_statistic(x_bins, xpdf_bins,\
                                                         statistic=statmode, bins=bins)
    if statmode == 'sum':
        bincals = (bincals/np.sum(x_bins))*100.
    elif statmode == 'count':
        bincals = (bincals/len(x_bins))*100.
    else:
        stop

    return(bincals, binedges, binnumber)

def plt_map_asia(ax):

    print(" \n *** the map of east asia")
    ##
    llcrnrlat, urcrnrlat, llcrnrlon, urcrnrlon= -15, 55, 65, 155
    m = Basemap(llcrnrlon=llcrnrlon, llcrnrlat=llcrnrlat, urcrnrlon=urcrnrlon, urcrnrlat=urcrnrlat,
                resolution='i', projection='mill', ax=ax)

    m.drawmapboundary(fill_color='white', zorder=-1)
    m.drawcoastlines(color='0.6', linewidth=0.3)
    m.drawcountries(color='0.6', linewidth=0.3)

    # add details on the map
    m.fillcontinents(color='white', lake_color='white', zorder=0)
    m.drawparallels(np.arange(0., 180., 20.), labels=[1,0,0,1], dashes=[1,1], linewidth=0.25, color='0.5', fontsize=7)
    m.drawmeridians(np.arange(0., 360., 20.), labels=[1,0,0,1], dashes=[1,1], linewidth=0.25, color='0.5', fontsize=7)

    # mark the areas (boxes)
    draw_screen_poly(m, opt='gems')
    draw_screen_poly(m, opt='korea')

    x, y = m(73,47)
    ax.text(x,y,'GEMS', weight='bold', fontsize=8)
    return(m)

def plt_map(ax, pltdats, opt=None):

    print(" \n *** the map of Korea")
    ##
    llcrnrlat, urcrnrlat, llcrnrlon, urcrnrlon= 32.5, 39.51, 124, 130.5
    m = Basemap(llcrnrlon=llcrnrlon, llcrnrlat=llcrnrlat, urcrnrlon=urcrnrlon, urcrnrlat=urcrnrlat,
                resolution='i', projection='mill', ax=ax)

    m.drawmapboundary(fill_color='white', zorder=-1)
    m.drawcoastlines(color='0.6', linewidth=0.3)
    m.drawcountries(color='0.6', linewidth=0.3)

    m.fillcontinents(color='lightgrey', lake_color='white', zorder=0, alpha=0.5)
    m.drawparallels(np.arange(0, 180., 2), labels=[1,0,0,1], dashes=[1,1], linewidth=0.25, color='0.5', fontsize=8)
    m.drawmeridians(np.arange(0, 360., 2), labels=[1,0,0,1], dashes=[1,1], linewidth=0.25, color='0.5', fontsize=8)

    lats=pltdats['lat']
    lons=pltdats['lon']

    ## aerosol concentrations
    if (opt=='a')|(opt=='b'):

        if opt=='a': pval=pltdats['PM10mean_overlap']
        if opt=='b': pval=pltdats['PM10_yhat_mean_overlap']
        cmap = truncate_colormap(plt.get_cmap('YlOrRd'), 0.1, 1)

        #location of PM10 with annual average
        vmin, vmax=20, 60

        for i in range(len(pltdats)):
            x, y = m(lons[i], lats[i])
            plt.scatter(x, y, 1.1, marker='o', vmin=vmin, vmax=vmax,
                        c=pval[i], cmap=cmap, alpha=0.7)

        ## colorbar
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cbar=plt.colorbar(extend='max', cax=cax)
        cbar.ax.tick_params(labelsize=8)

        cbar.set_ticks(np.arange(20,60+1,10))
        if opt=='a': cbar.set_label('measured PM$_{10}$ [${\mu}g/m^{3}$]', fontsize=9)
        if opt=='b': cbar.set_label('estimated PM$_{10}$ [${\mu}g/m^{3}$]', fontsize=9)

        print(" >>> ax_inset")
        ax_inset = inset_axes(ax, "100%", "100%", loc="upper left",
                         bbox_to_anchor=(0.72,0.11,.22,.2), bbox_transform=ax.transAxes)

        bins=np.arange(20,vmax+1,2.5)
        bins[-1]=70 #due to max
        xticks=np.arange(20,vmax+1,10)
        yticks=np.arange(0,21,10)
        ylim_max=20

        pval_counts, dum, dum=get_bins(pval, pval, bins, 'count')
        xticks_plt= [(a + b) / 2 for a, b in zip(bins, bins[1:])]
        plt.plot(xticks_plt, pval_counts, color='dimgrey', lw=.8, linestyle='-')
        plt.xticks(xticks,xticks,fontsize=7,rotation=90)
        plt.yticks(yticks,fontsize=7)
        plt.ylabel('PDF [%]', fontsize=8)
        plt.ylim(0,ylim_max)

        ax_inset.tick_params(axis='x', pad=1, length=1)
        ax_inset.tick_params(axis='y', pad=1, length=1)

    ## Model Performance
    if opt=='c':
        cmap=plt.cm.get_cmap("viridis",5)

        for i in range(len(pltdats)):
            x, y = m(lons[i], lats[i])
            plt.scatter(x, y, c=pltdats['RFcorr'].values[i], vmin=0, vmax=1,
                        s=1, marker='o', cmap=cmap)

        ## inset
        print(" >>> ax_inset")
        ax_inset = inset_axes(ax, "100%", "100%", loc="upper left",
                         bbox_to_anchor=(0.05,0.9,.4,.1), bbox_transform=ax.transAxes)
        ax_inset.spines['top'].set_visible(False)
        ax_inset.spines['right'].set_visible(False)
        ax_inset.spines['left'].set_visible(False)

        bph=plt.boxplot(pltdats['RFcorr'], positions=[1], widths=0.6, whis=[10,90],
                        showfliers=True, patch_artist=True, vert=False,
                        boxprops=dict(facecolor='None', color='k'),
                        whiskerprops=dict(color='k'),
                        medianprops=dict(color='k'),
                        flierprops=dict(ms=2))


        plt.tick_params(axis='y',          # changes apply to the x-axis
                        which='both',      # both major and minor ticks are affected
                        left=False)
        plt.yticks([])
        plt.xticks(np.arange(.4,.81,.2),np.arange(.4,.81,.2), fontsize=7)
        ax_inset.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
        #plt.xlabel('corr. coeff. (r)', fontsize=7, labelpad=1)

        ## colorbar
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cbar=plt.colorbar(cax=cax)
        cbar.set_ticks(np.arange(0,1.1,.2))
        cbar.ax.tick_params(labelsize=8)
        cbar.set_label('corr. coeff. [-]', fontsize=9)

    x, y = m(124,40)
    ax.text(x,y,opt+')', weight='bold', fontsize=10)

    return(m)


############### MAIN ###############
fig= plt.figure(figsize=(12, 4), facecolor='w', edgecolor='k')
gs = gridspec.GridSpec(1, 7,
                       width_ratios=[.5,.1,1,.2,1,.2,1],
                       left=.05, bottom=.15, top=.99, right=.95)

##### LEFT MAP - ASIA, GEMS
gs1 = gridspec.GridSpecFromSubplotSpec(2, 1,
               subplot_spec=gs[0], height_ratios=[1.5,1], hspace=0)
ax1 = fig.add_subplot(gs1[0])
m1=plt_map_asia(ax1)

##### SECOND MAP - PM concentrations
gs2 = gridspec.GridSpecFromSubplotSpec(2, 1,
              subplot_spec=gs[2], height_ratios=[.2,1], hspace=0)
ax2 = fig.add_subplot(gs2[1])
m2=plt_map(ax2, pltdats=load_data(opt='obs'), opt='a')

##### Zoom-in lines between the maps
xA, yA = m1(124,32.5)
xB, yB = m2(124,32.5)
conn = ConnectionPatch(
        xyA=(xA, yA), coordsA='data', axesA=ax1,
        xyB=(xB, yB), coordsB='data', axesB=ax2,
        color='k', linewidth=.5,
    )
ax2.add_artist(conn)
conn.set_in_layout(False)

xA, yA = m1(124,39.5)
xB, yB = m2(124,39.5)
conn = ConnectionPatch(
        xyA=(xA, yA), coordsA='data', axesA=ax1,
        xyB=(xB, yB), coordsB='data', axesB=ax2,
        color='k', linewidth=.5,
    )
ax2.add_artist(conn)
conn.set_in_layout(False)

##### THIRD MAP - ESIMATED PM concentrations
gs3 = gridspec.GridSpecFromSubplotSpec(2, 1,
              subplot_spec=gs[4], height_ratios=[.2,1], hspace=0)
ax3 = fig.add_subplot(gs3[1])
m3=plt_map(ax3, pltdats=load_data(opt='obs'), opt='b')

##### LAST MAP - CORR BETWEEN MEASURED AND ESTIMATED PM
gs4 = gridspec.GridSpecFromSubplotSpec(2, 1,
              subplot_spec=gs[6], height_ratios=[.2,1], hspace=0)
ax4 = fig.add_subplot(gs4[1])
m4=plt_map(ax4, pltdats=load_data(opt='rf'), opt='c')

plt.show()
print("End.")


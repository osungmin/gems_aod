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


def load_meta(model=None, target=None, var_opt=None, opt=None):

    if (opt=='c')|(opt=='f'):
        load=pd.read_csv('./_pltdata/temporal'+var_opt+'_model_perform_'+target+'.dat',
                        header=0, index_col=None, na_values=-9999)
        load=load[['lat','lon',model+'corr']].copy()
    else:
        #the final station list from make_final_list.py
        load=pd.read_csv('./_pltdata/'+model+'.'+target+'_overlap_v2.dat',
                          header=0, index_col=None)
        load=load[['lat','lon',target+'mean_overlap',target+'_yhat_mean_overlap']].copy()
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

    if opt=='white':
       plats = [32.6, 34, 34, 32.6]
       plons = [128.5, 128.5, 130.48, 130.48]

       x, y = m(plons, plats)
       xy = zip(x,y)
       poly = Polygon(list(xy), facecolor='w', fill=True, alpha=1)
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
    m.drawmeridians(np.arange(0., 360., 30.), labels=[1,0,0,1], dashes=[1,1], linewidth=0.25, color='0.5', fontsize=7)

    # mark the areas (boxes)
    draw_screen_poly(m, opt='gems')
    draw_screen_poly(m, opt='korea')

    x, y = m(73,47)
    ax.text(x,y,'GEMS', weight='bold', fontsize=8)
    return(m)

def plt_map(ax, pltdats, model=None, var=None, opt=None):

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
    if (opt=='a')|(opt=='b')|(opt=='d')|(opt=='e'):

        if (opt=='a')|(opt=='d'): pval=pltdats[var+'mean_overlap']
        if (opt=='b')|(opt=='e'): pval=pltdats[var+'_yhat_mean_overlap']
        cmap = truncate_colormap(plt.get_cmap('YlOrRd'), 0.1, 1)

        #location of PM10 with annual average
        if var=='PM10': vmin, vmax=20, 60
        if var=='PM25': vmin, vmax=10, 25

        for i in range(len(pltdats)):
            x, y = m(lons[i], lats[i])
            plt.scatter(x, y, 1.1, marker='o', vmin=vmin, vmax=vmax,
                        c=pval[i], cmap=cmap, alpha=0.7)

        ## colorbar
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cbar=plt.colorbar(extend='max', cax=cax)
        cbar.ax.tick_params(labelsize=8)

        if var=='PM10':
            cbar.set_ticks(np.arange(20,60+1,10))
            if opt=='a': cbar.set_label('measured PM$_{10}$ [${\mu}g/m^{3}$]', fontsize=9)
            if opt=='b': cbar.set_label('estimated PM$_{10}$ [${\mu}g/m^{3}$]', fontsize=9)
        if var=='PM25':
            cbar.set_ticks(np.arange(10,25+1,5))
            cbar.set_label('measured PM$_{2.5}$ [${\mu}g/m^{3}$]', fontsize=9)
            if opt=='d': cbar.set_label('measured PM$_{2.5}$ [${\mu}g/m^{3}$]', fontsize=9)
            if opt=='e': cbar.set_label('estimated PM$_{2.5}$ [${\mu}g/m^{3}$]', fontsize=9)

        ##### inset bar plots
        draw_screen_poly(m, opt='white') #to make the white background

        print(" >>> ax_inset")
        ax_inset = inset_axes(ax, "100%", "100%", loc="upper left",
                         bbox_to_anchor=(0.72,0.12,.22,.2), bbox_transform=ax.transAxes)

        if var=='PM10':
            bins=np.arange(20,vmax+1,2.5)
            bins[-1]=70 #due to max
            xticks=np.arange(20,vmax+1,20)
            yticks=np.arange(0,21,10)
            ylim_max=20

        if var=='PM25':
            bins=np.arange(10,31,2.5)
            bins[-1]=35 #due to max
            xticks=np.arange(10,31,10)
            yticks=np.arange(0,31,15)
            ylim_max=31

        pval_counts, dum, dum=get_bins(pval, pval, bins, 'count')
        xticks_plt= [(a + b) / 2 for a, b in zip(bins, bins[1:])]
        print("sum of pval:", np.sum(pval_counts))
        plt.plot(xticks_plt, pval_counts, color='dimgrey', lw=.8, linestyle='-')
        plt.xticks(xticks,xticks,fontsize=7,rotation=90)
        plt.yticks(yticks,fontsize=7)
        plt.ylabel('PDF [%]', fontsize=8)
        plt.ylim(0,ylim_max)

        ax_inset.tick_params(axis='x', pad=.5, length=1)
        ax_inset.tick_params(axis='y', pad=1, length=1)


    ## Model Performance - Spatial
    if (opt=='c')|(opt=='f'):
        cmap=plt.cm.get_cmap("viridis",5)

        for i in range(len(pltdats)):
            x, y = m(lons[i], lats[i])
            plt.scatter(x, y, c=pltdats[model+'corr'].values[i], vmin=0, vmax=1,
                        s=1, marker='o', cmap=cmap)

        ## inset
        print(" >>> ax_inset")
        ax_inset = inset_axes(ax, "100%", "100%", loc="upper left",
                         bbox_to_anchor=(0.05,0.92,.5,.1), bbox_transform=ax.transAxes)
        ax_inset.spines['top'].set_visible(False)
        ax_inset.spines['right'].set_visible(False)
        ax_inset.spines['left'].set_visible(False)

        bph=plt.boxplot(pltdats[model+'corr'], positions=[1], widths=0.6, whis=[10,90],
                        showfliers=True, patch_artist=True, vert=False,
                        boxprops=dict(facecolor='None', color='k'),
                        whiskerprops=dict(color='k'),
                        medianprops=dict(color='k'),
                        flierprops=dict(ms=1))


        plt.tick_params(axis='y',          # changes apply to the x-axis
                        which='both',      # both major and minor ticks are affected
                        left=False)
        plt.yticks([])
        plt.xticks(np.arange(.4,.81,.2),np.arange(.4,.81,.2), fontsize=7)
        plt.xlim(.2,.8)
        ax_inset.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))


        print(" *****")
        print("mean and median", np.mean(pltdats[model+'corr']), np.median(pltdats[model+'corr']))
        print("10 and 90 percentiles", np.percentile(pltdats[model+'corr'],10),np.percentile(pltdats[model+'corr'],90))

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



#####
model='RF'
var_opt=''
#####

############### MAIN ###############
fig= plt.figure(figsize=(10, 6), facecolor='w', edgecolor='k')
gs = gridspec.GridSpec(2, 7,
                       width_ratios=[.5,.1,1,.2,1,.2,1],
                       height_ratios=[1,1],
                       left=.05, bottom=.15, top=.99, right=.95)

##### LEFT MAP - ASIA, GEMS
gs1 = gridspec.GridSpecFromSubplotSpec(2, 1,
               subplot_spec=gs[0], height_ratios=[1.5,1], hspace=0)
ax1 = fig.add_subplot(gs1[0])
m1=plt_map_asia(ax1)


##### UPPER #####
targetvar='PM10'
##### UPPER #####

gs2 = gridspec.GridSpecFromSubplotSpec(2, 1,
              subplot_spec=gs[2], height_ratios=[.2,1], hspace=0)
ax2 = fig.add_subplot(gs2[1])
m2=plt_map(ax2, pltdats=load_meta(model=model, target=targetvar, var_opt=var_opt), model=model, var=targetvar, opt='a')

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
m3=plt_map(ax3, pltdats=load_meta(model=model, target=targetvar, var_opt=var_opt), model=model, var=targetvar, opt='b')

##### LAST MAP - CORR BETWEEN MEASURED AND ESTIMATED PM
gs4 = gridspec.GridSpecFromSubplotSpec(2, 1,
              subplot_spec=gs[6], height_ratios=[.2,1], hspace=0)
ax4 = fig.add_subplot(gs4[1])
m4=plt_map(ax4, pltdats=load_meta(model=model, target=targetvar, var_opt=var_opt, opt='c'), model=model, var=targetvar, opt='c')
##### UPPER ############################################################

##### BOTTOM  #####
targetvar='PM25'
##### BOTTOM  #####

# obs
gs5 = gridspec.GridSpecFromSubplotSpec(2, 1,
              subplot_spec=gs[9], height_ratios=[.2,1], hspace=0)
ax5 = fig.add_subplot(gs5[1])
m5=plt_map(ax5, pltdats=load_meta(model=model, target=targetvar, var_opt=var_opt), model=model, var=targetvar, opt='d')

# est
gs6 = gridspec.GridSpecFromSubplotSpec(2, 1,
              subplot_spec=gs[11], height_ratios=[.2,1], hspace=0)
ax6 = fig.add_subplot(gs6[1])
m6=plt_map(ax6, pltdats=load_meta(model=model, target=targetvar, var_opt=var_opt), model=model, var=targetvar, opt='e')

# corr
gs7 = gridspec.GridSpecFromSubplotSpec(2, 1,
              subplot_spec=gs[13], height_ratios=[.2,1], hspace=0)
ax7 = fig.add_subplot(gs7[1])
m7=plt_map(ax7, pltdats=load_meta(model=model, target=targetvar, var_opt=var_opt, opt='f'), model=model, var=targetvar, opt='f')

##### BOTTOM ############################################################

plt.show()
print("End.")

#!/usr/bin/env python
import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pylab as plt
import matplotlib.gridspec as gridspec
print ("modules imported")

def load_pltdat(opt=None, nth_kfold=None):
    load=pd.read_csv("./_pltdata/rf_"+opt+"_kfold"+str(nth_kfold)+".dat",
                     header=0, index_col=0)
    #reorder by median
    load=load.reindex(load.median().sort_values().index, axis=1)
    return(load)


#combine 5-cross validation
for _n in range(5):
    rf_shap=load_pltdat(opt='shap', nth_kfold=_n)
    rf_features=rf_shap.columns
    rf_shap=[rf_shap[x].values for x in rf_features]

print("****** Input Importance *******")
print("rf_features:", rf_features)
fig=plt.figure(figsize=(5,4))
gs = gridspec.GridSpec(1,1,
                       left=0.12, right=0.9, bottom=0.15, top=0.95)

ax=fig.add_subplot(gs[0])
positions=range(len(rf_shap))
bph=plt.boxplot(rf_shap, positions=positions, widths=0.5,
                showfliers=True, patch_artist=True, whis=[10,90],
                boxprops=dict(facecolor='None', color='k'),
                whiskerprops=dict(color='k'),
                medianprops=dict(color='k'),
                flierprops=dict(ms=2), vert=False)
plt.xticks(np.arange(0,14+1,2), np.arange(0,14+1,2), fontsize=8)
plt.yticks(positions, ['AOD' if x =='aod443' else x.upper() for x in rf_features], fontsize=8)
plt.yticks(positions, ['AOD' if x =='aod443' else ('TEMP' if x=='t2m' else x.upper()) for x in rf_features], fontsize=8)
plt.xlabel("Mean(|SHAP value|)", fontsize=9, labelpad=10)

plt.show()

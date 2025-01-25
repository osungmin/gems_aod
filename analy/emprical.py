#!/usr/bin/env python
import numpy as np
import pandas as pd
import os

from scipy import stats
from scipy.optimize import curve_fit
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
import shap

import matplotlib as mpl
import matplotlib.pylab as plt
import matplotlib.gridspec as gridspec
print("modules imported")

def load_meta():
    load=pd.read_csv('list_of_stations',
                         header=0, index_col=0)
    return load

# objective function (AOD->AEROSOL)
def model1(x, a, b):
    return a*x+b

# objective function (AOD and selected METEO->AEROSOL)
def model2(X, a, b, c, d, e):
    aod, blh, rh, t2m = X
    return a*aod+ b*blh+ c*rh+ d*t2m+ e

# objective function (AOD and ALL METEO->AEROSOL)
def model3(X, a, b, c, d, e, f, g, h):
    aod, blh, rh, t2m, ws, wd, sp= X
    return a*aod+ b*blh+ c*rh+ d*t2m+ e*ws+ f*wd + g*sp+ h

# objective function (AOD and ALL METEO + presecuder ->AEROSOL)
def model4(X, a, b, c, d, e, f, g, h, i, j, k, l):
    aod, blh, rh, t2m, ws, wd, sp, co, no2, so2, o3= X
    return a*aod+ b*blh+ c*rh+ d*t2m+ e*ws+ f*wd + g*sp+ h*co+ i*no2 + j*so2+ k*o3+ l

# run the model
def fit_to_func(model, train, test, features=None, target=None):

    if model==1:
        popt1, _ = curve_fit(model1, train[features[0]], train[target])
        a1, b1 = popt1
        predicts=model1(test[features[0]], a1,b1)

    if model==2:
        popt2, _ = curve_fit(model2, (train[features[0]],train[features[1]],train[features[2]],\
                            train[features[3]]), train[target])
        a2, b2, c2, d2, e2= popt2
        predicts=model2((test[features[0]],test[features[1]],test[features[2]],\
                            test[features[3]]), a2,b2,c2,d2,e2)

    if model==3:
        popt3, _ = curve_fit(model3, (train[features[0]],train[features[1]],train[features[2]],\
                            train[features[3]],train[features[4]],train[features[5]],train[features[6]]),train[target])
        a3, b3, c3, d3, e3, f3, g3, h3 = popt3
        predicts=model3((test[features[0]],test[features[1]],test[features[2]],\
                            test[features[3]],test[features[4]],test[features[5]],test[features[6]]), a3,b3,c3,d3,e3,f3,g3,h3)


    if model==4:
        popt4, _ = curve_fit(model4, (train[features[0]],train[features[1]],train[features[2]],\
                            train[features[3]],train[features[4]],train[features[5]],train[features[6]],\
                            train[features[7]],train[features[8]],train[features[9]],train[features[10]]),train[target])
        a4, b4, c4, d4, e4, f4, g4, h4, i4, j4, k4, l4 = popt4
        predicts=model4((test[features[0]],test[features[1]],test[features[2]],\
                            test[features[3]],test[features[4]],test[features[5]],test[features[6]], \
                            test[features[7]],test[features[8]],test[features[9]],test[features[10]]), \
                            a4,b4,c4,d4,e4,f4,g4,h4,i4,j4,k4,l4)

    return predicts

# random forest
def rnd_forest(train, test, features=None, target=None):

    # Split the data into training and testing sets
    train_features, test_features= train[features].copy(), test[features].copy()
    train_labels, test_labels = train[target].copy(), test[target].copy()

    # Instantiate model with 100 decision trees
    rf = RandomForestRegressor(n_estimators = 100, max_features='sqrt',
                               random_state = 888)

    # Train the model on training data
    rf.fit(train_features, train_labels)
    predictions = rf.predict(test_features)

    # Get SHAP values
    explainer = shap.TreeExplainer(rf)
    shap_values = explainer.shap_values(test_features)

    return(predictions, np.abs(shap_values).mean(0).round(5))

# xgb
def xgb_forest(train, test, features=None, target=None):

    # Split the data into training and testing sets
    train_features, test_features= train[features].copy(), test[features].copy()
    train_labels, test_labels = train[target].copy(), test[target].copy()

    # Instantiate model with 100 decision trees
    xgb = XGBRegressor(n_estimators=100,  # Number of trees
                       learning_rate=0.1,  # Step size shrinkage
                       max_depth=6,       # Maximum depth of a tree
                       subsample=0.8,     # Fraction of samples for each tree
                       colsample_bytree=0.8,  # Fraction of features for each tree
                       random_state=42)

    xgb.fit(train_features, train_labels)
    predictions = xgb.predict(test_features)

    explainer = shap.TreeExplainer(xgb)
    shap_values = explainer.shap_values(test_features)

    return(predictions, np.abs(shap_values).mean(0).round(5))

def pm_estimate(meta, target=None, n_kfolds=None, nth_kfold=0, exp=None):
    #mainpath
    mainpath='where_your_data_are'
    #input and target
    aodvar='aod443' #target
    
  if exp=='': rf_features=[aodvar,'blh','rh','t2m','ws','wd','sp']
    if exp=='_all': rf_features=[aodvar,'blh','rh','t2m','ws','wd','sp','CO','NO2','SO2','O3']
   
    # input importance
    _xgb_shap, _rf_shap= [], []

    # main loop
    i=0
    for loc in meta.index:

        ##
        if i%50==0: print(" > ", i, "out of", len(meta))

        ##
        fpath=mainpath+'data/concat_v2_reloc/concat_'+str(loc)+'_v2.dat'
        ##

        if os.path.isfile(fpath):
            df=pd.read_csv(fpath,
                           header=0, index_col=0,
                           parse_dates=True, na_values=-9999)
            df=df.dropna(subset=rf_features+[target])

            df['wd']=df['wd']+0.1 #to avoide zero
            df['blh']=df['blh']*0.001 #m to km

            #randomly mixed df and then split into n groups
            df=df.sample(frac=1, replace = False, random_state = 88)

            #define train vs test data
            kfolds=np.array_split(df, n_kfolds)
            test=kfolds[nth_kfold].copy() #20% to test
            train=df.drop(test.index, axis=0) #80% to train

            if len(df) != len(train)+len(test): stop

            # fit curve
            if (exp=='')|(exp=='_all'):
                y_predict1=fit_to_func(1, train.copy(), test.copy(), features=[aodvar], target=target)
                y_predict2=fit_to_func(2, train.copy(), test.copy(), features=[aodvar,'blh','rh','t2m'], target=target)
                y_predict3=fit_to_func(3, train.copy(), test.copy(), features=[aodvar,'blh','rh','t2m','ws','wd','sp'], target=target)
            if exp=='_all': y_predict4=fit_to_func(4, train.copy(), test.copy(), features=rf_features, target=target)
            
            #no scaling
            train_sc=train.copy()
            test_sc=test.copy()

            rf_predict, rf_shap=rnd_forest(train_sc.copy(), test_sc.copy(), features=rf_features, target=target)
            xgb_predict, xgb_shap=xgb_forest(train_sc.copy(), test_sc.copy(), features=rf_features, target=target)

            _rf_shap.append(rf_shap)
            _xgb_shap.append(xgb_shap)

            # save model prediction
            if (exp==''):
                models=['M1','M2','M3','RF','XGB']
                y_predicts=[y_predict1, y_predict2, y_predict3, rf_predict, xgb_predict]
            if exp=='_all':
                models=['M1','M2','M3','M4','RF','XGB']
                y_predicts=[y_predict1, y_predict2, y_predict3, y_predict4, rf_predict, xgb_predict]
  
            ii=0
            for y_predict in y_predicts:
                outfpath=mainpath+'data/predicts_v2/kfold'+str(nth_kfold)+exp+'/pred.'+target+'.'+models[ii]+'_'+str(loc)+'.dat'
                if (models[ii]=='RF')|(models[ii]=='XGB'):
                    test_sc[target+'_yhat']=y_predict
                    test_sc.to_csv(outfpath)

                else:
                    test[target+'_yhat']=y_predict
                    test.to_csv(outfpath)


                ii+=1
        ##
        i+=1

    print("Done.")

##### set parameters #####
meta=load_meta()
target='PM10'
n_kfolds=5
exp='' #with meteo only
######

#######  PM10 predictions ######
print(" *** APPLYING EMPRICAL MODELS AT EACH LOCATION ***")
for nth_kfold in range(n_kfolds):
    pm_estimate(meta.copy(), target=target, n_kfolds=n_kfolds, nth_kfold=nth_kfold, exp=exp)
######

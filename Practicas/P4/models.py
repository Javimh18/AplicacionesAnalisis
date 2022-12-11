import pandas as pd
import numpy as np

from sklearn.metrics import mean_squared_error, mean_absolute_error
import statsmodels.api as sm
import statsmodels.tsa.seasonal as tsa
import statsmodels.graphics.tsaplots as tsaplots
from statsmodels.tsa.stattools import adfuller, kpss

from os.path import isfile

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dropout
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from tensorflow.keras.preprocessing import timeseries_dataset_from_array
from keras.utils import set_random_seed
from statsmodels.tsa.stattools import adfuller, kpss

import warnings
warnings.filterwarnings("ignore")

def adf_test(series, **kw):
    result = adfuller(series, autolag='AIC')
    print(f'ADF Statistic: {result[0]}')
    print(f'n_lags: {result[1]}')
    print(f'p-value: {result[1]}')
    for key, value in result[4].items():
        print('Critial Values:')
        print(f'   {key}, {value}') 
    print(f'Result: The series is {"not " if result[1] > 0.05 else ""}stationary')  


def kpss_test(series, **kw):    
    statistic, p_value, n_lags, critical_values = kpss(series, **kw)
    # Format Output
    print(f'KPSS Statistic: {statistic}')
    print(f'p-value: {p_value}')
    print(f'num lags: {n_lags}')
    print('Critial Values:')
    for key, value in critical_values.items():
        print(f'   {key} : {value}')
    print(f'Result: The series is {"not " if p_value < 0.05 else ""}stationary')


def SARIMAX_train(s, order, n_tr, period=0, seasonal_order=(0,0,0,0), exog=None):
    s_aux = s.copy()
    if (period != 0):
        s_aux = s_aux.diff(periods=period)
    
    if exog is None:
        exogTrain = None
    else:
        exogTrain = exog[:n_tr].to_numpy()
        
    tr_mod = sm.tsa.SARIMAX(s_aux[:n_tr].to_numpy(), exog=exogTrain, 
                            order=order, seasonal_order=seasonal_order, disp=False)
    #The parameter values are estimated using just the training data
    tr_res = tr_mod.fit()

    #Extend the parameters to the whole series
    if exog is None:
        exogExtend = None
    else:
        exogExtend = exog.to_numpy()
        
    res = tr_res.extend(s_aux.to_numpy(), exog=exogExtend)
    
    return res


def SARIMAX_predict(model, s, start, end, horizon=0, period=0):
    if horizon == 0:
        pred = model.predict(start=start, end=end - 1, dynamic=False)
    else:
        pred = []
        for i in range(start, end):
            print('\r\tComputing... (%5d / %5d)' % (i, end), end='')
            pred.append(model.predict(start=i-horizon, end=i, dynamic=True)[horizon])
        pred = np.array(pred)
        print('\r%50s\r' % ' ', end='')
    if (period != 0):
        return pred + s[start - period:end - period].to_numpy()
    else:
        return pred


def errors_by_day(true, pred, MAE=True):
    date_ind = true.index

    if MAE==True:
        maes = [mean_absolute_error(true, pred)]
        return maes
    else: 
        mses = [mean_squared_error(true, pred)]
        return mses


def validate(horizon, s, n_tr, n_va, period=0):
    vec_p = np.arange(10)
    vec_q = np.arange(10)
    
    best_e = np.inf
    
    true = s[n_tr:n_tr + n_va].to_numpy()
    for p in vec_p:
        for q in vec_q:
            try:
                model = SARIMAX_train(s, (p, 0, q), n_tr, period=period)
                pred = SARIMAX_predict(model, s, n_tr, n_tr + n_va, horizon, period=period)
                e = mean_absolute_error(true, pred)
            except Exception as exc:
                e = np.inf
            if (e < best_e):
                best_e = e
                best_p = p
                best_q = q
            
            print('%d %d => %.4f' % (p, q, e))
    
    order = (best_p, 0, best_q)
    print('\tBest:', order)

    return order

def create_dataset(eolic, n_tr, n_va, h=0, batch_size=32):

    y = eolic[["WindEnergy"]][h+1:]
    x = eolic[:-(h+1)]

    x = MinMaxScaler().fit_transform(np.array(x).reshape(-1, 3))

    dataset = timeseries_dataset_from_array(x, y, sequence_length=7, batch_size=batch_size)

    dataset_tr = dataset.take(int((n_tr + n_va) / batch_size))
    dataset_te = dataset.skip(int((n_tr + n_va) / batch_size))
    y_te = np.concatenate([batch[1].numpy() for batch in dataset_te])

    return dataset_tr, dataset_te, y_te






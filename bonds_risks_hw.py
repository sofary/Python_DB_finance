#!/usr/bin/env python
# coding: utf-8

# # Задача 1 
# Посчитать численно $DV01$ как разностную производную.
# 1. Номер выпуска облигации определяет функция getBond ниже 
# 1. Процентные ставки известны ниже curve_tenors, curve_rates
# 1. Использоватье линейнйую интерполяцию кубическими сплайнами (см. пример ниже)

# $$ PV  = PV (r_1, r_2, r_3, ..., r_N) = \sum \limits_{i=1}^{N} \frac{C_i}{(1 + r_i)^{t_i}} $$
# где $r_i$ - значение ставки, $C_i$ - выплата в день купонного платежа под номером $i$
# 
# $$ DV01 (r_1, r_2,  ..., r_N) = \lim \limits_{\delta \to 0} \frac{PV (r_1 + \delta r, r_2 + \delta r, ..., r_N + \delta r) - PV (r_1, r_2,  ..., r_N)}{\delta r}  \approx
# \frac{PV (r_1 + \Delta r, r_2 + \Delta r, ..., r_N + \Delta r) - PV (r_1, r_2,  ..., r_N)}{\Delta r}$$

# In[1]:


def getBond(email):
    ccy = ['53004RMFS', '53003RMFS', '53005RMFS']
    h = hash(email)
    return ccy[h % len(ccy)]
getBond('iamastonelady@gmail.com')


# In[15]:


import numpy as np
import scipy.optimize
import scipy.interpolate
import matplotlib.pyplot as pt
import pandas as pd

curve_tenors = np.array([0.25, 0.5, 0.75, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0, 15.0, 20.0, 30.0])
curve_rates = np.array([4.17,4.21,4.26,4.32,4.59,4.88,5.41,5.83,6.26,6.62,6.79,6.98])*1e-2

f = scipy.interpolate.interp1d(curve_tenors, curve_rates, kind = 'cubic')
f(np.array([10, 20, 30]) / 12) # пример ставки на 10M, 20M, 30M


# In[11]:


#задача 1-


# In[46]:


days = np.array([184, 182, 182, 182, 182, 182])
coupons = np.array([6.50, 7.00, 7.05, 7.10, 7.25, 7.35])
payments = np.array([32.77, 34.90, 35.15, 35.40, 36.15, 1211.02])

days*coupons/payments*10
day_count=365


# In[51]:


days = np.array([184, 182, 182, 182, 182, 182]) 
payments = np.array([32.77, 34.90, 35.15, 35.40, 36.15, 1211.02])

Price = 1.028627*1000 + 20.30 

def pv_ytm(days, payments, ytm):
    days = np.cumsum(days) / 365  # use the right day count
    df = np.power(1.0 / (ytm + 1.0), days)
    return np.sum(payments*df)

ytm = scipy.optimize.broyden1( lambda x: (pv_ytm(days, payments, x) - Price)**2, 0.0)

PV=pv_ytm(days, payments, ytm)


# In[52]:


dv01_num = 0.5*(pv_ytm(days, payments, ytm-1e-4) - pv_ytm(days, payments, ytm+1e-4))
dv01_num


# # Задача 2
# 
# 1. Таблица ниже описывает облигацию, необходимо ее захеджировать [ОФЗ](https://special.minfin.gov.ru/ru/document/?id_4=130822-parametry_obligatsii_federalnogo_zaima_dlya_fizicheskikh_lits_ofz-n_vypuska__53006rmfs) 
# 
# Использовать для расчета $DV01$ [кривую](https://www.moex.com/ru/marketdata/indices/state/g-curve/)
# 
# Чему равна $beta$?
# 
# 
# | Date | Coupon |
# |-------|-----------|
# | 2021-02-24 | 34.9 |
# | 2021-08-25 | 34.9|
# | 2022-02-23 | 34.9|
# | 2022-08-24 | 34.9 |
# | 2023-02-22 | 34.9 |
# | 2023-08-23 | 1034.9|
# 
# 2. Построить график $PV$ портфеля от величины вертикального сдвига кривой $\Delta$
# $$ PV (r; \Delta) = PV (r_1 + \Delta, r_2+ \Delta, r_3+ \Delta, ..., r_N+ \Delta) = \sum \limits_{i=1}^{N} \frac{C_i}{(1 + r_i + \Delta)^{t_i}} $$
# 
# 
# 
# 

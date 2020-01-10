# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 09:49:14 2020

@author: walke
"""

import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib.style as style
import numpy as np
import pandas as pd
import seaborn as sns
import math
style.use('seaborn')
sns.set_style(style='darkgrid')

#S&P500
sp500 = pd.read_csv("C:/Users/walke/Documents/galvanize/capstones/Does-the-Market-move-with-Trump-s-Tweets-/data/s&p500.csv")

sp500 = sp500.dropna()
sp500['trading_day'] = pd.to_datetime(sp500['Date'])
sp500['trading_day'] = sp500['trading_day'].dt.date

inauguration = pd.to_datetime('2017-1-20')
sp500 = sp500[(sp500['trading_day'] >= inauguration)]
sp500 = sp500.iloc[::-1]
sp500 = sp500.reset_index()
sp500 = sp500.drop(columns=['index'])

sp500['percent_change'] = 100*(sp500['Close']-sp500['Open'])/sp500['Open']
sp500['points_change'] = sp500['Close']-sp500['Open']

sp500 = sp500.set_index('trading_day')
sp500 = sp500.drop(columns=['Date'])

weekly_sp500 = sp500.reset_index()
weekly_sp500['trading_week'] = pd.to_datetime(weekly_sp500['trading_day']) - pd.to_timedelta(6, unit='d')
weekly_sp500 = weekly_sp500.groupby(['High', pd.Grouper(key='trading_week', freq='W-MON')])['Low'].max().reset_index().sort_values('trading_week')
weekly_sp500['trading_week'] = weekly_sp500['trading_week'].dt.date

weekly_sp500_highs = weekly_sp500.groupby(["trading_week"]).max()['High'].to_frame()
weekly_sp500_lows = weekly_sp500.groupby(["trading_week"]).min()['Low'].to_frame()

weekly_sp500 = weekly_sp500_highs.join(weekly_sp500_lows)
weekly_sp500['Volatility'] = weekly_sp500['High']-weekly_sp500['Low']


#DOW Industrial Avg
dow = pd.read_csv("C:/Users/walke/Documents/galvanize/capstones/Does-the-Market-move-with-Trump-s-Tweets-/data/dow.csv")

dow = dow.dropna()
dow['trading_day'] = pd.to_datetime(dow['Date'])
dow['trading_day'] = dow['trading_day'].dt.date

dow = dow[(dow['trading_day'] >= inauguration)]
dow = dow.iloc[::-1]
dow = dow.reset_index()
dow = dow.drop(columns=['index'])

dow['percent_change'] = 100*(dow['Close']-dow['Open'])/dow['Open']
dow['points_change'] = dow['Close']-dow['Open']

dow = dow.set_index('trading_day')

#Soybean Futures
soybeans = pd.read_csv("C:/Users/walke/Documents/galvanize/capstones/Does-the-Market-move-with-Trump-s-Tweets-/data/soybean.csv")

soybeans = soybeans.dropna()
soybeans['trading_day'] = pd.to_datetime(soybeans['Date'])
soybeans['trading_day'] = soybeans['trading_day'].dt.date

soybeans = soybeans[(soybeans['trading_day'] >= inauguration)]

soybeans = soybeans.rename(columns={"Price": "Close"})
cols = soybeans.columns.tolist()
cols.pop(1)
cols.insert(4,'Close')
soybeans = soybeans[cols]
soybeans = soybeans.drop(columns=['Change %'])

soybeans['Open'] = soybeans['Open'].str.replace(',','')
soybeans['Open'] = soybeans['Open'].astype(float)
soybeans['High'] = soybeans['High'].str.replace(',','')
soybeans['High'] = soybeans['High'].astype(float)
soybeans['Low'] = soybeans['Low'].str.replace(',','')
soybeans['Low'] = soybeans['Low'].astype(float)
soybeans['Close'] = soybeans['Close'].str.replace(',','')
soybeans['Close'] = soybeans['Close'].astype(float)

soybeans['percent_change'] = 100*(soybeans['Close']-soybeans['Open'])/soybeans['Open']
soybeans['points_change'] = soybeans['Close']-soybeans['Open']

soybeans = soybeans.set_index('trading_day')

soybeans[['Low']].plot(figsize=(15,4))
plt.xlim(pd.to_datetime('01-01-2019'),pd.to_datetime('01-01-2020'))
plt.xlabel('Trading Day')
plt.ylabel('Points')
plt.tight_layout()
plt.savefig('/plots/soybean_lows.png', dpi=640)

weekly_soybeans = soybeans.reset_index()
weekly_soybeans['trading_week'] = pd.to_datetime(weekly_soybeans['trading_day']) - pd.to_timedelta(6, unit='d')
weekly_soybeans = weekly_soybeans.groupby(['High', pd.Grouper(key='trading_week', freq='W-MON')])['Low'].max().reset_index().sort_values('trading_week')
weekly_soybeans['trading_week'] = weekly_soybeans['trading_week'].dt.date

weekly_soybeans_highs = weekly_soybeans.groupby(["trading_week"]).max()['High'].to_frame()
weekly_soybeans_lows = weekly_soybeans.groupby(["trading_week"]).min()['Low'].to_frame()

weekly_soybeans = weekly_soybeans_highs.join(weekly_soybeans_lows)
weekly_soybeans['Volatility'] = weekly_soybeans['High']-weekly_soybeans['Low']

#VIX
vix = pd.read_csv("C:/Users/walke/Documents/galvanize/capstones/Does-the-Market-move-with-Trump-s-Tweets-/data/vix.csv")

vix = vix.dropna()
vix['trading_day'] = pd.to_datetime(vix['Date'])
vix['trading_day'] = vix['trading_day'].dt.date

vix = vix[(vix['trading_day'] >= inauguration)]
vix = vix.iloc[::-1]
vix = vix.reset_index()
vix = vix.drop(columns=['index'])

vix['percent_change'] = 100*(vix['Close']-vix['Open'])/vix['Open']
vix['points_change'] = vix['Close']-vix['Open']

vix = vix.set_index('trading_day')

weekly_vix = vix.reset_index()
weekly_vix['trading_week'] = pd.to_datetime(weekly_vix['trading_day']) - pd.to_timedelta(6, unit='d')
weekly_vix = weekly_vix.groupby(['High', pd.Grouper(key='trading_week', freq='W-MON')])['Low'].max().reset_index().sort_values('trading_week')
weekly_vix['trading_week'] = weekly_vix['trading_week'].dt.date

weekly_vix_highs = weekly_vix.groupby(["trading_week"]).max()['High'].to_frame()
weekly_vix_lows = weekly_vix.groupby(["trading_week"]).min()['Low'].to_frame()

weekly_vix = weekly_vix_highs.join(weekly_vix_lows)
weekly_vix['Volatility'] = weekly_vix['High']-weekly_vix['Low']
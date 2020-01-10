# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 13:50:29 2020

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

from organizing_tweets import day_sums,keyword_counts,day_counts,weekly_keyword_counts
from organizing_financial_data import sp500,weekly_sp500,weekly_soybeans,weekly_vix

sp500_words = day_sums.join(sp500)
sp500_words = sp500_words.dropna()

sp500_tweets_w_words = keyword_counts.join(sp500)
sp500_tweets_w_words = sp500_tweets_w_words.dropna()

corr = sp500_tweets_w_words[['trade_war','fed','impeachment','percent_change','points_change']].corr()
fig10 = plt.figure(10)
ax10 = fig10.add_subplot(111)
ax10=sns.heatmap(corr, 
        xticklabels=corr.columns,
        yticklabels=corr.columns)
ax10.axis('equal')
ax10.set_title('Correlation Heatmap')
plt.tight_layout()
fig10.savefig('/plots/keyword_drop_correlation_heatmap.png', dpi=640)

sp500_tweets = day_counts.join(sp500)
sp500_tweets = sp500_tweets.dropna()

weekly_sp500_tweets_w_words = weekly_keyword_counts.join(weekly_sp500)
weekly_sp500_tweets_w_words = weekly_sp500_tweets_w_words.dropna()

"""corr = weekly_sp500_tweets_w_words[['trade_war','fed','impeachment','Volatility']].corr()
fig11 = plt.figure(11)
ax11 = fig11.add_subplot(111)
ax11=sns.heatmap(corr, 
        xticklabels=corr.columns,
        yticklabels=corr.columns)
ax11.axis('equal')
ax11.set_title('Correlation Heatmap')
plt.tight_layout()"""

weekly_tweets_w_words = weekly_sp500_tweets_w_words
weekly_tweets_w_words = weekly_tweets_w_words.rename(columns={"High":"S&P500 High","Low":"S&P500 Low","Volatility":"S&P500 Volatility"})
weekly_soybeans = weekly_soybeans.rename(columns={"High":"Soybean High","Low":"Soybean Low","Volatility":"Soybean Volatility"})
weekly_tweets_w_words = weekly_tweets_w_words.join(weekly_soybeans)
weekly_vix = weekly_vix.rename(columns={"High":"VIX High","Low":"VIX Low","Volatility":"VIX Volatility"})
weekly_tweets_w_words = weekly_tweets_w_words.join(weekly_vix)

corr = weekly_tweets_w_words[['# of tweets','trade_war_%','fed_%','impeachment_%','S&P500 Volatility','Soybean Volatility','VIX High']].corr()
fig12 = plt.figure(12)
ax12 = fig12.add_subplot(111)
ax12=sns.heatmap(corr, 
        xticklabels=corr.columns,
        yticklabels=corr.columns)
ax12.axis('equal')
ax12.set_title('Correlation Heatmap')
plt.tight_layout()
fig12.savefig('/plots/weekly_keyword_volatility_correlation_heatmap.png', dpi=640)

high_trade_war_weeks = weekly_tweets_w_words.loc[weekly_tweets_w_words['trade_war_%']>0.031250]
low_trade_war_weeks = weekly_tweets_w_words.loc[weekly_tweets_w_words['trade_war_%']<0.031250]
print(stats.mannwhitneyu(high_trade_war_weeks['Soybean Volatility'], low_trade_war_weeks['Soybean Volatility'], alternative="greater"))
print(stats.mannwhitneyu(high_trade_war_weeks['VIX High'], low_trade_war_weeks['VIX High'], alternative="greater"))
print(stats.mannwhitneyu(high_trade_war_weeks['S&P500 Volatility'], low_trade_war_weeks['S&P500 Volatility'], alternative="greater"))

fig,ax = plt.subplots()
sns.distplot(low_trade_war_weeks['Soybean Volatility'],kde=False,norm_hist=True,bins=list(np.linspace(0,90,19)),ax=ax,label='Weeks with low % of tweets mentioning Trade War',hist_kws={"alpha": 0.5, "color": "r"})
sns.distplot(high_trade_war_weeks['Soybean Volatility'],kde=False,norm_hist=True,bins=list(np.linspace(0,90,19)),ax=ax,label='Weeks with high % of tweets mentioning Trade War',hist_kws={"alpha": 0.5, "color": "b"})
ax.legend()
ax.set_title('Soybean Volatility for High vs. Low % of Tweets mentioning Trade War')
ax.set_xlabel('Soybean Volatility')
ax.set_ylabel('Density')
fig.text(.75, .5, 'P Value:0.0008, Reject the Null Hypothesis', ha='center')
plt.tight_layout()
fig.savefig('/plots/Weekly_Soybean_Hypothesis_Test.png', dpi=640)

fig,ax = plt.subplots()
sns.distplot(low_trade_war_weeks['VIX High'],kde=False,norm_hist=True,bins=list(np.linspace(10,55,19)),ax=ax,label='Weeks with low % of tweets mentioning Trade War',hist_kws={"alpha": 0.5, "color": "r"})
sns.distplot(high_trade_war_weeks['VIX High'],kde=False,norm_hist=True,bins=list(np.linspace(10,55,19)),ax=ax,label='Weeks with high % of tweets mentioning Trade War',hist_kws={"alpha": 0.5, "color": "b"})
ax.legend()
ax.set_title('VIX High for High vs. Low % of Tweets mentioning Trade War')
ax.set_xlabel('VIX High')
ax.set_ylabel('Density')
fig.text(.75, .5, 'P Value:0.002, Reject the Null Hypothesis', ha='center')
plt.tight_layout()
fig.savefig('/plots/Weekly_VIX_Hypothesis_Test.png', dpi=640)

fig,ax = plt.subplots()
sns.distplot(low_trade_war_weeks['S&P500 Volatility'],kde=False,norm_hist=True,bins=list(np.linspace(0,240,21)),ax=ax,label='Weeks with low % of tweets mentioning Trade War',hist_kws={"alpha": 0.5, "color": "r"})
sns.distplot(high_trade_war_weeks['S&P500 Volatility'],kde=False,norm_hist=True,bins=list(np.linspace(0,240,21)),ax=ax,label='Weeks with high % of tweets mentioning Trade War',hist_kws={"alpha": 0.5, "color": "b"})
ax.legend()
ax.set_title('S&P500 Volatility for High vs. Low % of Tweets mentioning Trade War')
ax.set_xlabel('S&P500 Volatility')
ax.set_ylabel('Density')
fig.text(.75, .5, 'P Value:0.033, Reject the Null Hypothesis', ha='center')
plt.tight_layout()
fig.savefig('/plots/Weekly_S&P500_Hypothesis_Test.png', dpi=640)

high_fed_weeks = weekly_tweets_w_words.loc[weekly_tweets_w_words['fed_%']>0]
low_fed_weeks = weekly_tweets_w_words.loc[weekly_tweets_w_words['fed_%']==0]
print(stats.mannwhitneyu(high_fed_weeks['VIX High'], low_fed_weeks['VIX High'], alternative="greater"))
print(stats.mannwhitneyu(high_fed_weeks['S&P500 Volatility'], low_fed_weeks['S&P500 Volatility'], alternative="greater"))

fig,ax = plt.subplots()
sns.distplot(low_fed_weeks['VIX High'],kde=False,norm_hist=True,bins=list(np.linspace(10,55,19)),ax=ax,label='Weeks with no tweets mentioning Federal Reserve',hist_kws={"alpha": 0.5, "color": "r"})
sns.distplot(high_fed_weeks['VIX High'],kde=False,norm_hist=True,bins=list(np.linspace(10,55,19)),ax=ax,label='Weeks with tweets mentioning Federal Reserve',hist_kws={"alpha": 0.5, "color": "b"})
ax.legend()
ax.set_title('VIX High for Weeks mentioning Federal Reserve vs. no tweets')
ax.set_xlabel('VIX High')
ax.set_ylabel('Density')
fig.text(.75, .5, 'P Value:0.016, Reject the Null Hypothesis', ha='center')
plt.tight_layout()
fig.savefig('/plots/Fed_Weekly_VIX_Hypothesis_Test.png', dpi=640)

fig,ax = plt.subplots()
sns.distplot(low_fed_weeks['S&P500 Volatility'],kde=False,norm_hist=True,bins=list(np.linspace(0,240,21)),ax=ax,label='Weeks with no tweets mentioning Federal Reserve',hist_kws={"alpha": 0.5, "color": "r"})
sns.distplot(high_fed_weeks['S&P500 Volatility'],kde=False,norm_hist=True,bins=list(np.linspace(0,240,21)),ax=ax,label='Weeks with tweets mentioning Federal Reserve',hist_kws={"alpha": 0.5, "color": "b"})
ax.legend()
ax.set_title('S&P500 Volatility for Weeks mentioning Federal Reserve vs. no tweets')
ax.set_xlabel('S&P500 Volatility')
ax.set_ylabel('Density')
fig.text(.75, .5, 'P Value:0.007, Reject the Null Hypothesis', ha='center')
plt.tight_layout()
fig.savefig('/plots/Fed_Weekly_S&P500_Hypothesis_Test.png', dpi=640)
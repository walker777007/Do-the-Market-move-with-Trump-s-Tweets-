# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 11:18:40 2020

@author: walke
"""

import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib.style as style
import numpy as np
import pandas as pd
import seaborn as sns
import math
from collections import Counter
style.use('seaborn')
sns.set_style(style='darkgrid')

tweets = pd.read_csv("C:/Users/walke/Documents/galvanize/capstones/Does-the-Market-move-with-Trump-s-Tweets-/data/trumptweets.csv", quotechar='"',quoting=3)

tweets = tweets.dropna()

#tweets = tweets.drop(columns=['source','id_str'])
tweets['created_at'] = pd.to_datetime(tweets['created_at'])
tweets['EST'] = tweets['created_at'].dt.tz_localize('UTC').dt.tz_convert('US/Eastern')
tweets['after_close'] = tweets['EST'].dt.hour>16
tweets['weekday'] = tweets['EST'].dt.dayofweek
tweets['trading_day'] = tweets['EST']
tweets.loc[tweets['after_close']==True,'trading_day'] = tweets['trading_day'][tweets['after_close']==True]+pd.Timedelta(days=1)
tweets['trading_day'] = tweets['trading_day'].dt.date

inauguration = pd.to_datetime('2017-1-20')
tweets = tweets[(tweets['trading_day'] >= inauguration)]

#%%
#Time of Presidency
days = tweets['EST'].dt.date
"""days.hist(bins=37,color='indianred')
plt.title("Number of Tweets over Trump's Presidency")
plt.xlabel('Month')
plt.ylabel('Number of Tweets')"""

#%%
#Words
tweets['text'] = tweets['text'].str.lower()
words=tweets['text'].str.split(' ')
word_list =[]
ignore = ['a','','i','the','me','&amp','&amp;','rt','by','they','with','it','is','no','-',
          'in','and','on','will','have','not','be','was','so','to','just','that','who',
          'as','he','this','of','at','for','has','all','my','our','we','are','you','from',
          'do','would','if','an','than','been','or','get','their','should','what','his',
          'there','your','about','when','but']
for x in words:
    word_list.extend(x)

exclamations=0    
for x in word_list:
    exclamations+=x.count('!')
print(exclamations)

for x in word_list:
    x.replace('....','').replace('!','').replace('.','').replace(',','').replace('"','').replace('”','').replace('“','')
word_list = [x for x in word_list if x not in ignore]
counter = Counter(word_list)
frequent_words = {k:v for (k,v) in counter.items() if v > 500}
frequent_words = {k: v for k, v in sorted(frequent_words.items(), key=lambda item: item[1])}

"""plt.bar(frequent_words.keys(), frequent_words.values(), 0.75)
plt.xticks(rotation='vertical')
plt.title('Most Frequently Tweeted Words')
plt.xlabel('Words')
plt.ylabel('Count')
plt.tight_layout()"""

#%%

#tweets['# words'] = tweets['text'].str.split().str.len()
#tweets['tariff'] = tweets['text'].str.count('tariff')
tweets['fed'] = tweets['text'].str.count('fed$|^fed| fed |federal reserve|powell|interest rate|inflation')
tweets['trade_war'] = tweets['text'].str.count('tariff|trade|china| xi |^xi|xi$|nafta')
tweets['impeachment'] = tweets['text'].str.count('impeach|witch')

day_sums = tweets.groupby(["trading_day"]).sum()
day_sums = day_sums[['fed','trade_war','impeachment']]

day_counts = tweets.groupby(["trading_day"]).count()
day_counts = day_counts['text']
day_counts = day_counts.rename("# of tweets")
day_counts = day_counts.to_frame()

fed_counts = tweets[['trading_day','fed']]
fed_counts = fed_counts.set_index('trading_day')
fed_counts = fed_counts[(fed_counts.T != 0).any()]
fed_counts = fed_counts.groupby(["trading_day"]).count()
fed_counts = fed_counts['fed']
fed_counts = fed_counts.to_frame()

trade_war_counts = tweets[['trading_day','trade_war']]
trade_war_counts = trade_war_counts.set_index('trading_day')
trade_war_counts = trade_war_counts[(trade_war_counts.T != 0).any()]
trade_war_counts = trade_war_counts.groupby(["trading_day"]).count()
trade_war_counts = trade_war_counts['trade_war']
trade_war_counts = trade_war_counts.to_frame()

impeach_counts = tweets[['trading_day','impeachment']]
impeach_counts = impeach_counts.set_index('trading_day')
impeach_counts = impeach_counts[(impeach_counts.T != 0).any()]
impeach_counts = impeach_counts.groupby(["trading_day"]).count()
impeach_counts = impeach_counts['impeachment']
impeach_counts = impeach_counts.to_frame()

"""tariff_counts = tweets[['trading_day','tariff']]
tariff_counts = tariff_counts.set_index('trading_day')
tariff_counts = tariff_counts[(tariff_counts.T != 0).any()]
tariff_counts = tariff_counts.groupby(["trading_day"]).count()
tariff_counts = tariff_counts['tariff']
tariff_counts = tariff_counts.to_frame()"""


keyword_counts = fed_counts.join(trade_war_counts,how='outer')
keyword_counts = keyword_counts.join(impeach_counts,how='outer')
#keyword_counts = keyword_counts.join(tariff_counts,how='outer')
keyword_counts = keyword_counts.fillna(0)

keyword_counts[['impeachment','trade_war','fed']].plot(figsize=(15,4))
plt.xlabel('Trading Day')
plt.ylabel('# of Tweets')
plt.tight_layout()
#plt.savefig('C:/Users/walke/Documents/galvanize/capstones/Does-the-Market-move-with-Trump-s-Tweets-/plots/daily_keywords.png', dpi=640)

keyword_counts[['trade_war']].plot(figsize=(15,4),color='g')
plt.xlim(pd.to_datetime('01-01-2019'),pd.to_datetime('01-01-2020'))
plt.title('# of Tweets about Trade War')
plt.xlabel('Trading Day')
plt.ylabel('# of Tweets')
plt.tight_layout()
#plt.savefig('C:/Users/walke/Documents/galvanize/capstones/Does-the-Market-move-with-Trump-s-Tweets-/plots/trade_war_may.png', dpi=640)

#Weekly
weekly_tweets = tweets
weekly_tweets['weekday'] = pd.to_datetime(tweets['trading_day']).dt.dayofweek
weekly_tweets.loc[weekly_tweets['weekday']==5,'trading_day'] = weekly_tweets['trading_day'][weekly_tweets['weekday']==5]+pd.Timedelta(days=2)
weekly_tweets.loc[weekly_tweets['weekday']==6,'trading_day'] = weekly_tweets['trading_day'][weekly_tweets['weekday']==6]+pd.Timedelta(days=1)

weekly_totals = weekly_tweets
weekly_totals['trading_week'] = pd.to_datetime(weekly_totals['trading_day']) - pd.to_timedelta(6, unit='d')
weekly_totals = weekly_totals.groupby(['text', pd.Grouper(key='trading_week', freq='W-MON')]).count().reset_index().sort_values('trading_week')
weekly_totals = weekly_totals.groupby(["trading_week"]).sum()['source']
weekly_totals = weekly_totals.reset_index()
weekly_totals['trading_week'] = weekly_totals['trading_week'].dt.date
weekly_totals = weekly_totals.set_index('trading_week')
weekly_totals = weekly_totals.rename(columns={"source": "# of tweets"})

weekly_fed_counts = weekly_tweets[['trading_day','fed']]
weekly_fed_counts = weekly_fed_counts.set_index('trading_day')
weekly_fed_counts = weekly_fed_counts[(weekly_fed_counts.T != 0).any()]
weekly_fed_counts = weekly_fed_counts.groupby(["trading_day"]).count()
weekly_fed_counts = weekly_fed_counts['fed']
weekly_fed_counts = weekly_fed_counts.to_frame()

weekly_trade_war_counts = weekly_tweets[['trading_day','trade_war']]
weekly_trade_war_counts = weekly_trade_war_counts.set_index('trading_day')
weekly_trade_war_counts = weekly_trade_war_counts[(weekly_trade_war_counts.T != 0).any()]
weekly_trade_war_counts = weekly_trade_war_counts.groupby(["trading_day"]).count()
weekly_trade_war_counts = weekly_trade_war_counts['trade_war']
weekly_trade_war_counts = weekly_trade_war_counts.to_frame()

weekly_impeachment_counts = weekly_tweets[['trading_day','impeachment']]
weekly_impeachment_counts = weekly_impeachment_counts.set_index('trading_day')
weekly_impeachment_counts = weekly_impeachment_counts[(weekly_impeachment_counts.T != 0).any()]
weekly_impeachment_counts = weekly_impeachment_counts.groupby(["trading_day"]).count()
weekly_impeachment_counts = weekly_impeachment_counts['impeachment']
weekly_impeachment_counts = weekly_impeachment_counts.to_frame()

weekly_keyword_counts = weekly_fed_counts.join(weekly_trade_war_counts,how='outer')
weekly_keyword_counts = weekly_keyword_counts.join(weekly_impeachment_counts,how='outer')
weekly_keyword_counts = weekly_keyword_counts.fillna(0)

weekly_keyword_counts = weekly_keyword_counts.reset_index()
weekly_keyword_counts['trading_week'] = pd.to_datetime(weekly_keyword_counts['trading_day']) - pd.to_timedelta(6, unit='d')
weekly_keyword_counts = weekly_keyword_counts.groupby(['fed', pd.Grouper(key='trading_week', freq='W-MON')])['trade_war','impeachment'].sum().reset_index().sort_values('trading_week')
weekly_keyword_counts = weekly_keyword_counts.groupby(['trading_week']).sum()
weekly_keyword_counts = weekly_keyword_counts.reset_index()
weekly_keyword_counts['trading_week'] = weekly_keyword_counts['trading_week'].dt.date
weekly_keyword_counts = weekly_keyword_counts.set_index('trading_week')

weekly_keyword_counts = weekly_totals.join(weekly_keyword_counts)
weekly_keyword_counts = weekly_keyword_counts.fillna(0)
weekly_keyword_counts['trade_war_%'] = weekly_keyword_counts['trade_war']/weekly_keyword_counts['# of tweets']
weekly_keyword_counts['fed_%'] = weekly_keyword_counts['fed']/weekly_keyword_counts['# of tweets']
weekly_keyword_counts['impeachment_%'] = weekly_keyword_counts['impeachment']/weekly_keyword_counts['# of tweets']
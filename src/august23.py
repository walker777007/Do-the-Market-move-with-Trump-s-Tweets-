# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 11:25:34 2020

@author: walke
"""

import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
import matplotlib.style as style
import numpy as np
import pandas as pd
import seaborn as sns
import math
style.use('seaborn')
sns.set_style(style='darkgrid')

sp500data = np.loadtxt("C:/Users/walke/Documents/galvanize/capstone1/sp500august23.csv",delimiter=',')
sp500time = sp500data[:,0]
sp500price = sp500data[:,1]

vixdata = np.loadtxt("C:/Users/walke/Documents/galvanize/capstone1/vixaugust23.csv",delimiter=',')
vixtime = vixdata[:,0]
vixprice = vixdata[:,1]

sp500price = (sp500price - np.min(sp500price))/(np.max(sp500price)-(np.min(sp500price)))
vixprice = (vixprice - np.min(vixprice))/(np.max(vixprice)-(np.min(vixprice)))

text = '....My only question is who\n is our bigger enemy\n Jay Powell or Chairman Xi?'

fig,ax = plt.subplots()
ax.plot(sp500time,sp500price, label='S&P500')
ax.plot(vixtime,vixprice, label='VIX')
ax.set_xlim(10,15)
ax.axvline(10.961,linewidth=1, color='r')
ax.arrow(10.8,0.64,0.125,0,width=0.005,color='k')
props = dict(boxstyle='round', facecolor='skyblue', alpha=0.5)
ax.text(10.1, 0.62, text, fontsize=10,
        verticalalignment='top', bbox=props)
ax.set_title('S&P500 and VIX August 23, 2019')
ax.set_xlabel('Hour (24hr time)')
ax.set_ylabel('Normalized Price')
ax.legend(loc=7)
donald = mpimg.imread("C:/Users/walke/Documents/galvanize/capstone1/donald.jpg")
imagebox = OffsetImage(donald, zoom=0.2)
ab = AnnotationBbox(imagebox, (10.45, 0.7))
ax.add_artist(ab)
plt.draw()
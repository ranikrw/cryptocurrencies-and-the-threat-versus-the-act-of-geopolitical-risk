# Importing libraries
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt

import matplotlib.dates as mdate

import matplotlib.ticker as mtick # For formatting axis with percent

# Importing file(s) with functions
import sys
sys.path.insert(1, 'functions')
sys.path.insert(1, 'data_cryptocurrency')
from functions_data import *
from list_of_CCs_to_download import *

##########################################
## Global parameters                    ##
##########################################
sample_period_min = pd.Timestamp('2022-02-01 01:00:00')
sample_period_max = pd.Timestamp('2022-03-15 00:00:00')

# On 21 February at 22:35 (UTC+3),[233] Putin announced that the Russian 
# government would diplomatically recognize the Donetsk and Luhansk people's 
# republics.
event_time_1 = pd.Timestamp('2022-02-21 22:00:00') - dt.timedelta(hours=3)

# On 24 February 2022, at 5:30 am Moscow Time, state television channels began broadcasting the address of Russian president Vladimir Putin.[1][2]
# https://en.wikipedia.org/wiki/On_conducting_a_special_military_operation
# Moscow time: UTC/GMT +3 hours
# https://www.timeanddate.com/time/zone/russia/moscow
event_time_2 = pd.Timestamp('2022-02-24 05:00:00') - dt.timedelta(hours=3)

##########################################
## Folder for saving results
##########################################
folder_name = 'descriptives'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

##########################################
## load and prepare CC data             ##
##########################################
CCs_to_upload = get_list_of_CCs_to_download()
CCs_to_upload = CCs_to_upload[0:100] 

data_CC_price,data_CC_volume,data_CC_returns,beta,gamma = \
    load_and_prepare_CC_data(CCs_to_upload,sample_period_min,sample_period_max)

##########################################
## Returns and volume plots
##########################################
hour_interval = 24*2
hour_interval = int(hour_interval)
min_time    = (event_time_1 - dt.timedelta(hours=hour_interval)).strftime('%Y-%m-%d %H')
max_time    = (event_time_2 + dt.timedelta(hours=hour_interval)).strftime('%Y-%m-%d %H')

ind = (data_CC_returns.index >= min_time)&(data_CC_returns.index <= max_time)
returns = data_CC_returns[ind]

# Parameters that determine how the plots will look like
fig_width  = 20 # Width of the figure
fig_length = 10 # Length of the figure
linewidth  = 3  # Width of the lines in the plots
fontsize   = 31

date_formatter = mdate.DateFormatter('%d')
locator = mdate.DayLocator()

colors = [
    'royalblue',
    'orangered',
    ]

linestyles = [
    'solid',
    'solid',
    ]

# Returns
fig, ax = plt.subplots(1, 1, figsize=(fig_width,fig_length))
fig.patch.set_facecolor('white')
plt.gca().xaxis.set_major_locator(locator)
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times New Roman"]
legend = []
for i,c,linestyle,lw,alpha in zip([5,100],colors,linestyles,[3,0],[1,1]):
    temp = np.mean(returns.iloc[:,0:i],axis=1)
    ax.plot(temp,c=c,lw=linewidth+lw,linestyle=linestyle,alpha=alpha)
    legend = legend+['Top '+str(i)]
plt.axvline(event_time_1,color='darkviolet',lw=2,linestyle=(5, (10, 3)))
plt.axvline(event_time_2,color='darkviolet',lw=2,linestyle=(5, (10, 3)))
ax.xaxis.set_major_formatter(date_formatter)
ax.set_xlabel('February 2022',fontsize=fontsize)
ax.set_ylabel('Average log returns',fontsize=fontsize)
ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize)
ax.tick_params(axis = 'both', which = 'minor', labelsize = fontsize)
plt.xticks(rotation=0)
ax.set_xlim([returns.index[0].to_pydatetime(),returns.index[-1].to_pydatetime()])
ax.set_xlim([returns.index[0].to_pydatetime(),returns.index[-1].to_pydatetime()])
ax.legend(legend,fontsize=fontsize,framealpha=1)
plt.grid()
# plt.show() # Uncomment to show plot in Kernel
plt.savefig(folder_name+'/Returns_plot.png',dpi=150, bbox_inches='tight')
# plt.close() 

# Cumulative returns
fig, ax = plt.subplots(1, 1, figsize=(fig_width,fig_length))
fig.patch.set_facecolor('white')
plt.gca().xaxis.set_major_locator(locator)
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times New Roman"]
legend = []
for i,c,linestyle,lw,alpha in zip([5,100],colors,linestyles,[3,0],[1,1]):
    ax.plot(np.mean(returns.iloc[:,0:i].cumsum(),axis=1),c=c,lw=linewidth+lw,linestyle=linestyle,alpha=alpha)
    legend = legend+['Top '+str(i)]
plt.axvline(event_time_1,color='darkviolet',lw=2,linestyle=(5, (10, 3)))
plt.axvline(event_time_2,color='darkviolet',lw=2,linestyle=(5, (10, 3)))
ax.xaxis.set_major_formatter(date_formatter)
ax.set_xlabel('February 2022',fontsize=fontsize)
ax.set_ylabel('Cumulative average log returns',fontsize=fontsize)
ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize)
ax.tick_params(axis = 'both', which = 'minor', labelsize = fontsize)
plt.xticks(rotation=0)
ax.set_xlim([returns.index[0].to_pydatetime(),returns.index[-1].to_pydatetime()])
ax.legend(legend,fontsize=fontsize,framealpha=1)
plt.grid()
# plt.show() # Uncomment to show plot in Kernel
plt.savefig(folder_name+'/Returns_plot_cum.png',dpi=150, bbox_inches='tight')
# plt.close() 


# Importing libraries
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdate

# Setting font on plots
import matplotlib
matplotlib.rcParams['font.family'] = "Times New Roman"

# Importing file(s) with functions
import sys
sys.path.insert(1, 'functions')
from functions_data import *
from functions_analysis import *
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


# Parameters that determine how the plots will look like
fig_width  = 20 # Width of the figure
fig_length = 10 # Length of the figure
linewidth  = 2  # Width of the lines in the plots
fontsize   = 31

##########################################
## Folder for saving results
##########################################
folder_name = 'results_liquidity_analysis'
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
## RtoV: Post/Pre ratio
##########################################
window_range = list(np.arange(1,24*2+1))
window_range = list(np.array(window_range, dtype = 'float')) # Convert to float

plot_table = pd.DataFrame()

# Event time 1
num_CCs = 5
results_5 = make_post_pre_ratio(num_CCs,event_time_1,window_range,data_CC_returns,data_CC_volume,beta,gamma)
col_name = make_col_name_plot_table(num_CCs,event_time_1)
plot_table[col_name] = results_5['P/P ratio']
results_5 = formating_ratio_column(results_5)

num_CCs = 100
results_100 = make_post_pre_ratio(num_CCs,event_time_1,window_range,data_CC_returns,data_CC_volume,beta,gamma)
col_name = make_col_name_plot_table(num_CCs,event_time_1)
plot_table[col_name] = results_100['P/P ratio']
results_100 = formating_ratio_column(results_100)

results = pd.concat([results_5,results_100],axis=1)

filename = str(event_time_1)[:-6].replace(' ','-')
results.to_excel(folder_name+'/liquidity_table_'+filename+'.xlsx',index=True)

# Event time 2
num_CCs = 5
results_5 = make_post_pre_ratio(num_CCs,event_time_2,window_range,data_CC_returns,data_CC_volume,beta,gamma)
col_name = make_col_name_plot_table(num_CCs,event_time_2)
plot_table[col_name] = results_5['P/P ratio']
results_5 = formating_ratio_column(results_5)

num_CCs = 100
results_100 = make_post_pre_ratio(num_CCs,event_time_2,window_range,data_CC_returns,data_CC_volume,beta,gamma)
col_name = make_col_name_plot_table(num_CCs,event_time_2)
plot_table[col_name] = results_100['P/P ratio']
results_100 = formating_ratio_column(results_100)

results = pd.concat([results_5,results_100],axis=1)

filename = str(event_time_2)[:-6].replace(' ','-')
results.to_excel(folder_name+'/liquidity_table_'+filename+'.xlsx',index=True)

max_range = np.max(window_range)

plot_table.rename(columns = {
    '21 February 2022 at 7 pm - Top5':'Threat event - Top 5',
    '21 February 2022 at 7 pm - Top100':'Threat event - Top 100',
    '24 February 2022 at 2 am - Top5':'Act event - Top 5',
    '24 February 2022 at 2 am - Top100':'Act event - Top 100',
    }, inplace = True)

colors = [
    'royalblue',
    'orangered',
    'forestgreen',
    'darkviolet',
    ]

linestyles = [
    'solid',
    'solid',
    'solid',
    'solid',
    ]

fig, ax = plt.subplots(1, 1, figsize=(fig_width,fig_length))
fig.patch.set_facecolor('white')
for c,linestyle,i,lw in zip(colors,linestyles,plot_table,[2,0,2,0]):
    ax.plot(window_range,plot_table[i],c=c,lw=linewidth+lw,linestyle=linestyle)
plt.axvline(2*24+17,color='black',lw=linewidth,linestyle='dashed') # Event 2 for event 1
ax.set_xlabel('Hours posterior and prior',fontsize=fontsize)
ax.set_ylabel('P/P ratio',fontsize=fontsize)
ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize)
ax.tick_params(axis = 'both', which = 'minor', labelsize = fontsize)
plt.xticks(rotation=0)
ax.set_xlim((0, max_range))
ax.legend(list(plot_table.columns),fontsize=fontsize,framealpha=1)
plt.grid()
# plt.show() # Uncomment to show plot in Kernel
plt.savefig(folder_name+'/Post_Pre_ratio_plot.png',dpi=150, bbox_inches='tight')
# plt.close()


##########################################
## S plot    
##########################################
hour_interval = 24*2
hour_interval = int(hour_interval)
min_time    = (event_time_1 - dt.timedelta(hours=hour_interval)).strftime('%Y-%m-%d %H')
max_time    = (event_time_2 + dt.timedelta(hours=hour_interval)).strftime('%Y-%m-%d %H')

date_formatter = mdate.DateFormatter('%d')
locator = mdate.DayLocator()

colors = [
    'royalblue',
    'orangered',
    ]

linewidth  = 3  # Width of the lines in the plots

fig, ax = plt.subplots(1, 1, figsize=(fig_width,fig_length))
fig.patch.set_facecolor('white')
plt.gca().xaxis.set_major_locator(locator)
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times New Roman"]
legend = []
for num_CCs,c,lw in zip([5,100],colors,[3,0]):
    temp = make_S_values(num_CCs,min_time,max_time,beta,gamma)
    ax.plot(temp,c=c,lw=linewidth+lw,linestyle=linestyle)
    legend = legend+['Top '+str(num_CCs)]
plt.axvline(event_time_1,color='darkviolet',lw=2,linestyle=(5, (10, 3)))
plt.axvline(event_time_2,color='darkviolet',lw=2,linestyle=(5, (10, 3)))
ax.xaxis.set_major_formatter(date_formatter)
ax.set_xlabel('February 2022',fontsize=fontsize)
ax.set_ylabel('Bid-ask spread estimator, S',fontsize=fontsize)
ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize)
ax.tick_params(axis = 'both', which = 'minor', labelsize = fontsize)
plt.xticks(rotation=0)
ax.set_xlim([temp.index[0].to_pydatetime(),temp.index[-1].to_pydatetime()])
ax.legend(legend,fontsize=fontsize,framealpha=1)
plt.grid()
# plt.show() # Uncomment to show plot in Kernel
plt.savefig(folder_name+'/S_plot.png',dpi=150, bbox_inches='tight')
# plt.close() 


# Importing libraries
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt

import matplotlib.ticker as mtick # For formatting axis with percent

# Setting font on plots
import matplotlib
matplotlib.rcParams['font.family'] = "Times New Roman"

# Importing file(s) with functions
import sys
sys.path.insert(1, 'functions')
sys.path.insert(1, 'data_cryptocurrency')
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
folder_name = 'results_analysis_event'
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
## Make results
##########################################
dict_parameters = {}

dict_parameters['training_period_end'] = 36 # Hours for where to end the training period
dict_parameters['training_period_length'] = 30*24 # Hours

temp = dict_parameters['training_period_end']
dict_parameters['CAR_interval'] = [-temp,temp]

CAR_plot = pd.DataFrame()

AR_table = pd.DataFrame()
CAR_table = pd.DataFrame()

# Event time 1
dict_parameters['event_time'] = event_time_1
dict_parameters['num_CCs'] = 5
CAR_plot,AR_table,CAR_table = make_CAR_column(CAR_plot,AR_table,CAR_table,data_CC_returns,dict_parameters)
dict_parameters['num_CCs'] = 100
CAR_plot,AR_table,CAR_table = make_CAR_column(CAR_plot,AR_table,CAR_table,data_CC_returns,dict_parameters)

# Event time 2
dict_parameters['event_time'] = event_time_2
dict_parameters['num_CCs'] = 5
CAR_plot,AR_table,CAR_table = make_CAR_column(CAR_plot,AR_table,CAR_table,data_CC_returns,dict_parameters)
dict_parameters['num_CCs'] = 100
CAR_plot,AR_table,CAR_table = make_CAR_column(CAR_plot,AR_table,CAR_table,data_CC_returns,dict_parameters)


# Save tables
AR_table.to_excel(folder_name+'/AR.xlsx')
CAR_table.to_excel(folder_name+'/CAR.xlsx')

##########################################
## MAking plot
##########################################
hour_window = 36

CAR_plot_plot = CAR_plot.loc[-hour_window:hour_window]

CAR_plot_plot.rename(columns = {
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
for c,linestyle,i,lw in zip(colors,linestyles,CAR_plot_plot.columns,[2,0,2,0]):
    ax.plot(CAR_plot_plot[i],c=c,lw=linewidth+lw,linestyle=linestyle)
plt.axvline(0,color='black',lw=2,linestyle='dashed')
plt.axhline(0,color='black',lw=2,linestyle='-')
# ax.set_xlabel('Hour',fontsize=fontsize)
ax.set_ylabel('Cumulative abnormal return (CAR)',fontsize=fontsize)
ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize)
ax.tick_params(axis = 'both', which = 'minor', labelsize = fontsize)
plt.xticks(rotation=0)
ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax.set_xlim((-hour_window, hour_window))
ax.legend(list(CAR_plot_plot.columns),fontsize=fontsize,framealpha=0)
# plt.grid()
# plt.show() # Uncomment to show plot in Kernel
plt.savefig(folder_name+'/CAR_plot.png',dpi=150, bbox_inches='tight')
# plt.close()
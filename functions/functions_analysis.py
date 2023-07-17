import pandas as pd
import numpy as np

import datetime as dt
from statsmodels.stats import weightstats

from scipy.stats import t

def make_S(beta,gamma):
    num = 3-(2*np.sqrt(2))

    term1 = np.sqrt(2*beta.astype(float)) - np.sqrt(beta.astype(float))
    term1 = term1/num

    term2 = np.sqrt(gamma/num)

    alpha = term1+term2

    return 2*(np.exp(alpha)-1) / (1+np.exp(alpha))

def make_CAR_column(CAR_plot,AR_table,CAR_table,data_CC_returns,dict_parameters):

    training_period_end     = dict_parameters['training_period_end']
    training_period_length  = dict_parameters['training_period_length']
    CAR_interval            = dict_parameters['CAR_interval']
    event_time              = dict_parameters['event_time']
    num_CCs                 = dict_parameters['num_CCs']

    col_name = make_col_name_plot_table(num_CCs,event_time)

    data = data_CC_returns.iloc[:,0:num_CCs].copy()

    # Expected returns 
    temp_start  = (event_time - dt.timedelta(hours=training_period_end+training_period_length)).strftime('%Y-%m-%d %H')
    temp_end    = (event_time - dt.timedelta(hours=training_period_end)).strftime('%Y-%m-%d %H')

    ind = (data.index > temp_start)&(data.index <= temp_end)
    data_training = data[ind]

    ER = np.mean(data[ind],axis=0)

    ############################
    ## CAR plot
    ############################
    # Abnormal returns
    AR = pd.DataFrame(index=data.index)
    for i in data.columns:
        AR[i] = data[i] - ER[i]
    AR = np.mean(AR,axis=1)

    # CAR plot
    temp_start  = (event_time + dt.timedelta(hours=CAR_interval[0])).strftime('%Y-%m-%d %H')
    temp_end    = (event_time + dt.timedelta(hours=CAR_interval[1])).strftime('%Y-%m-%d %H')

    ind = (AR.index >= temp_start)&(AR.index <= temp_end)
    temp = AR[ind].cumsum()
    temp.index = range(CAR_interval[0],CAR_interval[1]+1)
    CAR_plot[col_name] = temp

    ############################
    ## AR and CAR tables
    ############################
    # Making windows
    event_window_before = []
    event_window_after = []
    event_window_symmetric = []
    for i in range(1,CAR_interval[1]+1):
        event_window_before.append([-i,0])
        event_window_after.append([0,i])
        event_window_symmetric.append([-i,i])
    event_window_before.reverse()
    event_windows = event_window_before+event_window_after+event_window_symmetric

    # Create data frame for CAR
    CAR_df = pd.DataFrame()
    for i in event_windows:
        temp = pd.DataFrame()
        temp['Begin']   = [i[0]]
        temp['End']     = [i[1]]
        temp['Event Windows'] = ['['+str(i[0])+','+str(i[1])+']']
        CAR_df = pd.concat([CAR_df,temp],axis=0)
    CAR_df = CAR_df.reset_index(drop=True)

    # Create data frame for AR
    AR_df = pd.DataFrame(index=np.arange(CAR_interval[0],CAR_interval[1]+1))

    # Create data frame for standard deviation of daily abnormal returns
    std_AR_df = pd.Series(index=data.columns,dtype=float)

    # Define index of event date
    event_date_ind = data.index.get_loc(event_time)

    # Compute AR and CAR for each CC
    for CC in data.columns:
        R = data[CC]

        # AR
        temp_start  = (event_time + dt.timedelta(hours=CAR_interval[0])).strftime('%Y-%m-%d %H')
        temp_end    = (event_time + dt.timedelta(hours=CAR_interval[1])).strftime('%Y-%m-%d %H')
        ind = (AR.index >= temp_start)&(AR.index <= temp_end)
        AR_df[CC] = pd.Series(list(R[ind] - ER[CC]),index=AR_df.index)

        # standard deviation of AR across training sample
        temp_AR = data_training[CC] - ER[CC]
        num = np.sum((temp_AR-np.mean(temp_AR))**2)
        std_AR_df[CC] = np.sqrt(num/len(temp_AR))

        # CAR
        CAR_df[CC] = pd.Series([None]*CAR_df.shape[0])
        for i in CAR_df.index:
            Begin   = CAR_df.loc[i]['Begin']
            End     = CAR_df.loc[i]['End']
            event_window_beginning = event_date_ind+Begin
            event_window_end = event_date_ind+End+1
            data_temp = pd.DataFrame(data.iloc[event_window_beginning:event_window_end][CC])
            data_temp.index = np.arange(Begin,End+1)
            CAR_df.at[i,CC] = np.sum(data_temp - ER[CC]).values[0]

    #######################################
    ## Orginizing CAR data frame
    #######################################
    CAR_date_dif = CAR_df['End']-CAR_df['Begin'] # Need for t-value
    CAR_df.index = list(CAR_df['Event Windows'])
    CAR_df = CAR_df[data.columns]

    #######################################
    ## Make final data frame
    #######################################
    # aggregate estimation period standard deviation
    num     = np.sum(std_AR_df**2)
    denum   = std_AR_df.shape[0]**2
    std_AR_aggr = np.sqrt(num/denum)

    # Making data frames for results
    AR_table_col = pd.DataFrame()
    CAR_table_col = pd.DataFrame()

    # Average values
    AR_table_col[col_name]     = np.mean(AR_df,axis=1)
    CAR_table_col[col_name]   = np.mean(CAR_df,axis=1)

    # t-values
    AR_table_col['t-test'] = AR_table_col[col_name]/std_AR_aggr

    num_days_event_window = pd.Series(list(np.abs(CAR_date_dif)),index=CAR_table_col.index)
    num_days_event_window = np.sqrt(num_days_event_window+1)
    CAR_table_col['t-test'] = CAR_table_col[col_name]/(std_AR_aggr*num_days_event_window)

    # p values
    AR_table_col     = add_p_values(AR_table_col)
    CAR_table_col    = add_p_values(CAR_table_col)
    
    # Round coefficient values
    AR_table_col = round_coefficient(AR_table_col,col_name)
    CAR_table_col = round_coefficient(CAR_table_col,col_name)

    # Merging with final data frame
    AR_table    = pd.concat([AR_table,AR_table_col],axis=1)
    CAR_table   = pd.concat([CAR_table,CAR_table_col],axis=1)

    return CAR_plot,AR_table,CAR_table

def round_coefficient(index_df,col_name):
    for i in index_df.index:
        temp = str(np.round(index_df.at[i,col_name],2))
        if temp[-2]=='.':
            temp = temp + '0'
        index_df.at[i,col_name] = temp
    return index_df

def add_p_values(index_df):
    pvalues = t.sf(abs(index_df['t-test']), df=(index_df.shape[0]-1))*2 # Two-sided
    pvalues = pd.Series(pvalues,index=index_df.index)
    for i in index_df.index:
        temp_val = str(np.round(index_df['t-test'].loc[i],2))
        if temp_val[-2]=='.':
            temp_val = temp_val + '0'
        if pvalues.loc[i]<0.01:
            index_df['t-test'].loc[i] = temp_val+'***'
        elif pvalues.loc[i]<0.05:
            index_df['t-test'].loc[i] = temp_val+'**'
        elif pvalues.loc[i]<0.10:
            index_df['t-test'].loc[i] = temp_val+'*'
        else:
            index_df['t-test'].loc[i] = temp_val
    return index_df

def make_col_name_plot_table(num_CCs,event_time):
    day = event_time.strftime("%d")
    month = event_time.strftime("%B")
    year = event_time.strftime("%Y")
    hour = event_time.strftime("%I %p").lower()
    if hour[0]=='0':
        hour = hour[1:] # Remove the first zero
    return '{} {} {} at {} - Top{}'.format(day,month,year,hour,str(num_CCs))

def make_post_pre_ratio(num_CCs,event_time,window_range,data_CC_returns,data_CC_volume,beta,gamma):
    results = pd.DataFrame([[None,None,None]]*len(window_range))
    for hour,i in zip(window_range,range(len(window_range))):

        min_time    = (event_time - dt.timedelta(hours=hour)).strftime('%Y-%m-%d %H')
        max_time    = (event_time + dt.timedelta(hours=hour)).strftime('%Y-%m-%d %H')

        ##########################################
        ## POST
        ##########################################
        ind = (beta.index <= max_time)&(beta.index > event_time.strftime('%Y-%m-%d %H:%M:%S'))
        beta_post = beta.iloc[:, 0:num_CCs][ind]

        ind = (gamma.index <= max_time)&(gamma.index > event_time.strftime('%Y-%m-%d %H:%M:%S'))
        gamma_post = gamma.iloc[:, 0:num_CCs][ind]

        post = make_S(beta_post,gamma_post)
        post = np.sum(post,axis=0)

        ##########################################
        ## PRE
        ##########################################
        ind = (beta.index >= min_time)&(beta.index < event_time.strftime('%Y-%m-%d %H:%M:%S'))
        beta_pre = beta.iloc[:, 0:num_CCs][ind]

        ind = (gamma.index >= min_time)&(gamma.index < event_time.strftime('%Y-%m-%d %H:%M:%S'))
        gamma_pre = gamma.iloc[:, 0:num_CCs][ind]

        pre = make_S(beta_pre,gamma_pre)
        pre = np.sum(pre,axis=0)

        for CC in pre.index:
            if pre[CC]==0:
                print('Hour: {} for Top{}: {} is zero for pre, so removing this token'.format(hour,num_CCs,CC))
                del post[CC]
                del pre[CC]

        ##########################################
        ## Ratio                                ##
        ##########################################
        series = make_series_LIQ(post,pre)

        # Add hours description
        temp = pd.Series(['(-'+str(int(hour))+',+'+str(int(hour))+')'],index=['Event Window (hours)'])
        series = pd.concat([temp,series])

        results.iloc[i] = series

    results.columns = list(series.index)

    results.index = results['Event Window (hours)']
    del results['Event Window (hours)']

    return results

def make_series_LIQ(post,pre):
    ratio = post/pre

    # One sample t-test
    # Description: https://www.statsmodels.org/dev/generated/statsmodels.stats.weightstats.DescrStatsW.ttest_mean.html#statsmodels.stats.weightstats.DescrStatsW.ttest_mean
    # Alternative code: https://www.statology.org/one-sample-t-test-python/
    tstat = weightstats.DescrStatsW(ratio).ttest_mean(1,alternative='two-sided')[0]
    pvalue = weightstats.DescrStatsW(ratio).ttest_mean(1,alternative='two-sided')[1]

    series = pd.Series(dtype=float)
    series['P/P ratio'] = np.mean(ratio)
    series['T-test'] = str(np.round(tstat,2))

    # Adding zero for last digit where missing
    if series['T-test'][-2]=='.':
        series['T-test']=series['T-test']+'0'

    if pvalue<0.01:
        series['T-test'] = series['T-test']+'***'
    elif pvalue<0.05:
        series['T-test'] = series['T-test']+'**'
    elif pvalue<0.10:
        series['T-test'] = series['T-test']+'*'

    return series

def make_S_values(num_CCs,min_time,max_time,beta,gamma):

    ind = (beta.index >= min_time)&(beta.index <= max_time)
    beta_interval = beta.iloc[:, 0:num_CCs][ind]

    ind = (gamma.index >= min_time)&(gamma.index <= max_time)
    gamma_interval = gamma.iloc[:, 0:num_CCs][ind]

    S_values = make_S(beta_interval,gamma_interval)

    S_values = np.mean(S_values,1)

    return S_values
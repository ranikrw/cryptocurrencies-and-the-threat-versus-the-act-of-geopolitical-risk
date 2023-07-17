# Importing libraries
import pandas as pd
import numpy as np
import datetime as dt

# Converting to log returns
def make_log_returns(data,instrument_to_make_log_return):
    log_returns = pd.Series([None]*data.shape[0],name=instrument_to_make_log_return,dtype=float,index=data.index)
    for i in range(1,data.shape[0]):
        log_returns.iloc[i] = 100*np.log(data[instrument_to_make_log_return].iloc[i]/data[instrument_to_make_log_return].iloc[i-1])
    data[instrument_to_make_log_return] = log_returns
    return data

def formating_ratio_column(results):
    for i in range(results.shape[0]):
        temp = str(np.round(results.iloc[i,0],2))
        if temp[-2]=='.':
            temp=temp+'0'
        results.iloc[i,0]=temp
    return results

def load_and_prepare_CC_data(CCs_to_upload,sample_period_min,sample_period_max):

    data_CC_price_all   = pd.DataFrame()
    data_CC_volume_all  = pd.DataFrame()
    data_CC_high_all  = pd.DataFrame()
    data_CC_low_all  = pd.DataFrame()
    i = 0
    for num_uploaded,CC_to_upload in zip(range(len(CCs_to_upload)),CCs_to_upload):
        # Loading data from one CC
        data_loaded = pd.read_csv('../data_CCs/'+CC_to_upload+'.csv',sep=';',index_col='Open time')

        # Removing index name
        data_loaded.index.name = None 

        # Extracting only variables of interest
        data_close  = data_loaded['Close']
        data_volume = data_loaded['Quote asset volume']
        data_high   = data_loaded['High']
        data_low    = data_loaded['Low']

        # Renaming to the name of the CC
        data_close.name = CC_to_upload
        data_volume.name = CC_to_upload
        data_high.name = CC_to_upload
        data_low.name = CC_to_upload

        # Merging with data of all CCs
        data_CC_price_all   = pd.concat([data_CC_price_all,data_close],axis=1) 
        data_CC_volume_all  = pd.concat([data_CC_volume_all,data_volume],axis=1) 
        data_CC_high_all  = pd.concat([data_CC_high_all,data_high],axis=1)
        data_CC_low_all  = pd.concat([data_CC_low_all,data_low],axis=1)

        i+=1
        if i==10:
            print('Uploaded {}/{} CCs'.format(num_uploaded+1,len(CCs_to_upload)))
            i=0
    print('Done uploading CCs')

    # Convert format of index
    date_fmt = '%Y-%m-%d %H:%M:%S'
    data_CC_price_all.index = [dt.datetime.strptime(str(i), date_fmt) for i in data_CC_price_all.index]
    data_CC_volume_all.index = [dt.datetime.strptime(str(i), date_fmt) for i in data_CC_volume_all.index]
    data_CC_high_all.index = [dt.datetime.strptime(str(i), date_fmt) for i in data_CC_high_all.index]
    data_CC_low_all.index = [dt.datetime.strptime(str(i), date_fmt) for i in data_CC_low_all.index]

    ##########################################
    ## Defining sample period
    ##########################################
    data_CC_price   = defining_sample_period(data_CC_price_all,sample_period_max,sample_period_min)
    data_CC_volume  = defining_sample_period(data_CC_volume_all,sample_period_max,sample_period_min)
    data_CC_high    = defining_sample_period(data_CC_high_all,sample_period_max,sample_period_min)
    data_CC_low     = defining_sample_period(data_CC_low_all,sample_period_max,sample_period_min)

    ##########################################
    ## Fill NaN values using an             ##
    ## interpolation method                 ##
    ##########################################
    # No interpolation needed in the article. Thus, the
    # code is commented out here

    # if np.sum(np.sum(pd.isnull(data_CC_price)))!=0:
    #     print('interpolating price')
    #     data_CC_price   = interpolate_rrw(data_CC_price)
    # if np.sum(np.sum(pd.isnull(data_CC_volume)))!=0:
    #     print('interpolating volume')
    #     data_CC_volume  = interpolate_rrw(data_CC_volume)
    # if np.sum(np.sum(pd.isnull(data_CC_high)))!=0:
    #     print('interpolating high')
    #     data_CC_high  = interpolate_rrw(data_CC_high)
    # if np.sum(np.sum(pd.isnull(data_CC_low)))!=0:
    #     print('interpolating low')
    #     data_CC_low  = interpolate_rrw(data_CC_low)

    ##########################################
    ## Making LOG returns
    ##########################################
    data_CC_returns = data_CC_price.copy()
    for CC in data_CC_returns.columns:
        data_CC_returns = make_log_returns(data_CC_returns,CC)

    ##########################################
    ## Making high_high and low_low
    ##########################################
    data_CC_high_high = pd.DataFrame(columns=data_CC_high.columns,index=data_CC_high.index)
    for CC in data_CC_high_high.columns:
        for i in range(1,data_CC_high_high.shape[0]):
            data_CC_high_high[CC].iloc[i] = np.max([data_CC_high[CC].iloc[i],data_CC_high[CC].iloc[i-1]])

    data_CC_low_low = pd.DataFrame(columns=data_CC_low.columns,index=data_CC_low.index)
    for CC in data_CC_low_low.columns:
        for i in range(1,data_CC_low_low.shape[0]):
            data_CC_low_low[CC].iloc[i] = np.min([data_CC_low[CC].iloc[i],data_CC_low[CC].iloc[i-1]])

    ##########################################
    ## beta
    ##########################################
    beta = pd.DataFrame(columns=data_CC_high.columns,index=data_CC_high.index)
    for CC in beta.columns:
        for i in range(1,beta.shape[0]-1):
            temp1 = np.log(data_CC_high[CC].iloc[i]/data_CC_low[CC].iloc[i])**2
            temp2 = np.log(data_CC_high[CC].iloc[i+1]/data_CC_low[CC].iloc[i+1])**2
            beta[CC].iloc[i] = temp1+temp2

    ##########################################
    ## Remove first and last observation
    ##########################################
    # Remove first row
    data_CC_price       = data_CC_price.iloc[1:] 
    data_CC_volume      = data_CC_volume.iloc[1:]
    data_CC_returns     = data_CC_returns.iloc[1:]
    data_CC_high        = data_CC_high.iloc[1:]
    data_CC_low         = data_CC_low.iloc[1:]
    data_CC_high_high   = data_CC_high_high.iloc[1:]
    data_CC_low_low     = data_CC_low_low.iloc[1:]
    beta                = beta.iloc[1:]

    # Remove last row
    data_CC_price       = data_CC_price.iloc[:-1] 
    data_CC_volume      = data_CC_volume.iloc[:-1]
    data_CC_returns     = data_CC_returns.iloc[:-1]
    data_CC_high        = data_CC_high.iloc[:-1]
    data_CC_low         = data_CC_low.iloc[:-1]
    data_CC_high_high   = data_CC_high_high.iloc[:-1]
    data_CC_low_low     = data_CC_low_low.iloc[:-1]
    beta                = beta.iloc[:-1]

    ##########################################
    ## gamma
    ##########################################
    gamma = np.log((data_CC_high_high/data_CC_low_low).astype(float))**2

    ##########################################
    ## Checking data
    ## Returns no text if all is ok
    ##########################################
    if np.sum(np.sum(pd.isnull(data_CC_price)))!=0:
        print('ERROR in Interpolating')
    if np.sum(np.sum(pd.isnull(data_CC_volume)))!=0:
        print('ERROR in Interpolating')
    if np.sum(np.sum(pd.isnull(data_CC_returns)))!=0:
        print('ERROR in Interpolating')
    if np.sum(np.sum(pd.isnull(data_CC_high)))!=0:
        print('ERROR in Interpolating')
    if np.sum(np.sum(pd.isnull(data_CC_low)))!=0:
        print('ERROR in Interpolating')
    if np.sum(np.sum(pd.isnull(data_CC_high_high)))!=0:
        print('ERROR in Interpolating')
    if np.sum(np.sum(pd.isnull(data_CC_low_low)))!=0:
        print('ERROR in Interpolating')
    if np.sum(np.sum(pd.isnull(beta)))!=0:
        print('ERROR in Interpolating')
    if np.sum(np.sum(pd.isnull(gamma)))!=0:
        print('ERROR in Interpolating')

    if data_CC_price.shape != data_CC_volume.shape:
        print('ERROR in data')
    if data_CC_price.shape != data_CC_returns.shape:
        print('ERROR in data')
    if data_CC_price.shape != data_CC_high.shape:
        print('ERROR in data')
    if data_CC_price.shape != data_CC_low.shape:
        print('ERROR in data')
    if data_CC_price.shape != data_CC_high_high.shape:
        print('ERROR in data')
    if data_CC_price.shape != data_CC_low_low.shape:
        print('ERROR in data')
    if data_CC_price.shape != beta.shape:
        print('ERROR in data')
    if data_CC_price.shape != gamma.shape:
        print('ERROR in data')

    return data_CC_price,data_CC_volume,data_CC_returns,beta,gamma

def defining_sample_period(data,sample_period_max,sample_period_min):
    min_one_previous    = (sample_period_min - dt.timedelta(hours=1))
    max_one_subsequent  = (sample_period_max + dt.timedelta(hours=1))
    ind = (data.index <= max_one_subsequent)
    ind = ind & (data.index >= min_one_previous)
    return data[ind]

# No interpolation needed in the article. Thus, the
# code is commented out here
#
# def interpolate_rrw(data):
#     ind = np.sum(pd.isnull(data))
#     for CC in list(ind[ind!=0].index):
#         temp_num = np.sum(pd.isnull(data[CC]))
#         temp_pst = np.round(100*temp_num/data.shape[0],2)
#         print('Interpolating {} observations, or {} percent, of {}'.format(temp_num,temp_pst,CC))
#         temp = data[CC].copy()
#         data[CC] = data[CC].interpolate('time').copy()
#     if np.sum(np.sum(pd.isnull(data)))!=0:
#         print('ERROR in Interpolating')
#     return data

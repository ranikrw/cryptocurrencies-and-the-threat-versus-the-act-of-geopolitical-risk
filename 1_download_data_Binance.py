import numpy as np
import pandas as pd
import os
import zipfile # For unzipping files
import shutil # For removing folders

# Importing file(s) with functions
import sys
sys.path.insert(1, 'functions')
from download_kline import *
from list_of_CCs_to_download import *

# For details about the Binance API, see:
# https://github.com/binance/binance-public-data

CCs_to_download = get_list_of_CCs_to_download()

trading_type = 'spot'
num_symbols = 1 #len(symbols)
intervals = ['1h']
start_date = date(2022, 1, 1).strftime('%Y-%m-%d')
end_date = date(2022, 3, 31).strftime('%Y-%m-%d')
folder = ''
checksum = 0

# Defining and making folder for saving data
folder_to_save = '../data_CCs'
if not os.path.exists(folder_to_save):
    os.makedirs(folder_to_save)

for symbol in CCs_to_download:
    
    symbols = [symbol]
    
    period = convert_to_date_object(end_date) - convert_to_date_object(start_date)
    dates = pd.date_range(end=end_date, periods=period.days + 1).to_pydatetime().tolist()
    dates = [date.strftime("%Y-%m-%d") for date in dates]

    # Downloading data as .zip-files
    data = download_daily_klines(
        trading_type=trading_type,
        symbols=symbols,
        num_symbols=num_symbols,
        intervals=intervals,
        dates=dates,
        start_date=start_date,
        end_date=end_date,
        folder=folder,
        checksum=checksum)
    print('\n###############################') 
    print('Done downloading zipped files')
    print('###############################') 

    # Unzipping all files
    folder_name = 'functions/data/'+trading_type+'/daily/klines/'\
        +symbols[0]+'/'+intervals[0]+'/'\
        +start_date+'_'+end_date
    file_names = os.listdir(folder_name)
    for file_name in file_names:
        zip_file = folder_name+'/'+file_name
        try:
            with zipfile.ZipFile(zip_file) as z:
                z.extractall('functions/data_downloaded')
                print("Extracted all")
        except:
            print("Invalid file")

    # Reading data from all unzipped files
    folder_name = 'functions/data_downloaded'
    file_names = os.listdir(folder_name)
    col_names = [
        'Open time',
        'Open',
        'High',
        'Low',
        'Close',
        'Volume',
        'Close time',
        'Quote asset volume',
        'Number of trades',
        'Taker buy base asset volume',
        'Taker buy quote asset volume',
        'Ignore',
    ]
    data = pd.DataFrame(columns=col_names)
    for file_name in file_names:
        # Loading file
        data_loaded = pd.read_csv(folder_name+'/'+file_name,sep=',',low_memory=False,header=None)
        data_loaded.columns=col_names

        # Merging all data together into object data
        data = pd.concat([data,data_loaded],axis=0)

    # Convert Unix time to date
    data['Open time'] = pd.to_datetime(data['Open time']/1000, unit='s')
    data['Close time'] = pd.to_datetime(data['Close time']/1000, unit='s')

    # Remove folders
    shutil.rmtree('functions/data')
    shutil.rmtree('functions/data_downloaded')

    # Save data
    data.to_csv(folder_to_save+'/'+symbol+'.csv',index=False,sep=';')

    print('\n###############################') 
    print('Done with '+symbol)
    print('###############################') 

print('\n\n###############################') 
print('Done downloading all cryptos')
print('###############################') 
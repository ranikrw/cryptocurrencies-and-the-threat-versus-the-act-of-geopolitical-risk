import numpy as np
import pandas as pd

def get_list_of_CCs_to_download():

    # The list of cryptocurrencies (CCs) is sorted 
    # descending based on their market capitalization

    CCs_to_download = [
        'BTCUSDT', # BitCoin
        'ETHUSDT', # Ethereum
        'BNBUSDT', # BNB
        'ADAUSDT', # Cardano
        'XRPUSDT', # Ripple
        'SOLUSDT', 
        'DOGEUSDT', 
        'DOTUSDT', 
        'SHIBUSDT', # Time series start in May 2021
        'AVAXUSDT', 
        'UNIUSDT', 
        'TRXUSDT', 
        'ETCUSDT', 
        'LTCUSDT', 
        'NEARUSDT', 
        'FTTUSDT', 
        'LINKUSDT', 
        'ATOMUSDT', 
        'XLMUSDT', 
        'XMRUSDT', 
        'FLOWUSDT',  # Time series start on 30 July 2021
        'BCHUSDT', 
        'ALGOUSDT', 
        'VETUSDT', 
        'FILUSDT', 
        'ICPUSDT',  # Time series start in May 2021
        'SANDUSDT', 
        'HBARUSDT', 
        'XTZUSDT', 
        'AXSUSDT', 
        'AAVEUSDT', 
        'THETAUSDT', 
        'EGLDUSDT', 
        'QNTUSDT', # Time series start on 29 July 2021
        'EOSUSDT', 
        'ZECUSDT', 
        'HNTUSDT', 
        'MKRUSDT', 
        'FTMUSDT', 
        'IOTAUSDT', 
        'GRTUSDT', 
        'RUNEUSDT', 
        'KLAYUSDT', # Time series start on 24 June 2021
        'XECUSDT', # Time series start on 3 September 2021
        'NEOUSDT', 
        'CAKEUSDT', 
        'CRVUSDT', 
        'BATUSDT', 
        'WAVESUSDT', 
        'STXUSDT', 
        'LRCUSDT', 
        'ENJUSDT', 
        'ZILUSDT', 
        'DASHUSDT', 
        'KAVAUSDT', 
        'BTGUSDT',  # Time series start in April 2021
        'KSMUSDT', 
        'DCRUSDT', 
        'XEMUSDT', 
        'HOTUSDT', 
        'ARUSDT', # Time series start in May 2021
        'ANKRUSDT', 
        'CVXUSDT', # Time series start in December 2021
        'COMPUSDT', 
        'SNXUSDT', 
        'QTUMUSDT', 
        'YFIUSDT', 
        'ONEUSDT', 
        'TFUELUSDT', 
        'AMPUSDT', # Time series start in November 2021
        'ICXUSDT', 
        'OMGUSDT', 
        'RSRUSDT', 
        'ZRXUSDT', 
        'AUDIOUSDT', 
        'JSTUSDT', 
        'BALUSDT', 
        'KNCUSDT', 
        'IOSTUSDT', 
        'ENSUSDT', # Time series start in November 2021
        'LPTUSDT', # Time series start in May 2021
        'BTCSTUSDT', # Many missing
        'BNXUSDT', # Time series start in November 2021
        'WAXPUSDT', # Time series start in August 2021
        'HIVEUSDT', 
        'LUNAUSDT', # Many missing
        'ZENUSDT', 
        'ONTUSDT', 
        'SXPUSDT', 
        'SKLUSDT', 
        'UMAUSDT', 
        'SCRTUSDT', # Time series start in January 2022
        'POLYUSDT', # Time series start in September 2021
        'SLPUSDT', # Time series start on 30 April 2021
        'CVCUSDT', 
        'DGBUSDT', 
        'SUSHIUSDT', 
        'RNDRUSDT', # Time series start in November 2021
        'API3USDT', # Time series start in January 2022
        'DYDXUSDT', # Time series start in September 2021
        'WINUSDT', 
        'SPELLUSDT', # Time series start in December 2021
        'ACAUSDT', # Time series start in January 2022
        'XNOUSDT', # Time series start in January 2022
        'RLCUSDT',
        'OCEANUSDT',
        'REEFUSDT',
        'TRIBEUSDT', # Time series start in August 2021
        'CFXUSDT', # Time series start on 29 March 2021
        'NMRUSDT',
        'CTSIUSDT',
        'BNTUSDT',
        'CHRUSDT',
        'WRXUSDT',
        'BICOUSDT', # Time series start in December 2021
        'C98USDT', # Time series start in July 2021
        'SANTOSUSDT', # Time series start in December 2021
        'FUNUSDT',
        'REPUSDT',
        'RAYUSDT', # Time series start in August 2021
        'PYRUSDT', # Time series start in November 2021
        'CTKUSDT',
        'STRAXUSDT',
        'STMXUSDT',
        'STPTUSDT',
        'FXSUSDT', # Time series start in December 2021
        'JOEUSDT', # Time series start in December 2021
        'RADUSDT', # Time series start in October 2021
        'ELFUSDT', # Time series start in September 2021
        'NKNUSDT',
        'ANTUSDT',
        'FETUSDT',
        'ACHUSDT', # Time series start in January 2022
		'CHZUSDT',
		'BTTCUSDT', # Time series start in January 2022
		'RVNUSDT',
		'MINAUSDT', # Time series start in August 2021
		'TWTUSDT',
		'CELOUSDT',
		'1INCHUSDT',
		'ROSEUSDT',
		'GALAUSDT', # Time series start in September 2021
		'IOTXUSDT',
    ]

    return CCs_to_download
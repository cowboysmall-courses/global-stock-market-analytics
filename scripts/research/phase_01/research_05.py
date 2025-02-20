
"""

Global market indices of interest:

    NSEI:  Nifty 50
    DJI:   Dow Jones Index
    IXIC:  Nasdaq
    HSI:   Hang Seng
    N225:  Nikkei 225
    GDAXI: Dax
    VIX:   Volatility Index

"""



# %% 1 - import required libraries
from cowboysmall.data.file import read_index_file, save_master_file
from cowboysmall.data.master import merge_data
from cowboysmall.feature import INDICES



# %% 2 - read data, merge data, and save the data
save_master_file(merge_data([read_index_file(index) for index in INDICES]))

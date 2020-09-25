import requests
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

import datetime as dt
import time


def main():
    # 6 months * 3 days * 24 hours / 6 hours per candle = 720 candles
    candles = 6 * 30 * 24/6

    # couldnt get the end parameter working so had to fix the start so it is 6 months before now
    milliseconds = int(round(time.time() * 1000))
    months_6 = 6 * 30 * 24 * 60 * 60 *1000
    start_period = milliseconds - months_6

    param = {'limit':candles,
            'sort':1,
            'start':start_period}

    r = requests.get('https://api-pub.bitfinex.com/v2/candles/trade:6h:tBTCUSD/hist', params = param)
    
    ohlc_df = pd.DataFrame(r.json(), columns = ['timestamp', 'open', 'close', 'high', 'low', 'vol'])
    ohlc_df['timestamp'] = pd.to_datetime(ohlc_df['timestamp'], unit='ms')
    ohlc_df = ohlc_df.set_index('timestamp')


    
    # ohlc_df['change'] = (ohlc_df['close'] / ohlc_df['open']) -1
    # For some reason new timestamp opens at different value than previous closed at so I used close to close as change instead
    ohlc_df['change'] = ohlc_df['close'].pct_change()
    ohlc_df['vol-weight change'] = ohlc_df['change'] * ohlc_df['vol']


    # Initially planned on doing a 2 axis graph with change and price plotted on top of each other, decided otherwise

    # # plt.plot(ohlc_df['change'])
    # # plt.show()
    # # fig, ax1 = plt.subplots(figsize=(15,7))
    # # ax1.plot(ohlc_df['change'])
    # # ax1.set_ylabel('Change')
    # # ax2 = ax1.twinx()
    # # ax2.set_ylabel('Price', color='red')
    # # ax2.plot(ohlc_df['close'], color='red')
    # # print(ohlc_df)


    # Plotting the histogram
    figure(figsize=(15,7))
    plt.style.use('seaborn-darkgrid')
    plt.hist(ohlc_df['change'], bins=125)

    plt.axvline(ohlc_df['change'].mean(), color='k', linestyle='dashed', linewidth=1)
    plt.title('Histogram of returns over 6 hour periods', fontsize=20)
    plt.xlabel('Change', fontsize=15)
    plt.ylabel('Count', fontsize=15)


    # Adding text
    min_ylim, max_ylim = plt.ylim()
    plt.text(0.02, max_ylim*0.9, 'Mean: {:.6f}'.format(ohlc_df['change'].mean()))
    plt.text(0.02, max_ylim*0.88, 'Std: {:.6f}'.format(ohlc_df['change'].std()))
    plt.show()

    


    # Plotting the price movement
    plt.style.use('seaborn-darkgrid')
    fig = figure(figsize=(15,7))
    plt.plot(ohlc_df['close'])
    plt.title('Price development', fontsize=20)
    plt.ylabel('Price', fontsize=15)
    plt.xlabel('Date', fontsize=15)
    plt.show()

    print(ohlc_df)

main()
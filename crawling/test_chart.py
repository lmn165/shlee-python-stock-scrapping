import os

import pandas_datareader as pdr
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def execute_stock_to_plt(dts):
    df = pdr.DataReader('NVDA', 'yahoo', '2022-04-01')
    # df.to_excel('./data/NVDA.xlsx')
    df.reset_index(inplace=True, drop=False)
    # print(df.keys())
    # print(df.head())

    plt.figure(figsize=(10, 4))
    plt.plot(df['Date'], df['Close'])
    plt.xlabel('')
    plt.ylabel('close')
    plt.tick_params(
        axis='x',
        which='both',
        bottom=False,
        top=False,
        labelbottom=False)
    for dt in dts:
        dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
        td = timedelta(days=0.1)
        plt.axvspan(dt - td, dt + td, facecolor='gray', alpha=0.5)
    plt.savefig('./data/sample.png', dpi=300)


def execute_read_list(fname):
    date_count ={}
    for dir in os.listdir(f'./data/{fname}'):
        for big_i in os.listdir(f'./data/{fname}/{dir}'):
            for i in os.listdir(f'./data/{fname}/{dir}/{big_i}'):
                date_str = i.split('_')[1].split('.')[0]
                date = []
                date.append(int(date_str[:4]))
                date.append(int(date_str[4:6]))
                date.append(int(date_str[6:8]))
                # print(datetime(date[0], date[1], date[2]))
                tmp_date = datetime(date[0], date[1], date[2])
                date_count[str(tmp_date)] = date_count.get(str(tmp_date), 0) + 1

    # print(date_count)
    # print(date_count.keys())
    return date_count.keys()


if __name__ == '__main__':
    dts = execute_read_list('엔비디아')
    execute_stock_to_plt(dts)

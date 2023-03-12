# Name: Henry Ramstad
# Anaylsis and visualization of three of the largest ETFs run
# through the investment service vanguard

"""
The ETFs used in the following analysis:
VTI: Vanguard Total Stock Market ETF
VOO: Vanguard S&P 500 ETF
VXUS: Vanguard Total International Stock ETF

data obtained via
https://www.kaggle.com/datasets/borismarjanovic/price-volume-data-for-all-us-stocks-etfs?resource=download
"""
from datetime import datetime
import csv
from matplotlib import pyplot as plt, dates as mdates
import numpy as np


def data_extraction(filename):
    """
    CSV data files recieved as Date, Open, High, Low, Close, Volume.
    this function takes a csv data file of this output and returns a
    list of lists containing this information.
    """
    final_list = []
    f = open(filename)
    input_file = csv.DictReader(f)
    column_names = input_file.fieldnames
    for name in column_names:
        column_data = []
        for row in input_file:
            column_data.append(row[name])
        f.seek(0)
        input_file = csv.DictReader(f)
        if name in ['Open', 'High', 'Low', 'Close']:
            column_data = [float(x) for x in column_data]
        elif name == 'Volume':
            column_data = [int(x) for x in column_data]

        final_list.append(column_data)
    f.close()
    return final_list


def plot_open_close(list_of_lists, etf_name):
    """
    This function takes in a list of lists as data parsed by data_extraction
    and returns a graph of the average between the daily open and close price
    of each ETF over the course of its known data.
    """
    dates = list_of_lists[0]
    opn = list_of_lists[1]
    clse = list_of_lists[4]
    x = [datetime.strptime(d, "%m/%d/%Y").date() for d in dates]
    avg_price = np.mean([opn, clse], axis=0)
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=500))
    ax.tick_params(axis='x', labelrotation=45)
    ax.set_facecolor('lightgray')
    plt.plot(x, avg_price, color='red', label='Average')
    plt.xlabel('Date')
    plt.ylabel('Price in USD')
    plt.title(f'{etf_name}: Open and Close Price Average')
    plt.legend()
    plt.show()


def plot_high_low_recent(list_of_lists, etf_name):
    """
    This function takes in a list of lists as data parsed by data_extraction
    and returns a graph of the recent high and low pricing to examine approx.
    one year of performance.
    """
    dates = list_of_lists[0][-300:]
    high_recent = list_of_lists[2][-300:]
    low_recent = list_of_lists[3][-300:]
    x = [datetime.strptime(d, "%m/%d/%Y").date() for d in dates]
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=50))
    ax.tick_params(axis='x', labelrotation=45)
    ax.set_facecolor('lightgray')
    plt.plot(x, high_recent, label='High')
    plt.plot(x, low_recent, label='Low')
    plt.xlabel('Date')
    plt.ylabel('Price in USD')
    plt.title(f'{etf_name}: Recent High and Low performance')
    plt.legend()
    plt.show()


vti = data_extraction('vti.csv')
voo = data_extraction('voo.csv')
vxus = data_extraction('vxus.csv')

plot_open_close(vti, 'VTI')
plot_high_low_recent(vti, 'VTI')

plot_open_close(voo, 'VOO')
plot_high_low_recent(voo, 'VOO')

plot_open_close(vxus, 'VXUS')
plot_high_low_recent(vxus, 'VXUS')

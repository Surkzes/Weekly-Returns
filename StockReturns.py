import pandas as pd
import numpy as np
from pandas_datareader import data as wb
from scipy.stats import norm
import matplotlib as mpl
import matplotlib.pyplot as plt
from operator import itemgetter
import datetime
import csv


# Calculate Stock Returns
def get_Stock_Returns(ticker, startdate, enddate):  
    
    stock_data = pd.DataFrame()
    stock_data[ticker] = wb.DataReader(ticker, data_source="yahoo", start=startdate, end=enddate)['Adj Close']
    
    
    #plot_Graph(stock_data)
    #print(stock_data[:20])

    weekly_returns = []
    
    loop = 1
    week = 5
    while(loop == 1):
        
        print(stock_data[:week])
        week = week + 5
        
        if (week > 30):
            loop = 3

    print(stock_data[1])
# Function to plot a graph
def plot_Graph(graph_Data):
    
    #plt.style.use('Solarize_Light2')    
    plt.figure(figsize=(10,6))
    
    plt.title("Title")
    plt.ylabel("Y-Axis")
    plt.xlabel("Time")
    
    plt.plot(graph_Data)
    plt.show()

    
get_Stock_Returns('SPY', '2017-1-1', '2020-7-1')
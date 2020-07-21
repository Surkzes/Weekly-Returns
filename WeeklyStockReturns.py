import pandas as pd
import numpy as np
from pandas_datareader import data as wb
import matplotlib.pyplot as plt


# Calculate Weekly Stock Returns

def get_Stock_Returns(ticker, startdate, enddate):  
    
    # Pull Stock Data
    stock_data = pd.DataFrame()
    stock_data = wb.DataReader(ticker, data_source="yahoo", start=startdate, end=enddate)['Adj Close']
    
    # Initialize Variables For Weekly Return Loop
    day_count = 1
    week_begin = 0
    week_end = 0
    returns = 0
    week = 0
   
    x = np.arange(1, (len(stock_data - 1))/5)
    weekly_returns = pd.DataFrame(x)
    
    # Loop Through Stock Data and Calculate Returns
    for day in range(0, len(stock_data - 1)):
        
        if(day_count == 1):
            week_begin = stock_data[day]
            print("Begin ", week_begin)
            
        if(day_count == 5):      
            weekly_returns.loc[week] = (stock_data[day] - week_begin) / week_begin * 100
            #print(weekly_returns.loc[week])
            print("End ", stock_data[day])
            
            week += 1
            day_count = 0

            
        day_count += 1
    
    max_value = int(np.amax(weekly_returns))
    min_value = int(np.amin(weekly_returns))
    
   
    # Output Return Data     
    print(weekly_returns)
    plot_Graph(weekly_returns, ticker, max_value, min_value)      


# Graph Weekly Return Data
          
def plot_Graph(graph_Data, ticker, max_value, min_value):
    
    plt.style.use('seaborn-ticks')    
    plt.figure(figsize=(10,6))
    
    axes = plt.axes()
    axes.set_ylim([(min_value - 2), (max_value + 1)])
    axes.set_yticks(np.arange(min_value, max_value, 2))
    plt.axhline(y=0,xmin=0,xmax=200,c="red",linewidth=1,zorder=0)
    
    plt.title("Weekly Stock Returns")
    plt.ylabel("Weekly Return %")
    plt.xlabel("Trading Weeks")
    
    plt.plot(graph_Data, label=ticker)
    plt.legend(framealpha=1, frameon=True)
    
    plt.show()


# Calculate Basic Stock Statistics

def print_stock_data(stock_data):
    print('Stock Mean:', np.mean(stock_data))
    print('Current Price:', stock_data[len(stock_data)-1])
    print('Start Date Price:', stock_data[0])
    print('Median Price', np.median(stock_data))
    print('Stock Variance', stock_data.var())
    print('Stock Standard Deviation', stock_data.std())


# Run Program    
get_Stock_Returns('TSLA', '2020-4-1', '2020-7-17')

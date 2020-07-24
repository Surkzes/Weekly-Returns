import pandas as pd
import numpy as np
from pandas_datareader import data as wb
import matplotlib.pyplot as plt
import datetime
import pandas_market_calendars as mcal
import timeit

start = timeit.default_timer()

#    Converts Y-M-D value to datetime object
def ymd_to_dt(ymd_date):
    year, month, day = (int(x) for x in ymd_date.split('-'))    
    return datetime.date(year, month, day)


#     Accepts Y-M-D value and outputs day of the week
#                 in integer form Mon = 0; Sunday = 6
def weekday(date):
    return datetime.datetime.weekday(ymd_to_dt(date))

#    Find the next opened date
def next_opened_date(stock_data, closed_date, rewind, nyse):
    rewind += 1
    if market_closed((closed_date - datetime.timedelta(days=rewind)).strftime('%Y-%m-%d'), nyse):                               
        week_begin = next_opened_date(stock_data, closed_date, rewind)                    
    else:
        week_begin = stock_data[closed_date - datetime.timedelta(days=rewind)]  
    #print("Market Closed moved backwards: ", rewind, "closed date ", closed_date)    
    return week_begin        
            
#   Checks if the date is a holiday
#
def get_business_days_list(startdate, enddate):   
    nyse = mcal.get_calendar('NYSE')
    business_days = nyse.valid_days(start_date=startdate, end_date=enddate).strftime('%Y-%m-%d')
    date_list = []
    for date in range(0, len(business_days) - 1):
        date_list.append(business_days[date])  
    return date_list

def market_closed(date, nyse):
    try:
        nyse.index(date)
        return False
    except: 
        return True
# Calculate Weekly Stock Returns

def get_Stock_Returns(ticker, startdate, enddate):  
    
    # Pull Stock Data
    stock_data = pd.DataFrame()
    stock_data = wb.DataReader(ticker, data_source="yahoo", start=startdate, end=enddate)['Adj Close']
    
    # Initialize Variables For Weekly Return Loop
    week_begin = 0
    week_end = 0
    week = 0
    first_week = 0    
   
    y = []
    x = []
    
    start_date = ymd_to_dt(startdate)
    end_date = ymd_to_dt(enddate)
    
    delta = datetime.timedelta(days=1)
    mon_fri = datetime.timedelta(days=4)
    fri_mon = datetime.timedelta(days=2)

    nyse = get_business_days_list(startdate, enddate)
    
    while start_date <= end_date:              
        
        if (datetime.datetime.weekday(start_date) == 0): 
            
            if(market_closed(start_date.strftime('%Y-%m-%d'), nyse) and (first_week == 1)):
                week_begin = next_opened_date(stock_data, start_date, 2, nyse)                  
            if (not(market_closed(start_date.strftime('%Y-%m-%d'), nyse))): 
                week_begin = stock_data[start_date]               
                first_week = 1
            if((start_date + mon_fri) <= end_date):
                start_date += mon_fri
            
        
        if ((first_week == 1) and (datetime.datetime.weekday(start_date) == 4)):
            if market_closed(start_date.strftime('%Y-%m-%d'), nyse):
                week_end = next_opened_date(stock_data, start_date, 0, nyse)            
            else:
                week_end = stock_data[start_date]             
            y.append((week_end - week_begin) / week_begin * 100)
            x.append(start_date.strftime('%Y-%m-%d'))
            
            week += 1
            start_date += fri_mon
           
        start_date += delta

    max_value = int(max(y))
    min_value = int(min(y))

    # Output Return Data  
    # Show Graph  
    #plot_Graph(y, ticker, max_value, min_value, x)              

    # Save Graph
    save_Graph(y, ticker, max_value, min_value, x)

def get_y_count(daterange, begin_range, end_range):   
    if((daterange >= begin_range) and (daterange <=end_range)):
        return 1
    else:
        begin_range += 5
        end_range += 5     
        return 1 + get_y_count(daterange, begin_range, end_range)

#     Graph Weekly Return Data         
def plot_Graph(graph_Data, ticker, max_value, min_value, daterange):
    
    y_count = get_y_count(len(daterange), 0, 5)
    
    plt.style.use('seaborn-ticks')    
    plt.figure(figsize=(10,6))
    
    axes = plt.axes()
    axes.set_ylim([int((min_value - 2)), int(max_value + 2)])
    axes.set_xticks(np.arange(0, len(daterange), y_count))
    axes.set_yticks(np.arange(int(min_value), int(max_value + 2), 2))
    
    plt.title("Weekly Stock Returns")
    plt.ylabel("Weekly Return %")
    plt.xlabel("Trading Weeks")
    
    plt.axhline(y=0,xmin=0,xmax=200,c="red",linewidth=1,zorder=0) 
    plt.plot (daterange, graph_Data, label=ticker)
    plt.legend(framealpha=1, frameon=True)
    plt.show()
    
def save_Graph(graph_Data, ticker, max_value, min_value, daterange):
    
    y_count = get_y_count(len(daterange), 0, 5)
    
    plt.style.use('seaborn-ticks')    
    plt.figure(figsize=(10,6))
    
    axes = plt.axes()
    axes.set_ylim([int((min_value - 2)), int(max_value + 2)])
    axes.set_xticks(np.arange(0, len(daterange), y_count))
    axes.set_yticks(np.arange(int(min_value), int(max_value + 2), 2))
    
    plt.title("Weekly Stock Returns")
    plt.ylabel("Weekly Return %")
    plt.xlabel("Trading Weeks")
    
    plt.axhline(y=0,xmin=0,xmax=200,c="red",linewidth=1,zorder=0) 
    plt.plot (daterange, graph_Data, label=ticker)
    plt.legend(framealpha=1, frameon=True)
    plt.savefig("temp_returns.png")
    plt.close()
    

# Run Program    
get_Stock_Returns('SPY', '2020-04-01', '2020-07-21')

stop = timeit.default_timer()

print('Time: ', stop - start)  

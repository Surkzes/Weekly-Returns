import pandas as pd
import numpy as np
from pandas_datareader import data as wb
import matplotlib.pyplot as plt
import datetime
import pandas_market_calendars as mcal

#    Converts Y-M-D value to datetime object
def ymd_to_dt(ymd_date):
    year, month, day = (int(x) for x in ymd_date.split('-'))    
    return datetime.date(year, month, day)


#     Accepts Y-M-D value and outputs day of the week
#                 in integer form Mon = 0; Sunday = 6
def weekday(date):
    return datetime.datetime.weekday(ymd_to_dt(date))

#    Find the next opened date
def next_opened_date(stock_data, closed_date, rewind):
    rewind += 1
    if(market_closed((closed_date - datetime.timedelta(days=rewind)).strftime('%Y-%m-%d'))):                               
        week_begin = next_opened_date(stock_data, closed_date, rewind)                    
    else:
        week_begin = stock_data[closed_date - datetime.timedelta(days=rewind)]  
    print("Market Closed moved backwards: ", rewind, "closed date ", closed_date)    
    return week_begin        
            
#   Checks if the date is a holiday
#
def market_closed(date):
    
    if (weekday(date) == 5 or weekday(date) == 6):
        return True
    
    #    Create date variable for date + 1
    year, month, day = (int(x) for x in date.split('-'))    
    enddate = (datetime.date(year, month, day) + datetime.timedelta(days=3)).strftime('%Y-%m-%d')

    #    Get business day list from date to date + 1
    nyse = mcal.get_calendar('NYSE')
    business_days = nyse.valid_days(start_date=date, end_date=enddate).strftime('%Y-%m-%d')
    
    #    If date is in the list, then return true, if its not then return false
    if(len(business_days) == 0):
        return False
    if(business_days[0] == date):
        return False
    else:
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
   
    x = np.arange(0, (len(stock_data)/5))
    y = np.arange(0, (len(stock_data)/5))
    
    weekly_returns = {'Week End Date':x, 'Weekly Return':y}
    weekly_returns = pd.DataFrame(weekly_returns)

    start_date = ymd_to_dt(startdate)
    end_date = ymd_to_dt(enddate)
    delta = datetime.timedelta(days=1)

    
    while start_date <= end_date:              
            
        if (datetime.datetime.weekday(start_date) == 0): 
            if(market_closed(start_date.strftime('%Y-%m-%d'))):
                week_begin = next_opened_date(stock_data, start_date, 2)                  
            else: 
                week_begin = stock_data[start_date]               
            first_week = 1

        if ((first_week == 1) and (datetime.datetime.weekday(start_date) == 4)):
            if(market_closed(start_date.strftime('%Y-%m-%d'))):
                week_end = next_opened_date(stock_data, start_date, 0)            
            else:
                week_end = stock_data[start_date]               
            weekly_returns.iloc[week]['Weekly Return'] = (week_end - week_begin) / week_begin * 100
            weekly_returns.iloc[week]['Week End Date'] = start_date.strftime('%Y-%m-%d')
            first_week = 0
            week += 1
          
        start_date += delta
        
    max_value = np.amax(weekly_returns["Weekly Return"])
    min_value = np.amin(weekly_returns["Weekly Return"])
    print(max_value)
    print(min_value)
    
    # Output Return Data     
    weekly_returns_adjusted = weekly_returns.drop(np.arange(week, len(weekly_returns)))
    #print(weekly_returns_adjusted)
    
    plot_Graph(weekly_returns_adjusted, ticker, max_value, min_value, start_date, end_date)              


#     Graph Weekly Return Data         
def plot_Graph(graph_Data, ticker, max_value, min_value, start_date, end_date):
    
    plt.style.use('seaborn-ticks')    
    plt.figure(figsize=(10,6))
    
    axes = plt.axes()
    #axes.set_ylim([(min_value - 2), (max_value + 2)])
    axes.set_xlim(start_date, end_date)
    #axes.set_yticks(np.arange(min_value, max_value + 2, 2))
    plt.axhline(y=0,xmin=0,xmax=200,c="red",linewidth=1,zorder=0)
    
    plt.title("Weekly Stock Returns")
    plt.ylabel("Weekly Return %")
    plt.xlabel("Trading Weeks")
    
    graph_Data.plot(x='Week End Date', y='Weekly Return', label=ticker)
    plt.legend(framealpha=1, frameon=True)
    
    plt.show()

# Run Program    
get_Stock_Returns('SPY', '2020-01-01', '2020-07-20')

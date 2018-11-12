"""MC2-P1: Market simulator.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		   	  			    		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		   	  			    		  		  		    	 		 		   		 		  
All Rights Reserved  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		   	  			    		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		   	  			    		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		   	  			    		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		   	  			    		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		   	  			    		  		  		    	 		 		   		 		  
or edited.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		   	  			    		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		   	  			    		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		   	  			    		  		  		    	 		 		   		 		  
GT honor code violation.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Student Name: Everardo Villasenor (replace with your name)
GT User ID: evillasenor3 (replace with your User ID)
GT ID: 903389317 (replace with your GT ID)
"""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data


def author():
    return 'evillasenor3'  # replace tb34 with your Georgia Tech username.

def compute_portvals(orders_file="./orders/orders-01.csv", start_val=1000000, commission=9.95, impact=0.005):
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # get_data handles trading days only
    # 1. Read in Orders file and Sort by date
    orders_df = pd.read_csv(orders_file, parse_dates=True, na_values=['nan'])
    date_range = pd.date_range(orders_df['Date'].min(), orders_df['Date'].max())

    # 3. Build Data frame prices (prices should be adjusted close)
    # scan orders.csv and get all distinct symbols
    symbols = pd.unique(orders_df['Symbol'])
    prices_df = get_data(symbols, dates=date_range, addSPY=False)
    prices_df = prices_df.dropna(how='all').fillna(method='ffill')
    prices_df = prices_df.fillna(method='bfill')
    # Add cash columns
    prices_df['Cash'] = 1.0

    # Build data frame trades
    # Represents changes
    trades_df = prices_df.copy()
    trades_df[:] = 0.0
    iter = 0

    for i in range(len(orders_df['Date'])):
        iter += 1
        date = orders_df.iloc[i, 0]
        symbol = orders_df.iloc[i , 1]
        order = orders_df.iloc[i, 2]
        quantity = orders_df.iloc[i, 3]

        cash = prices_df.loc[date, symbol] * quantity
        if order == "BUY":
            trades_df.loc[date, symbol] += quantity
            trades_df.loc[date, 'Cash'] -= cash
            trades_df.loc[date, 'Cash'] = trades_df.loc[date, 'Cash'] - commission - prices_df.loc[date, symbol] * quantity * impact
        else:
            trades_df.loc[date, symbol] -= quantity
            trades_df.loc[date, 'Cash'] += cash
            trades_df.loc[date, 'Cash'] = trades_df.loc[date, 'Cash'] - commission - prices_df.loc[date, symbol] * quantity * impact


    # print trades
    # print trades_df

    # print
    # print "Trades"
    # print trades_df
    # print

    # Create a data frame holdings
    holdings_df = trades_df.copy()
    holdings_df[1:] = 0
    holdings_df.iloc[0, -1] = holdings_df.iloc[0, -1] + start_val

    for i in range(1, holdings_df.shape[0]):
        holdings_df.iloc[i] = holdings_df.iloc[i - 1] + trades_df.iloc[i]

    # print
    # print "Holdings"
    # print holdings_df
    # print

    # Create dataframe value
    values_df = prices_df * holdings_df

    # print "Values: "
    # print values_df
    # print

    portvals = values_df.sum(axis=1)

    # print portvals
    return portvals


def test_code():
    # this is a helper function you can use to test your code  		   	  			    		  		  		    	 		 		   		 		  
    # note that during autograding his function will not be called.  		   	  			    		  		  		    	 		 		   		 		  
    # Define input parameters  		   	  			    		  		  		    	 		 		   		 		  

    of = "./orders/orders-01.csv"
    sv = 1000000
    sf = 252
    rfr = 0

    # Process orders  		   	  			    		  		  		    	 		 		   		 		  
    portvals = compute_portvals(orders_file=of, start_val=sv, commission=0, impact=0)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[
            portvals.columns[0]]  # just get the first column
    else:
        "warning, code did not return a DataFrame"

        # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.  		   	  			    		  		  		    	 		 		   		 		  
    start_date = dt.datetime(2008, 1, 1)
    end_date = dt.datetime(2008, 6, 1)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2, 0.01, 0.02, 1.5]
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2, 0.01, 0.02, 1.5]

    indices = portvals.index.values
    start_date = min(indices)
    end_date = max(indices)
    cum_ret = np.asscalar(portvals[-1] / portvals[0] - 1)
    portvals_norm = portvals / portvals[0]
    curDay = portvals_norm[1:]
    prevDay = portvals_norm[0:-1]
    dailyReturns = np.divide(np.subtract(curDay, prevDay), prevDay)
    avg_daily_ret = dailyReturns.mean()
    std_daily_ret = dailyReturns.std()
    sharpe_ratio = np.sqrt(sf) * np.divide((avg_daily_ret - rfr), std_daily_ret)


    # Compare portfolio against $SPX
    print
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])


if __name__ == "__main__":
    test_code()

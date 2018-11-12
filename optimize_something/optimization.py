"""MC1-P2: Optimize a portfolio.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
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
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import scipy.optimize as spo
from util import get_data, plot_data


# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def optimize_portfolio(sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 1, 1), \
                       syms=['GOOG', 'AAPL', 'GLD', 'XOM'], gen_plot=False):
    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later
    norm_price = normalize_data(prices)  # Normalize the prices according to the 1st day

    # Find the allocations for the optimal portfolio
    # Function to minimize which is the negative Sharpe Ratio
    def sharpe_func(allocs, sv=1000000, rfr=0.0, sf=252.0):
        norm_alloced = norm_price * allocs
        pos_vals = norm_alloced * sv
        # Get daily portfolio value
        port_val = pos_vals.sum(axis=1)
        daily_returns = (port_val / port_val.shift(1)) - 1
        daily_returns.ix[0, 0] = 0
        daily_returns = daily_returns[1:]
        k = np.sqrt(sf)
        sharpe = k * (daily_returns.mean() - rfr) / daily_returns.std()
        # print "X = {}, Y = {}".format(allocs, sharpe)

        return sharpe

    def min_sharpe_func(allocs):
        return -sharpe_func(allocs)

    # Constraints and bounds
    cons = ({'type': 'eq', 'fun': lambda x: np.sum(x)-1})
    bnds = tuple((0,1) for x in range(len(syms)))
    # Initial Guess
    equal_alloc = np.ones(len(syms), dtype='float64') * 1.0 / len(syms)

    # Call the optimizer
    min_result = spo.minimize(min_sharpe_func, equal_alloc, method='SLSQP', bounds=bnds, constraints=cons,
                        options={'disp': False})
    # print "Minima found at:"
    # print "X = {}, Y = {}".format(min_result.x.round(3), min_result.fun)

    allocs = np.asarray(min_result.x)
    sv = 1000000 # $1M
    norm_alloced = norm_price * allocs
    pos_vals = norm_alloced * sv
    # Get daily portfolio value
    port_val = pos_vals.sum(axis=1)
    cr, adr, sddr, sr = compute_portfolio_stats(port_val, allocs)

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        df_temp = normalize_data(df_temp)
        plot_data(df_temp, "Daily Portfolio vs. SPY")
        pass

    return allocs, cr, adr, sddr, sr


def compute_portfolio_stats(df, \
                            allocs = [0.1,0.2,0.3,0.4], \
                            rfr = 0.0, sf = 252.0):

    cr = (df.ix[-1, :]/df.ix[0, :]) - 1
    daily_returns = (df / df.shift(1)) - 1
    daily_returns.ix[0, 0] = 0
    daily_returns = daily_returns[1:]
    adr = daily_returns.mean()
    sddr = daily_returns.std()
    k = np.sqrt(sf)
    sr = k * (adr - rfr)/sddr
    return cr, adr, sddr, sr


def normalize_data(df):
    return df/df.ix[0, :]


def test_code():
    # This function WILL NOT be called by the auto grader  		   	  			    		  		  		    	 		 		   		 		  
    # Do not assume that any variables defined here are available to your function/code  		   	  			    		  		  		    	 		 		   		 		  
    # It is only here to help you set up and test your code  		   	  			    		  		  		    	 		 		   		 		  

    # Define input parameters  		   	  			    		  		  		    	 		 		   		 		  
    # Note that ALL of these values will be set to different values by  		   	  			    		  		  		    	 		 		   		 		  
    # the autograder!  		   	  			    		  		  		    	 		 		   		 		  

    start_date = dt.datetime(2008, 06, 01)
    end_date = dt.datetime(2009, 06, 01)
    symbols = ['GOOG', 'X', 'GLD', 'JPM']

    # Assess the portfolio  		   	  			    		  		  		    	 		 		   		 		  
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd=start_date, ed=end_date, \
                                                        syms=symbols, \
                                                        gen_plot=True)

    # Print statistics  		   	  			    		  		  		    	 		 		   		 		  
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr


if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader  		   	  			    		  		  		    	 		 		   		 		  
    # Do not assume that it will be called  		   	  			    		  		  		    	 		 		   		 		  
    test_code()

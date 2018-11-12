"""Assess a betting strategy.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
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

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def author():
    return 'evillasenor3'  # replace tb34 with your Georgia Tech username.


def gtid():
    return 903389317  # replace with your GT ID number


def get_spin_result(win_prob):
    result = False
    # print("Win prob: " + str(float(win_prob)))
    spin = np.random.random()
    if spin <= win_prob:
        # print("Result: " + str(spin))
        result = True
    return result


def test_code(num_simulations, bankroll_bool):
    win_prob = float(18.0/38.0)  # set appropriately to the probability of a win
    np.random.seed(gtid())  # do this only once
    # print(get_spin_result(win_prob))  # test the roulette spin

    # add your code here to implement the experiments
    winnings = np.zeros((num_simulations, 1000), dtype=int)
    eighty_winnings = 0
    episode_loss = 0
    other_winnings = 0
    for x in range(num_simulations):
        trials = 0
        episode_winnings = 0
        if bankroll_bool:
            bankroll = 256
        else:
            bankroll = float('inf')
        while episode_winnings < 80 and trials < 999 and episode_winnings > -256:
            won = False
            bet_amount = 1
            while not won:
                won = get_spin_result(win_prob)
                if won:
                    episode_winnings = episode_winnings + bet_amount
                    bankroll = bankroll + bet_amount
                else:
                    episode_winnings = episode_winnings - bet_amount
                    bankroll = bankroll - bet_amount
                    if bankroll < (bet_amount * 2):
                        bet_amount = bankroll
                    else:
                        bet_amount = bet_amount * 2

                trials += 1
                # print("Trial: " + str(trials))
                # print("Winnings: " + str(episode_winnings))
                winnings[x, trials] = episode_winnings

        if episode_winnings == 80 and bankroll_bool == 1:
            eighty_winnings += 1
        elif episode_winnings == -256 and bankroll_bool == 1:
            episode_loss += 1
        elif episode_winnings > -256 and bankroll_bool == 1:
            other_winnings += 1

        while trials < 999:
            trials += 1
            # print("Trial: " + str(trials))
            # print("Winnings: " + str(episode_winnings))
            winnings[x, trials] = episode_winnings

        # Plot the Figure 1:
        # print(winnings.size)
        if num_simulations == 10:
            # print("Simulation: " + str(x+1))
            plt.xlabel('Trials')
            plt.ylabel('Winnings ($)')
            name = "Episode: " + str(x+1)
            plt.plot(winnings[x], label=name)

    if num_simulations == 10 and bankroll > 500:
        # Figure 1
        plt.legend(loc = 'best')
        plt.ylim((-256, +100))
        plt.xlim((0, 300))
        plt.savefig('figure1.png')
        plt.clf()
    elif bankroll > 500:
        # Figure 2
        plt.xlabel('Trials')
        plt.ylabel('Winnings ($)')
        mean_array = np.mean(winnings, axis=0)
        plt.plot(mean_array, label="$\mu$")
        std_array = np.std(winnings, axis=0)
        mean_plus_std = mean_array + std_array
        plt.plot(mean_plus_std, label="$\mu + \sigma$")
        mean_minus_std = mean_array - std_array
        plt.plot(mean_minus_std, label="$\mu - \sigma$")
        plt.legend(loc='best')
        plt.ylim((-256, +100))
        plt.xlim((0, 300))
        plt.savefig('figure2.png')
        plt.clf()

        # Figure 3
        plt.xlabel('Trials')
        plt.ylabel('Winnings ($)')
        median_array = np.median(winnings, axis=0)
        plt.plot(median_array, label="median")
        std_array = np.std(winnings, axis=0)
        median_plus_std = median_array + std_array
        plt.plot(median_plus_std, label="median + $\sigma$")
        median_minus_std = median_array - std_array
        plt.plot(median_minus_std, label="median - $\sigma$")
        plt.legend(loc='best')
        plt.ylim((-256, +100))
        plt.xlim((0, 300))
        plt.savefig('figure3.png')
        plt.clf()
    else:
        # Figure 5
        plt.xlabel('Trials')
        plt.ylabel('Winnings ($)')
        mean_array = np.mean(winnings, axis=0)
        plt.plot(mean_array, label="$\mu$")
        std_array = np.std(winnings, axis=0)
        mean_plus_std = mean_array + std_array
        plt.plot(mean_plus_std, label="$\mu + \sigma$")
        mean_minus_std = mean_array - std_array
        plt.plot(mean_minus_std, label="$\mu - \sigma$")
        plt.legend(loc='best')
        plt.ylim((-256, +100))
        plt.xlim((0, 300))
        plt.savefig('figure4.png')
        plt.clf()

        # Figure 6
        plt.xlabel('Trials')
        plt.ylabel('Winnings ($)')
        median_array = np.median(winnings, axis=0)
        plt.plot(median_array, label="median")
        std_array = np.std(winnings, axis=0)
        median_plus_std = median_array + std_array
        plt.plot(median_plus_std, label="median + $\sigma$")
        median_minus_std = median_array - std_array
        plt.plot(median_minus_std, label="median - $\sigma$")
        plt.legend(loc='best')
        plt.ylim((-256, +100))
        plt.xlim((0, 300))
        plt.savefig('figure5.png')
        plt.clf()

        print("Win: " + str(eighty_winnings))
        print("Loss: " + str(episode_loss))
        print("Other: " + str(other_winnings))


if __name__ == "__main__":
    # Experiment 1:
    syms = ['GOOG', 'AAPL', 'GLD', 'XOM']

    num_syms = len(syms)

    allocs = (1.0 / num_syms) * num_syms

    print allocs
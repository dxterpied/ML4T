"""  		   	  			    		  		  		    	 		 		   		 		  
template for generating data to fool learners (c) 2016 Tucker Balch  		   	  			    		  		  		    	 		 		   		 		  
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
import math

# this function should return a dataset (X and Y) that will work  		   	  			    		  		  		    	 		 		   		 		  
# better for linear regression than decision trees


def best4LinReg(seed=1489683273):  		   	  			    		  		  		    	 		 		   		 		  
    np.random.seed(seed)
    mu = np.random.randint(100, size=100)
    sigma = np.random.randint(100, size=100)
    s = np.random.normal(mu, sigma)
    r = np.random.uniform(0, np.pi, size=100)
    radial = s*[np.cos(r), np.sin(r)]
    X = np.array([radial[0], radial[1]]).T
    Y = X[:, 0] + X[:, 1]
    return X, Y  		   	  			    		  		  		    	 		 		   		 		  


def best4DT(seed=1489683273):
    np.random.seed(seed)
    X = np.random.randint(100, size=(100, 4))
    # Y = np.random.random(size=(100,))*200-100
    # Here's is an example of creating a Y from randomly generated
    # X with multiple columns
    Y = X[:, 0] + np.sin(X[:, 1]) + np.sin(X[:, 2]) ** 2 + X[:, 3] ** 3
    return X, Y


def author():
    return 'evillasenor3' #Change this to your user ID


if __name__=="__main__":
    print ""
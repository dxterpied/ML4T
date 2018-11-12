"""  		   	  			    		  		  		    	 		 		   		 		  
Test a learner.  (c) 2015 Tucker Balch

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
"""

import numpy as np
import math
import LinRegLearner as lrl
import DTLearner as dt
import RTLearner as rt
import BagLearner as bl
import InsaneLearner as it
import sys
import util
import matplotlib.pyplot as plt
import pandas as pd
import time

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: python testlearner.py <filename>"
        sys.exit(1)

    inf = open(sys.argv[1])
    if sys.argv[1] == 'Data/Istanbul.csv':
        data = np.genfromtxt(util.get_learner_data_file('Istanbul.csv'), delimiter=',')
        data = data[1:, 1:]
    else:
        data = np.array([map(float, s.strip().split(',')) for s in inf.readlines()])

    # compute how much of the data is training and testing
    print "Data shape: "
    print data.shape[0]
    train_rows = int(0.6 * data.shape[0])
    test_rows = data.shape[0] - train_rows

    # separate out training and testing data  		   	  			    		  		  		    	 		 		   		 		  
    trainX = data[:train_rows, 0:-1]
    trainY = data[:train_rows, -1]
    testX = data[train_rows:, 0:-1]
    testY = data[train_rows:, -1]

    print testX.shape
    print testY.shape

    x1 = np.linspace(1, 25, num=25, dtype='int32')
    rmse_in_sample = []
    rmse_out_sample = []

    for i in x1:
        leaf_size = i
        # create a decision tree learner and train it
        learner = dt.DTLearner(leaf_size, verbose=False)
        learner.addEvidence(trainX,trainY)
        # print learner.author()

        # evaluate in sample
        predY = learner.query(trainX)  # get the predictions
        rmse = math.sqrt(((trainY - predY) ** 2).sum() / trainY.shape[0])
        # print
        # print "In sample results"
        # print "RMSE: ", rmse
        # c = np.corrcoef(predY, y=trainY)
        # print "corr: ", c[0, 1]

        rmse_in_sample.append(rmse)

        # evaluate out of sample
        predY = learner.query(testX)  # get the predictions
        rmse = math.sqrt(((testY - predY) ** 2).sum() / testY.shape[0])
        # print
        # print "Out of sample results"
        # print "RMSE: ", rmse
        # c = np.corrcoef(predY, y=testY)
        # print "corr: ", c[0, 1]

        rmse_out_sample.append(rmse)

    plt.plot(x1, rmse_in_sample, 'b-', label="In Sample Error")
    plt.plot(x1, rmse_out_sample, 'r-', label="Out of Sample Error")
    plt.xlabel('Leaf Size')
    plt.ylabel('RMSE')
    plt.legend(loc='best')
    plt.savefig('image1.png', bbox_inches='tight')

    # Make the table
    diff_error = abs(np.array(rmse_out_sample) - np.array(rmse_in_sample))
    print "Mean Difference between in and out sample error"
    print np.mean(diff_error)

    # 2nd Question
    rmse_in_sample_2 = []
    rmse_out_sample_2 = []
    x2 = np.linspace(1, 25, num=25, dtype='int32')
    for i in x2:

        leaf_size = i
        learner = bl.BagLearner(learner=dt.DTLearner, kwargs={"leaf_size": leaf_size}, bags=20, boost=False, verbose=False)
        learner.addEvidence(trainX, trainY)
        # evaluate in sample
        predY = learner.query(trainX)  # get the predictions
        rmse = math.sqrt(((trainY - predY) ** 2).sum() / trainY.shape[0])
        rmse_in_sample_2.append(rmse)

        # evaluate out of sample
        predY = learner.query(testX)  # get the predictions
        rmse = math.sqrt(((testY - predY) ** 2).sum() / testY.shape[0])
        rmse_out_sample_2.append(rmse)

    # Bagging Reduce or Eliminate?
    plt.clf()
    plt.plot(x2, rmse_in_sample_2, 'b-', label="In Sample Error")
    plt.plot(x2, rmse_out_sample_2, 'r-', label="Out of Sample Error")
    plt.ylim(0, 0.008)
    plt.xlabel('Leaf Size')
    plt.ylabel('RMSE')
    plt.legend(loc='best')
    plt.savefig('image2.png', bbox_inches='tight')

    # Make the table
    diff_error = abs(np.array(rmse_out_sample_2, dtype='float32') - np.array(rmse_in_sample_2, dtype='float32'))
    print "Mean Difference between in and out sample error"
    print np.mean(diff_error)

    # 3rd Question between DT and RT
    rmse_in_sample_dt = []
    rmse_out_sample_dt = []
    rmse_in_sample_rt = []
    rmse_out_sample_rt = []
    time_dt = []
    time_rt = []
    x3 = np.linspace(1, 25, num=25, dtype='int32')
    for i in x3:
        leaf_size = i
        # create a decision tree learner and train it
        learner = dt.DTLearner(leaf_size, verbose=False)
        start_time = time.time()
        learner.addEvidence(trainX, trainY)
        end_time = time.time()
        time_dt.append(end_time-start_time)
        predY = learner.query(trainX)  # get the predictions
        rmse = math.sqrt(((trainY - predY) ** 2).sum() / trainY.shape[0])

        rmse_in_sample_dt.append(rmse)

        # evaluate out of sample
        predY = learner.query(testX)  # get the predictions
        rmse = math.sqrt(((testY - predY) ** 2).sum() / testY.shape[0])

        rmse_out_sample_dt.append(rmse)

        # create a decision tree learner and train it
        learner = rt.RTLearner(leaf_size, verbose=False)
        start_time = time.time()
        learner.addEvidence(trainX, trainY)
        end_time = time.time()
        time_rt.append(end_time-start_time)
        predY = learner.query(trainX)  # get the predictions
        rmse = math.sqrt(((trainY - predY) ** 2).sum() / trainY.shape[0])

        rmse_in_sample_rt.append(rmse)

        # evaluate out of sample
        predY = learner.query(testX)  # get the predictions
        rmse = math.sqrt(((testY - predY) ** 2).sum() / testY.shape[0])

        rmse_out_sample_rt.append(rmse)

    diff_error_in_sample = abs(
        np.array(rmse_in_sample_dt, dtype='float32') - np.array(rmse_in_sample_rt, dtype='float32'))
    diff_error_out_sample = abs(
        np.array(rmse_out_sample_dt, dtype='float32') - np.array(rmse_out_sample_rt, dtype='float32'))

    # Bagging Reduce or Eliminate?
    plt.clf()
    plt.plot(x3, rmse_in_sample_dt, 'b-', label="DT In Sample Error")
    plt.plot(x3, rmse_out_sample_dt, 'r-', label="DT Out Sample Error")
    plt.plot(x3, rmse_in_sample_rt, 'b--', label="RT In Sample Error")
    plt.plot(x3, rmse_out_sample_rt, 'r--', label="RT Out Sample Error")
    plt.xlabel('Leaf Size')
    plt.ylabel('RMSE')
    plt.title('Difference between DTLearner and RTLearner')
    plt.legend(loc='best')
    plt.savefig('image3.png', bbox_inches='tight')

    plt.clf()
    plt.plot(x2, time_dt, 'b-', label="DT")
    plt.plot(x2, time_rt, 'r-', label="RT")
    plt.xlabel('Leaf Size')
    plt.ylabel('Time to Learn')
    plt.legend(loc='best')
    plt.savefig('image4.png', bbox_inches='tight')

    print "DT Mean Time: " + str(np.mean(time_dt))
    print "RT Mean Time: " + str(np.mean(time_rt))

    # compute how much of the data is training and testing

    x4 = np.linspace(0.1, 0.75, num=75)
    rmse_in_sample_dt = []
    rmse_out_sample_dt = []
    rmse_in_sample_rt = []
    rmse_out_sample_rt = []
    for i in x4:
        train_rows = int(i * data.shape[0])
        test_rows = data.shape[0] - train_rows

        # separate out training and testing data
        trainX = data[:train_rows, 0:-1]
        trainY = data[:train_rows, -1]
        testX = data[train_rows:, 0:-1]
        testY = data[train_rows:, -1]

        # create a decision tree learner and train it
        learner = dt.DTLearner(leaf_size=1, verbose=False)
        learner.addEvidence(trainX, trainY)
        predY = learner.query(trainX)  # get the predictions
        rmse = math.sqrt(((trainY - predY) ** 2).sum() / trainY.shape[0])

        rmse_in_sample_dt.append(rmse)

        # evaluate out of sample
        predY = learner.query(testX)  # get the predictions
        rmse = math.sqrt(((testY - predY) ** 2).sum() / testY.shape[0])

        rmse_out_sample_dt.append(rmse)

        # create a decision tree learner and train it
        learner = rt.RTLearner(leaf_size=1, verbose=False)
        learner.addEvidence(trainX, trainY)
        predY = learner.query(trainX)  # get the predictions
        rmse = math.sqrt(((trainY - predY) ** 2).sum() / trainY.shape[0])

        rmse_in_sample_rt.append(rmse)

        # evaluate out of sample
        predY = learner.query(testX)  # get the predictions
        rmse = math.sqrt(((testY - predY) ** 2).sum() / testY.shape[0])

        rmse_out_sample_rt.append(rmse)

    plt.clf()
    plt.plot(x4*100, rmse_in_sample_dt, 'b-', label="DT In Sample Error")
    plt.plot(x4*100, rmse_out_sample_dt, 'r-', label="DT Out Sample Error")
    plt.plot(x4*100, rmse_in_sample_rt, 'b--', label="RT In Sample Error")
    plt.plot(x4*100, rmse_out_sample_rt, 'r--', label="RT Out Sample Error")
    plt.xlabel('% of training data')
    plt.ylabel('RMSE')
    plt.title('Difference between DTLearner and RTLearner in Learning Curve')
    plt.legend(loc='best')
    plt.savefig('image5.png', bbox_inches='tight')
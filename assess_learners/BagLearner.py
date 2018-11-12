"""
A simple wrapper for random tree learner.  (c) 2015 Tucker Balch

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
import pandas as pd
import LinRegLearner as lrl
import DTLearner as dt
import RTLearner as rt


class BagLearner(object):

    def __init__(self, learner, kwargs, bags=20, boost=False, verbose=False):
        """
       :param verbose: print out information for debugging
       """
        self.verbose = verbose
        self.bags = bags
        self.boost = boost
        self.kwargs = kwargs
        learners = []
        for i in xrange(bags):
            learners.append(learner(**kwargs))
        self.learners = learners


    def author(self):
        return 'evillasenor3'  # replace tb34 with your Georgia Tech username

    def addEvidence(self, dataX, dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """
        # Train this ensemble learner
        # Randomly sample with replacement in a bag

        for i in xrange(self.bags):
            sample_idx = np.random.choice(int(dataX.shape[0]), int(dataX.shape[0]), replace=True)
            sample_dataX = dataX[sample_idx, :]
            sample_dataY = dataY[sample_idx]
            self.learners[i].addEvidence(sample_dataX, sample_dataY)

    def query(self, points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        predY = []
        for i in xrange(self.bags):
            # print self.learner[i].query(points)
            predY.append(self.learners[i].query(points))

        # Average of each column
        # print predY
        estimate = np.mean(predY, axis=0)

        # print estimate
        return estimate


if __name__ == "__main__":
    print "the secret clue is 'zzyzx'"

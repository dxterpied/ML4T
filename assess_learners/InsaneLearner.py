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
import LinRegLearner as lrl
import BagLearner as bl


class InsaneLearner(object):

    def __init__(self, learner=lrl.LinRegLearner, kwargs={}, bags=20, boost=False, verbose=False):
        """
       :param verbose: print out information for debugging
       """
        self.verbose = verbose
        self.bags = bags
        self.boost = boost
        self.kwargs = kwargs
        self.learner = learner
        learners = [bl.BagLearner(learner, kwargs) for i in xrange(bags)]
        # for i in xrange(bags):
        #     learners.append(bl.BagLearner(learner, kwargs))
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
        for i in xrange(self.bags):
            self.learners[i].addEvidence(dataX, dataY)

    def query(self, points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        predY = [self.learners[i].query(points) for i in range(self.bags)]
        # for i in xrange(self.bags):
            # print self.learner[i].query(points)
            # predY.append(self.learners[i].query(points))

        # print estimate
        return np.mean(predY, axis=0)

"""
A simple wrapper for decision tree learner.  (c) 2015 Tucker Balch

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


class DTLearner(object):

    def __init__(self, leaf_size=1, verbose=False):
        """

       :param leaf_size: maximum number of samples to be aggregated at a leaf
       :param verbose: print out information for debugging
       """
        self.leaf_size = leaf_size
        self.verbose = verbose
        self.tree = np.array([])

    def author(self):
        return 'evillasenor3'  # replace tb34 with your Georgia Tech username

    def addEvidence(self, dataX, dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """
        # print "Building a Tree"

        leaf = np.array(([-1, dataY[0], np.nan, np.nan],))

        # print "Data X Shape: "
        # print dataX.shape[0]
        # One Row Check
        if dataX.shape[0] <= self.leaf_size:
            return leaf

        # Check if all Ys are the same
        if np.unique(dataY).size == 1:
            return leaf

        # Determine best feature i to split on
        # Get a map of features and their correlations
        # print "Determining best feature i to split on"

        # Initialize the dataframe
        # df = pd.DataFrame(index=np.arange(dataX.shape[0]), columns=np.arange(dataX.shape[1]))
        # Go through each xVariable and add it to the data frame
        corr_coefs = []
        for feature in xrange(dataX.shape[1]):
            # df[feature] = dataX[:, feature]
            if np.isnan(abs(np.corrcoef(dataX[:, feature], dataY)[0, 1])):
                corr_coefs.append(0.0)
            else:
                corr_coefs.append(abs(np.corrcoef(dataX[:, feature], dataY)[0, 1]))

        # print "1st Corr: "
        # print corr_coefs
        # print "Max: "
        best_feature_i = np.nanargmax(corr_coefs)
        # Add the last column as Y
        # df[feature+1] = dataY[:]


        # Shape the correlation matrix
        # corr_df = abs(df.corr())
        # corr_df = corr_df.drop(feature+1, axis=0)

        # print "2nd Corr: "
        # print corr_df
        # Last column of the correlation is what we're interested in
        # corr_np = corr_df[feature+1].values
        # Index of the maximum correlation
        # best_feature_i = np.nanargmax(corr_np)
        # print "Best Feature: "
        # print best_feature_i

        # Split the data according to the best feature
        split_val = np.median(dataX[:, best_feature_i])
        # print "Split Value: "
        # print split_val

        # Check if split val is sending the whole tree:
        left_idx = dataX[:, best_feature_i] <= split_val

        if dataX[left_idx].shape[0] == dataX.shape[0]:
            return leaf

        # Build left tree recursively
        left_tree = self.addEvidence(dataX[left_idx], dataY[left_idx])
        right_tree = self.addEvidence(dataX[dataX[:, best_feature_i] > split_val],
                                      dataY[dataX[:, best_feature_i] > split_val])

        root = np.array(([best_feature_i, split_val, 1, left_tree.shape[0]+1]),)

        # print "Shapes: "
        # print root.shape
        # print left_tree.shape
        # print right_tree.shape

        self.tree = np.vstack((root, left_tree, right_tree))

        return self.tree

    def query(self, points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        # print points.shape[0]
        # print self.tree
        predY = []

        for point in points:
            # Traverse the tree
            # Get the first feature (X11)
            # If it is a leaf return it
            # Else compare the corresponding feature with the split value
            # print "Point: "
            # print point
            row = 0
            feat, split_val = self.tree[row, 0:2]
            while int(feat) != -1:
                if point[int(feat)] <= split_val:
                    # Go to the left tree
                    row_to_go = self.tree[int(row), 2]
                    row = row + row_to_go
                else:
                    # Go to the right tree
                    row_to_go = self.tree[int(row), 3]
                    row = row + row_to_go

                feat, split_val = self.tree[int(row), 0:2]

                # print "Split Value: " + str(split_val)

            # print "Appended a value"
            predY.append(split_val)

        return predY


if __name__ == "__main__":
    print "the secret clue is 'zzyzx'"

#!/usr/bin/python

# Testing/
import random
import collections
import math
import sys
from collections import Counter
from collections import defaultdict
from util import *

import copy
import chess
import chess.syzygy
import chess.gaviota

import functools
import os.path
import warnings
import json

import features
from features import *
############################################################
# Problem 3: binary classification
############################################################

############################################################
# Problem 3a: feature extraction

def extractWordFeatures(x):
    """
    Chess Features
    """
    # BEGIN_YOUR_CODE (around 5 lines of code expected)
    
    features = {}
    features.update(canCatchPawn(x))
    features.update(isWhiteKingAhead(x))
    features.update(isOpposition(x))
    features.update(move_distances(x))
    features.update(wrongSide(x))
    features.update(canBeCaptured(x))
    features.update(ishPawn(x))


    print x
#    print canCatchPawn(x)
#    print isWhiteKingAhead(x)
#    print isOpposition(x)
#    print move_distances(x)
#    print wrongSide(x)
#    print canBeCaptured(x) 
    
    print features

    # y = x.pieces(chess.KING, chess.BLACK)
    # for a in y:
    #     print a
    # END_YOUR_CODE

    #x.piece_at(56)
    #x.pieces(chess.KING, chess.BLACK)

############################################################
# Problem 3b: stochastic gradient descent

def learnPredictor(trainExamples, testExamples, featureExtractor):
    '''
    Given |trainExamples| and |testExamples| (each one is a list of (x,y)
    pairs), a |featureExtractor| to apply to x, and the number of iterations to
    train |numIters|, return the weight vector (sparse feature vector) learned.

    You should implement stochastic gradient descent.

    Note: only use the trainExamples for training!
    You should call evaluatePredictor() on both trainExamples and testExamples
    to see how you're doing as you learn after each iteration.
    numIters refers to a variable you need to declare. It is not passed in.
    '''
    weights = {}  # feature => weight
    weights = defaultdict(lambda: 0, weights)
    
    # BEGIN_YOUR_CODE (around 15 lines of code expected)
    numIters = 1;
    curIters = 0;
    n = 0.08

    syzygy = chess.syzygy.Tablebases()
    num = 0
    num += syzygy.open_directory(os.path.join(os.path.dirname(__file__), "four-men"))

    pos = 0
    for i in range (0,numIters):
        
 #       OPP = '2k5/8/2K5/8/8/8/5P2/8'

 #       board = chess.Board(OPP + " " + "w" + " - - 0 1")
 #       expectVal = syzygy.probe_wdl(board)
 #       if pos <= 10000:
 #       features = featureExtractor(board)

        for t in trainExamples:

            dotProd = 0
            #loading syzgy
            
            board = chess.Board(t + " " + "w" + " - - 0 1")
            expectVal = syzygy.probe_wdl(board)
            if pos <= 10000:
                features = featureExtractor(board)
                pos = pos + 1
            else:
                break
            # for val in features:
            #     dotProd += weights[val] * features[val]

            # if (1 - dotProd * t[1]) >= 0:
            #     for val in features:
            #         weights[val] = weights[val] +  n * features[val] * expectedVal

            # curIters = curIters + 1
    
    # END_YOUR_CODE
    return weights

############################################################
# Problem 3c: generate test case

def generateDataset(numExamples, weights):
    '''
    Return a set of examples (phi(x), y) randomly which are classified correctly by
    |weights|.
    '''
    random.seed(42)
    # Return a single example (phi(x), y).
    # phi(x) should be a dict whose keys are a subset of the keys in weights
    # and values can be anything (randomize!) with a nonzero score under the given weight vector.
    # y should be 1 or -1 as classified by the weight vector.
    def generateExample():
        # BEGIN_YOUR_CODE (around 2 lines of code expected)
        phi = {}
        for x in weights:
            if random.randint(1,2) == 1:
                phi[x] = random.randint(1,100)

        totalSum = 0
        
        for i in range(len(phi.keys())):
            totalSum += weights[phi.keys()[i]] * phi[phi.keys()[i]]
            
        y = 0  
        if totalSum < 0:
            y = -1
        else:
            y = 1
        print (phi,y)
        
        # END_YOUR_CODE
        return (phi, y)
    return [generateExample() for _ in range(numExamples)]


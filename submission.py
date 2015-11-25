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
def extractWordFeatures(x):
    """
    Chess Features
    """
    
    features = {}
    features = defaultdict(lambda: 0.0, features)

    features.update(canCatchPawn(x))
    if (features['cant catch pawn'] == 1):
        return features

    features.update(canBeCaptured(x))
    # if (features['black_can_capture'] == 1):
    #     return {'black_can_capture':1}
    features.update(isWhiteKingAhead(x))
    features.update(isOpposition(x))
    features.update(move_distances(x))
    features.update(wrongSide(x))
    features.update(ishPawn(x))
    
    return features

def isIllegal(FEN):
    
    rows = FEN.split('/')

    for i, j in enumerate(rows):
        if i == 0 or i == 7:
            for ch in j:
                if ch == 'P' or ch == 'p':
                    return True

    return False

def isolationTest(features):
    
    FEN = '2k5/2P5/2K5/8/8/8/8/8'
    
    board = chess.Board(FEN + " " + "w" + " - - 0 1")
#    expectVal = syzygy.probe_wdl(board)
    print(board)
    print features(board)
    

    FEN = '2k5/2P5/4K3/8/8/8/8/8'
    
    board = chess.Board(FEN + " " + "w" + " - - 0 1")
#    expectVal = syzygy.probe_wdl(board)
    print(board)
    print features(board)


############################################################
# Problem 3b: stochastic gradient descent

def learnPredictor(trainExamples, testExamples, featureExtractor, color, syzygy):
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
    weights = defaultdict(lambda: 0.0, weights)
   
    
    # BEGIN_YOUR_CODE (around 15 lines of code expected)
    numIters = 1;
    curIters = 0;
    n = 0.01

    pos = 0

    blackPos = 0
    blackNeg = 0
    for i in range (0,numIters):


        for t in trainExamples:
            if isIllegal(t):
                continue

            dotProd = 0.0
            
            board = chess.Board(t + " " + color + " - - 0 1")
            expectVal = syzygy.probe_wdl(board)

            if (expectVal is None):
                continue
            elif (expectVal == 0):
                expectVal = -1.0
            else:
                expectVal = 1.0

            # pos = pos + 1

            # if pos%10000 == 0:
            #     print pos

            features = featureExtractor(board)

            if(features['black_can_capture'] == 1):
                if (expectVal == -1):
                    blackPos = blackPos + 1
                elif (expectVal == 1):
                    blackNeg = blackNeg + 1
                    # print board
                    # print isIllegal(t)
                    # print ""
                # if (blackNeg == 100):
                #     break
                # print weights['black_can_capture']
                # print expectVal
                # print " "

            for val in features:
                dotProd += weights[val] * features[val]

            if (1 - dotProd * expectVal) >= 0:
                for val in features:
                    weights[val] = weights[val] +  n * features[val] * expectVal

            curIters = curIters + 1
        print blackPos
        print blackNeg
        print i
        print weights
    
    # END_YOUR_CODE
    print weights
    return weights

def test(examples, color, weights, syzygy):
    total = 0
    correct = 0
    incorrect = 0
    for t in examples:
        if isIllegal(t):
                continue

        board = chess.Board(t + " " + color + " - - 0 1")
        expectVal = syzygy.probe_wdl(board)
        features = extractWordFeatures(board)

        if (expectVal is None):
            continue
        elif (expectVal == 0):
            expectVal = -1
        else:
            expectVal = 1
        

        ourVal = 0

        for val in features:
            ourVal += weights[val] * features[val]

        if (ourVal <= 0):
            ourVal = -1
        elif (ourVal > 0):
            ourVal = 1


        if ourVal == expectVal:
            correct = correct + 1
        # else:
        #     incorrect = incorrect + 1
        #     print board
        #     print expectVal
        #     print ourVal
        #     print " "
        #     if incorrect == 100:
        #         break
        
        # print ourVal

        total = total + 1

        if (total % 1000 == 0):
            print correct
            print total
            print " "

    print correct
    print total

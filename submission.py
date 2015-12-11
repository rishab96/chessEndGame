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

# import features2P
# from features2P import *

import featuresRook
from featuresRook import *

def extractFeatures_Rook(board):
    
    A = getRookFeatures(board)
    print A



# def extractFeatures2(board):
    
#     # do "w" or "b" thing here:

# #    board = chess.Board(FEN)

#     features = {}
#     features = defaultdict(lambda: 0.0, features)
     
# #    feature_test(board)
# #    print board    
#     A = getFeatures2P(board)
#     print A
#     features.update(A)
# #    canCatchPawn(FEN)


#     return features






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

def runIsolation(FEN, features):
    
    # make it white to play.
    # complete FEN.
    FEN = FEN + " " + "b" + " - - 0 1"
    board = chess.Board(FEN)
#    expectVal = syzygy.probe_wdl(board)
    print(board)
    print features(board)
    
#    print 'testing board changes: '
#    print board


def isolationTest(features):
    
    print 'in isolation test'

# for Kp endgames:
    isolationTestP(features)

#   rook endgames
#    isolationTestR(features)

def isolationTestR(features):
    
   # FEN = 'r7/8/8/3k4/8/5P2/1K6/4R3'
   # runIsolation(FEN, features)
    
    
#    FEN = '5r2/8/8/3k4/8/5P2/5K2/4R3'
#    runIsolation(FEN, features)

#    FEN = 'r7/8/8/4k3/8/2P5/2K5/1R6'
#    runIsolation(FEN, features)
    
    FEN = '6r1/8/7R/3k4/6P1/8/5K2/8'
    runIsolation(FEN, features)


def isolationTestP(features):

#    FEN = '2k5/2P5/2K5/8/8/8/8/8'
    
#    board = chess.Board(FEN + " " + "w" + " - - 0 1")
#    expectVal = syzygy.probe_wdl(board)
#    print(board)
#    features(board)
    
#    print 'testing board changes: '
#    print board


#    FEN = '8/4k3/8/4K1p1/6P1/8/8/8'
    

#    FEN = FEN + " " + "w" + " - - 0 1"
#    board = chess.Board(FEN)
#    expectVal = syzygy.probe_wdl(board)
#    print(board)
#    print features(FEN)
    
#    print 'testing board changes: '
#    print board
    
    FEN = '8/3k1p2/5P2/3K4/8/8/8/8'
    runIsolation(FEN, features)



    # position 2
    FEN = '8/7k/6p1/4K3/6P1/8/8/8'   
    runIsolation(FEN, features)
    # position 3:
    
    FEN = '4k3/5p2/5P2/3K4/8/8/8/8'   
    runIsolation(FEN, features)
    
    # position 5:
    FEN = '8/5p2/3K1P1k/8/8/8/8/8'      
    runIsolation(FEN, features)
    # position 6:

    FEN = '8/5p1k/5P2/3K4/8/8/8/8' 
    runIsolation(FEN, features)
    # position 7:
#    FEN = '4k3/8/8/5p2/2K2P2/8/8/8' 
#    runIsolation(FEN, features)
    # position 8:

 #   FEN = '8/2k5/8/5p2/2K2P2/8/8/8' 
 #   runIsolation(FEN, features)
    # position 9: Winning
#    FEN = '8/8/8/5K2/3p4/1k1P4/8/8'
#    runIsolation(FEN, features)
    
    # These are adjacent pawn positions
    # position 10: Draw
#    FEN = '8/1k6/8/1K2p3/8/5P2/8/8'
#    runIsolation(FEN, features)

    # position 11: Draw
#    FEN = '3k4/8/4p3/8/4K3/8/5P2/8'
#    runIsolation(FEN, features)
    
    # position 12: Win (hard -- needs minimax?
#    FEN = '8/1k6/8/K3p3/8/5P2/8/8'
#    runIsolation(FEN, features)
    #
    # These are double passed pawn positions
    # position 13: Win
#    FEN = '8/3k4/8/7P/p3K3/8/8/8'
#    runIsolation(FEN, features)

    # position 14: Draw
#    FEN = '8/3k4/8/7P/1p3K2/8/8/8'
#    runIsolation(FEN, features)
    # position 15: Win...after Queens made, loses it'
#    FEN = '8/8/8/1k5P/1p3K2/8/8/8'
#    runIsolation(FEN, features)
    
    # position 16: Draw...Q vs rook pawn:
#    FEN = '8/8/8/p6P/5K2/8/8/1k6'
#    runIsolation(FEN, features)

    # position 17: Win (black pawn too slow)
#    FEN = '8/8/p7/7P/5K2/8/8/1k6'
#    runIsolation(FEN, features)

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

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


    # print x
#    print canCatchPawn(x)
#    print isWhiteKingAhead(x)
#    print isOpposition(x)
#    print move_distances(x)
#    print wrongSide(x)
#    print canBeCaptured(x) 
    
    return features

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
    weights = defaultdict(lambda: 0.0, weights)
   
    
    # BEGIN_YOUR_CODE (around 15 lines of code expected)
    numIters = 5;
    curIters = 0;
    n = 1.0

    syzygy = chess.syzygy.Tablebases()
    num = 0
    num += syzygy.open_directory(os.path.join(os.path.dirname(__file__), "four-men"))

    pos = 0
    for i in range (0,numIters):
        
 #       OPP = '2k5/8/2K5/8/8/8/5P2/8'

        for t in trainExamples:

            dotProd = 0.0
            
            board = chess.Board(t + " " + "w" + " - - 0 1")
            expectVal = syzygy.probe_wdl(board)

            if (expectVal is None):
                continue
            elif (expectVal == 0):
                expectVal = -1.0
            else:
                expectVal = 1.0
            # elif (expectVal is None):
            #     print "continue"
            #     continue
            # if pos <= 10000:
            #     features = featureExtractor(board)
            #     pos = pos + 1
            # else:
            #     break
            # pos = pos + 1

            # if pos%10000 == 0:
            #     print pos
               
            

            features = featureExtractor(board)
            # print features
            # print weights
            # print expectVal
            # print " "


            for val in features:
                dotProd += weights[val] * features[val]
            #print dotProd

            if (1 - dotProd * expectVal) >= 0:
                for val in features:
                    weights[val] = weights[val] +  n * features[val] * expectVal

            curIters = curIters + 1
        print i
        print weights
    
    # END_YOUR_CODE
    print weights
    return weights

############################################################
# Problem 3c: generate test case
#1 iter:
#weights = {'black_opposition': 0.0, 'white_king_wrong_side': -1.0, 'can catch pawn': 0.0, 'white king ahead': 0.0, 'white_king_closer_to_winning_square': 0.0, 'white_king_ahead': 22.0, 'black_can_capture': 0.0, 'black_king_closer_closer_to_winning_square': 1.0, 'white_king_behind': 0.0, 'white_king_closer': 3.0, 'black_king_wrong_side': 0.0, 'white_king_blocked': 3.0, 'cant catch pawn': 6.0, 'black_king_closer': 3.0, 'h_pawn': 2.0}

#4 iterations
#{'black_opposition': 0.0, 'white_king_wrong_side': -1.0, 'can catch pawn': 0.0, 'white king ahead': -1.0, 'white_king_closer_to_winning_square': 0.0, 'white_king_ahead': 26.0, 'black_can_capture': 0.0, 'black_king_closer_closer_to_winning_square': 1.0, 'white_king_behind': 0.0, 'white_king_closer': 3.0, 'black_king_wrong_side': 0.0, 'white_king_blocked': 4.0, 'cant catch pawn': 6.0, 'black_king_closer': 3.0, 'h_pawn': 2.0}
def test(examples):
    weights = {'black_opposition': 0.0, 'white_king_wrong_side': -1.0, 'can catch pawn': 0.0, 'white king ahead': -1.0, 'white_king_closer_to_winning_square': 0.0, 'white_king_ahead': 26.0, 'black_can_capture': 0.0, 'black_king_closer_closer_to_winning_square': 1.0, 'white_king_behind': 0.0, 'white_king_closer': 3.0, 'black_king_wrong_side': 0.0, 'white_king_blocked': 4.0, 'cant catch pawn': 6.0, 'black_king_closer': 3.0, 'h_pawn': 2.0}   
    syzygy = chess.syzygy.Tablebases()

    num = 0
    num += syzygy.open_directory(os.path.join(os.path.dirname(__file__), "four-men"))   

    total = 0
    correct = 0
    incorrect = 0
    for t in examples:
        board = chess.Board(t + " " + "w" + " - - 0 1")
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
        else:
            incorrect = incorrect + 1
            print board
            print expectVal
            print ourVal
            print " "
            if incorrect == 100:
                break
    
        total = total + 1

        if (total %1000 == 0):
            print correct
            print total
            print " "
        #     print total

    print correct
    print total

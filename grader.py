#!/usr/bin/python

#import graderUtil
import util
#import time
from util import *

import submission
from submission import *

def train():
    trainExamples = readExamples('data.txt')
    submission.learnPredictor(trainExamples, trainExamples, extractWordFeatures)
    #submission.test(trainExamples)
    # devExamples = readExamples('polarity.dev')
    # featureExtractor = submission.extractWordFeatures
    # weights = submission.learnPredictor(trainExamples, devExamples, featureExtractor)
    # outputWeights(weights, 'weights')
    # outputErrorAnalysis(devExamples, featureExtractor, weights, 'error-analysis')  # Use this to debug
    # trainError = evaluatePredictor(trainExamples, lambda(x) : (1 if dotProduct(featureExtractor(x), weights) >= 0 else -1))
    # devError = evaluatePredictor(devExamples, lambda(x) : (1 if dotProduct(featureExtractor(x), weights) >= 0 else -1))
    # print "Official: train error = %s, dev error = %s" % (trainError, devError)
    # grader.requireIsLessThan(0.08, trainError)
    # grader.requireIsLessThan(0.30, devError)
def test():
    trainExamples = readExamples('data.txt')
    submission.test(trainExamples)
    
test()

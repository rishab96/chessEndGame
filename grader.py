#!/usr/bin/python

import util
from util import *

import submission
from submission import *

def train():
    trainExamples = readExamples('data.txt')
    submission.learnPredictor(trainExamples, trainExamples, extractWordFeatures)
    
def test():
    trainExamples = readExamples('data.txt')
    submission.test(trainExamples)

def isolationTest():
    
    submission.isolationTest(extractWordFeatures)

isolationTest()
#train()
#test()

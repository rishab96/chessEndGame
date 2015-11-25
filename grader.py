#!/usr/bin/python

import util
from util import *

import submission
from submission import *

def train(color, trainExamples, syzygy):
    return submission.learnPredictor(trainExamples, trainExamples, extractWordFeatures,color, syzygy)

    
def test(color, testExamples, trainExamples, syzygy):
    submission.test(testExamples, color, train(color, trainExamples, syzygy), syzygy)

def isolationTest(): 
    submission.isolationTest(extractWordFeatures)

syzygy = chess.syzygy.Tablebases()
num = 0
num += syzygy.open_directory(os.path.join(os.path.dirname(__file__), "four-men"))
data = readExamples('data.txt')


test('w', data, data, syzygy)

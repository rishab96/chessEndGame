#!/usr/bin/python

import util
from util import *

import submission
from submission import *

def train(color, trainExamples, syzygy):
    return submission.learnPredictor(trainExamples, trainExamples, extractWordFeatures,color, syzygy)

    
def test(color, testExamples, trainExamples, syzygy):
    submission.test(testExamples, color, train(color, trainExamples, syzygy), syzygy)

## IMP --> need to change the feature extractor here when running pawns
# vs when running rooks.
def isolationTest(): 
    features = extractFeatures2
#    features = extractFeatures_Rook
    submission.isolationTest(features)

#syzygy = chess.syzygy.Tablebases()
#num = 0
#num += syzygy.open_directory(os.path.join(os.path.dirname(__file__), "four-men"))
#data = readExamples('data.txt')

isolationTest()

#test('w', data, data, syzygy)

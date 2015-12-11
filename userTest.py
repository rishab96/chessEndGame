import copy
import chess
import chess.syzygy
import chess.gaviota
import collections

from collections import Counter
import features
from features import *
import os.path

weight_vector_3_piece = {'black_king_closer_to_winning_square': -1.400000000000001, 'black_opposition': -1.9200000000000015, 'cant catch pawn': 1.0000000000000007, 'can catch pawn': -0.27, 'white_king_closer': 1.0700000000000007, 'white_king_closer_to_winning_square': -0.22000000000000008, 'black_can_capture': -0.38000000000000017, 'white_king_blocked_down': 0.04000000000000009, 'white_king_blocked_side': -0.5200000000000002, 'white king ahead': 0.42000000000000015, 'black_king_wrong_side': 1.5400000000000011, 'white_king_blocked': -0.6000000000000003, 'white_king_wrong_side': -1.570000000000001, 'black_king_closer': -1.340000000000001, 'h_pawn': -2.6499999999999875}
weight_vector_4_piece = {'black_king_closer_to_winning_square': -1.400000000000001, 'black_opposition': -1.9200000000000015, 'cant catch pawn': 1.0000000000000007, 'can catch pawn': -0.27, 'white_king_closer': 1.0700000000000007, 'white_king_closer_to_winning_square': -0.22000000000000008, 'black_can_capture': -0.38000000000000017, 'white_king_blocked_down': 0.04000000000000009, 'white_king_blocked_side': -0.5200000000000002, 'white king ahead': 0.42000000000000015, 'black_king_wrong_side': 1.5400000000000011, 'white_king_blocked': -0.6000000000000003, 'white_king_wrong_side': -1.570000000000001, 'black_king_closer': -1.340000000000001, 'h_pawn': -2.6499999999999875}
weight_vector_5_piece = {'black_king_closer_to_winning_square': -1.400000000000001, 'black_opposition': -1.9200000000000015, 'cant catch pawn': 1.0000000000000007, 'can catch pawn': -0.27, 'white_king_closer': 1.0700000000000007, 'white_king_closer_to_winning_square': -0.22000000000000008, 'black_can_capture': -0.38000000000000017, 'white_king_blocked_down': 0.04000000000000009, 'white_king_blocked_side': -0.5200000000000002, 'white king ahead': 0.42000000000000015, 'black_king_wrong_side': 1.5400000000000011, 'white_king_blocked': -0.6000000000000003, 'white_king_wrong_side': -1.570000000000001, 'black_king_closer': -1.340000000000001, 'h_pawn': -2.6499999999999875}

def featureExtractor_3(x):
    """
    Chess Features
    """
    
    features = {}
    features = Counter()

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


def userInput():
	print ""
	print "This is an endgame solver designed to solve 3,4 and 5 piece chess"
	print "Currently it can solve the following board combinations: " #fill 
	print "Please enter the board in algebraic notation, enter . when you are done"
	print "Uppercase letters define white's pieces, while lowecase define black's pieces"
	print "If there are 2 pieces on the same row, please enter them in ascending order (ka1 before Pa3)"
	print ""
	pieces = []
	while True:
		newPiece = raw_input('Enter new piece: ')
		if newPiece == ".":
			break
		else:
			pieces.append(newPiece)

	FEN = processInput(pieces)

	turn = raw_input('Whose move is it (b or w): ')

	board = chess.Board(FEN + " " + turn + " - - 0 1")

	syzygy = chess.syzygy.Tablebases()
	num = 0
	num += syzygy.open_directory(os.path.join(os.path.dirname(__file__), "four-men"))

	output = predictOutput(board, syzygy, len(pieces))

	actualOutput = output[0]
	predictedOutput = output[1]

	if actualOutput != -100:
		if actualOutput == -1:
			print ""
			print "The actual value according to databases is: DRAW"
		else:
			print ""
			print "The actual value according to databases is: WIN"

		if actualOutput == -1:
			print "The predicted output according our algorithm is: DRAW"
		else:
			print "The predicted output according our algorithm is: WIN"
	print ""
#problem
#Enter new piece: Ka2
# Enter new piece: ka6
# Enter new piece: pd2
# Enter new piece: .
# Whose move is it (b or w): w
# 3

def predictOutput(board, syzygy, numPieces):
	features = {}
	if numPieces == 3:
		weights = weight_vector_3_piece
		features = featureExtractor_3(board)

	elif numPieces == 4:
		weights = weight_vector_4_piece
	elif numPieces == 5:
		weights = weight_vector_5_piece

	print board

	expectVal = syzygy.probe_wdl(board)
	if (expectVal is None):
	    print "Illegal move"
	    return (-100, -100)

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


	return (expectVal, ourVal)


def processInput(pieces):
	FEN = ""
	board = [ [] for i in range(8)]
	Error = ""
	wasError = False
	for piece in pieces:
		if len(piece) > 3:
			Error = piece + " incorrect"
			wasError = True
			break
		pieceType = piece[0]

		column = int(piece[2]) - 1
		row = piece[1]


		row = ord(row) - ord('a') + 1
		#row = row - 1

		if column > 7 or row > 8:
			wasError = True
			Error = "Row or column invalid"
			break

		column = 7 - column

		board[column].append((pieceType, row))

	FEN = processBoard(board)
	return FEN

def processBoard(board):
	FEN = ""
	for j, row in enumerate(board):
		rowFEN = ""
		curFilled = 0
		prevPos = 0
		for i,piece in enumerate(row):
			if (piece[1] == 1):
				rowFEN = piece[0]
				curFilled = 1

			elif i == 0:
				rowFEN = str(piece[1] - 1) + piece[0]
				curFilled = int(piece[1])
			else:
				diff = int(piece[1]) - curFilled - 1
				if (diff != 0):
					rowFEN += str(diff)
				rowFEN += piece[0]
				curFilled = int(piece[1])
		left = 8 - curFilled

		if left > 0:
			rowFEN += str(left)

		FEN += rowFEN
		if j != 7:
			FEN += "/"
	return FEN



	# curPos = 0
	# while True:
	# 	if numSlash == row:
	# 		break
	# 	if FEN[curPos] == '/':
	# 		numSlash += 1
	# 	curPos += 1

	# curPosTemp = curPos
	# FENofRow = ""

	# while FEN[curPosTemp] != "/":
	# 	FENofRow += FEN[curPosTemp]
	# 	curPosTemp += 1

		
		

def tester():
	print ord('z') - ord('a')

userInput()
	

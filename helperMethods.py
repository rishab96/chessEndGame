
# !/usr/bin/env python

import numpy as np
import chess
import chess.uci

# Take an fen --> swap_colors --> mirror_horizontal to get
# the mirror image with black being white. Also don't forget
# to change whose move it is.

def swap_colors(fen):
    parts = fen.split()
    return parts[0].swapcase() + " " + parts[1] + " - - 0 1"

def mirror_vertical(fen):
    parts = fen.split()
    position_parts = "/".join(reversed(parts[0].split("/")))
    return position_parts + " " + parts[1] + " - - 0 1"

def mirror_horizontal(fen):
    parts = fen.split()
    position_parts = "/".join("".join(reversed(position_part)) for position_part in parts[0].split("/"))
    return position_parts + " " + parts[1] + " - - 0 1"


def manhattanDistance( xy1, xy2 ):
  "Returns the Manhattan distance between points xy1 and xy2"
  return abs( xy1[0] - xy2[0] ) + abs( xy1[1] - xy2[1] )

## Usual helper methods.
def kingDistance(square1, square2): 

    row = abs(square1[0] - square2[0]) 
    col = abs(square1[1] - square2[1])
    return max(row, col)

def getNumber(row, column):
    return row*8 + column

def getRowAndColumn(num):
    
    row = num / 8
    column = num % 8
    return row,column

def getPiece(board, piece, color):
    
    results = []
    A = board.pieces(piece, color)
    for x in A:
        results.append(x)
    return results

def getPieceCoOrd(board, piece, color):

    res = getPiece(board, piece, color) 
         
    if len(res) != 0:
        num = res[0]
    else:
        return (None, None)
   
    row_k, col_k = getRowAndColumn(num)
    
    return row_k, col_k

def createNewBoard(board):
    
#    print board

    FEN = board.fen()

    return chess.Board(FEN)

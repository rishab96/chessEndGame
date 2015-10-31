# !/usr/bin/env python

import numpy as np
import chess

# board is a 2d grid.
#

def findPiece(board, piece):
    
    for row, i in enumerate(board):
        try:
            column = i.index(piece)
        except ValueError:
            continue
        return row, column
    return -1



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


def canCatchPawn2(board):
    
    # getPieces, then find the co-ordinates
    # of those pieces.
    move = True
    res = getPiece(board, chess.KING, chess.BLACK) 
    
    if len(res) != 0:
        num = res[0]

    
    row_k, col_k = getRowAndColumn(num)

    res2 = getPiece(board, chess.PAWN, chess.WHITE)

    if len(res2) != 0:
        num = res2[0]
    
    row_p, col_p = getRowAndColumn(num)

    if row_k < row_p:

        if move:
            return False
        if row_p - row_k > 1:
            return False
    

    moves_to_end = 7 - row_p
    moves_to_catch = abs(col_p - col_k) - 1

    if moves_to_end < moves_to_catch:
        return False

    if moves_to_end == moves_to_catch:
        if move:
            return False

    return True
    





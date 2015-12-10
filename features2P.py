# !/usr/bin/env python

import numpy as np
import chess
import chess.uci

import targetedCalculation
from targetedCalculation import *

import helperMethods
from helperMethods import *

engine = chess.uci.popen_engine("./stockfish6")
engine.uci()


def opposition(board):

    row_k, col_k = getPieceCoOrd(board, chess.KING, chess.BLACK)
    row_K, col_K = getPieceCoOrd(board, chess.KING, chess.WHITE)

    rd = row_k - row_K
    cd = col_k - col_K

    if rd == 2 and (abs(cd) == 2 or cd == 0):
        return True
    
    return False


# board is a 2d grid.
#

# useful methods.


####### New Features:
####### Basic idea is to consider only if White can win or not --> and then flip
# boards, and consider it from black's side as well. This reduces the complexity
# of the methods considerably. 
# Divided into different type of situations <--> will need to add a layer on top
# which analyses the type of position and calls the appropriate method.

# Note: use board.fen to create the fen representation and then convert it back to 
# a board to create a new board --> so original board isn't affected.

##### Pawns on the same file features below. These methods should only be called
# if we've verified that the pawns are on the same file.

# Need to implement these.
def passedPawns(board):
    A = {}


    return A

def adjacentPawns(board):
    A = {}


    return A

# Main wrapper function <--> which checks the board and then distributes the calls
# to either sameFile, passedPawns, or adjacent pawns.

def getFeatures2P(board):
    
    A = {}
    
    row_p, col_p =  getPieceCoOrd(board, chess.PAWN, chess.BLACK)
    row_P, col_P =  getPieceCoOrd(board, chess.PAWN, chess.WHITE)
    # if pawns on the same file.
    
    r_diff = row_p - row_P
    c_diff = col_p - col_P
    
    if col_p == col_P and row_p > row_P:
        A = sameFilePawn(board)


    # if both passed pawns.
    
    # r_diff should normally be +ve.
    elif abs(c_diff) >= 2 or r_diff < 0:
        A = passedPawns(board)
     
    # if pawns on adjacent files.
    
    else:
        A = adjacentPawns(board)

    
    return A

# For K --> p.
#
# What if I remove every stupid heuristic, and only care about
# getting every option, then prune in isEnd.


# customized methods for targetedCalculation.

# white heuristic --> distance between K and pawn.
# Ideally, should have just returned True or False based
# on a bunch of conditions, and maybe take prev board as well.
# For now, this gives some values, and after some complicated
# mix, it all works out.

# Because of the complicated implementation here, needed to include the
# relaxed distance feature in the implementation of targetCalc --> that slows
# us down further. 
# + we've opposition in targetCalc for some complicated reasons, which might
# cause trouble for it when we generalize to other forms.
# Problem with True <--> False heuristic was that we needed context.
# Particularly <--> previous board. So could say when were moving backwards.



def distKp(board):
    
    row_k, col_k = getPieceCoOrd(board, chess.KING, chess.BLACK)
    row_K, col_K = getPieceCoOrd(board, chess.KING, chess.WHITE)
    # if the piece has been captured, then this should return -1 or 0?!
    row_p, col_p = getPieceCoOrd(board, chess.PAWN, chess.BLACK)
    
    # means it has been captured.
    if row_p == None:
        return -2

    A = (row_K, col_K)
    B = (row_p, col_p)
    dist = kingDistance(A, B)
    
    # adding penalties for the king being on a far off row.
    # Being on a far off column is usually preferrable, than being
    # on a far off row:
    #
    # Seems VERY rare if going backward will be better than going
    # forward, so I'll go ahead and put this here.
    
    # just don't want to do that unless it's a must.
    if abs(row_K - row_p) >= 2:
     #   print 'yes K too low'
        dist += 2
    
    # Adding bonuses for opposition completely fucks it up.
    
    return dist

# Heuristic for black. This guy should be willing to go
# after both the pawns <--> white or black.
# We weren't able to include the relaxed distance feature in
# the 

def distkp(board):
    
    row_k, col_k = getPieceCoOrd(board, chess.KING, chess.BLACK)
    # if the piece has been captured, then this should return -1 or 0?!
    row_p, col_p = getPieceCoOrd(board, chess.PAWN, chess.BLACK)
    row_P, col_P = getPieceCoOrd(board, chess.PAWN, chess.WHITE)    
    # means it has been captured.
    if row_p == None or row_P == None:
        return 0


    k = (row_k, col_k)
    p = (row_p, col_p)
    P = (row_p, col_P)

    A = kingDistance(k, p)
#    return A
    B = kingDistance(k, P)
    return min(A, B)

# check in the results if this is really a big deal.
# RIGHT now we're just returning everything.
#
def black_moves(board):


    old_dist = distkp(board)
    old_coord = getPieceCoOrd(board, chess.KING, chess.BLACK)
    p = getPieceCoOrd(board, chess.PAWN, chess.BLACK)

    moves = []

    legalMoves = board.generate_legal_moves(pawns=False) 
     
    
    for m in legalMoves:
        
        b2 = createNewBoard(board)
        b2.push(m)
        new_dist = distkp(b2)
        new_coord = getPieceCoOrd(b2, chess.KING, chess.BLACK)
      
        # cur_dist and new_dist would take care to remove
        # options that make the king go back.
        
    #    if new_dist <= old_dist:
        if True:
            moves.append((b2, m))
        else:
            if opposition(b2):
                moves.append((b2,m))
            

# do we need this?
#            elif new_coord[0] > old_coord[0]:
#                moves.append((b2,m))

#    return moves

#    moves = []
#    A = []
#            scores = []
    # first check only legalMoves of the king.
#    legalMoves = board.generate_legal_moves(pawns=False)
    
    
    
#    for m in legalMoves:
#        b2 = createNewBoard(board)
#        b2.push(m)
        # add m-to the list of visited_W squares.
        # time to check if b2 improves the situation.
#        A.append((distkp(b2), b2,m))
         
#    best_d = min(A)[0]
    
    # CHECK --- do I really want this for most cases?
    # adding relaxed_d considerably increases runtime here.
#    relaxed_d = best_d

#    for option in A:
#        if option[0] <= relaxed_d:
#                if pflag:
#                   print option[1]
#                    print depth
#               scores.append(V_opt(option[1], depth-1, list(visited_W)))
            
 #           moves.append((option[1], option[2]))
    
    return moves

            # consider all possible pawn moves.

           #     if improves(board, b2):
           #         A.append(V_opt(b2, depth-1))
             
   #         return min(scores)









def white_moves(board):
    
    old_dist = distKp(board)
    old_coord = getPieceCoOrd(board, chess.KING, chess.WHITE)

    moves = []

    pawnMoves = board.generate_legal_moves(king=False, pawns=True)
    for m in pawnMoves:
        b2 = createNewBoard(board)
        b2.push(m)
        moves.append((b2, m)) 
    
    # remaining legal Moves
    legalMoves = board.generate_legal_moves(pawns=False) 
    
    # in visited_W, we don't append every legal move, but we
    # append only those that pass our heuristics.
    
    list = []

    for m in legalMoves:
        b2 = createNewBoard(board)
        b2.push(m)
        new_dist = distKp(b2)
        new_coord = getPieceCoOrd(b2, chess.KING, chess.WHITE)
            
            # cur_dist and new_dist would take care to remove
            # options that make the king go back.

        if old_dist >= new_dist:
  #      if True:
            list.append((new_dist,b2, m))
        else:
            if opposition(b2):
                list.append((new_dist,b2,m))

    #        elif new_coord[0] > old_coord[0]:
    #            moves.append((b2,m))
    
    # Important because ordering makes a big difference here.

    list.sort(key=lambda x: x[0])
    for x in list:
        moves.append((x[1], x[2]))
        # if pawn capture possible, don't
        # consider everything else.
        if x[0] < 0:
            break

    return moves

            # time to check if b2 improves the situation.

# This getScore guy should use the 1p tester if pawn captured,
# else it should just return 0. 
# NEED TO USE A PROPER SCORING --> using test of 1p here.

def getScore(board):
    
    p = board.pieces(chess.PAWN, chess.BLACK)
    P = board.pieces(chess.PAWN, chess.WHITE)

    if len(p) == 0 and len(P) == 1:
        return 10
    else:
        return -10


# we need to send in custom made end functions.
#
# CAN improve this considerably to prune out unneccesary options...
# divide work with the heuristics..but ok no need for now.

def isEnd_samefileP(board):
    
    # condition for end --> pawn Queening.
    p = board.pieces(chess.PAWN, chess.BLACK) 
    P = board.pieces(chess.PAWN, chess.WHITE)

    if len(p) == 0 or len(P) == 0:
        return True
    else:
        return False

# CAN CHANGE STUFF INSIDE TARGETED CALCULATION <--> like the restriction of
# relaxed move etc. But screw it for now.   

# wrapper method for sending targetCalculation for 2 different types of positions.
# Below 5 offers black more drawing chances. 

# We don't really need to make changes to this because if the black k can reach defensive
# spot --> then this wouldn't be called.

def calculate_below5(board):

    
    # test if the piece exists:
    
    # let's say this returns -1 or 1 based on draw or win. Then we can
    # check it with flipped boards, and then decide if it's a draw or win.
    # depth could be the distance of K from P + 2 or something? Or just
    # put up something even bigger.
    score = targetedCalculation(board, white_moves, black_moves, getScore, isEnd_samefileP)
    return score

def calculate_rank5(board):

    
    # test if the piece exists:
    
    # let's say this returns -1 or 1 based on draw or win. Then we can
    # check it with flipped boards, and then decide if it's a draw or win.
    # depth could be the distance of K from P + 2 or something? Or just
    # put up something even bigger.
    score = targetedCalculation(board, white_moves, black_moves, getScore, isEnd_samefileP)
    return score

# just a test function.
def feature_test(board):

    
    # test if the piece exists:
    
    # let's say this returns -1 or 1 based on draw or win. Then we can
    # check it with flipped boards, and then decide if it's a draw or win.
    # depth could be the distance of K from P + 2 or something? Or just
    # put up something even bigger.
    score = targetedCalculation(board, white_moves, black_moves, getScore, isEnd_samefileP, 5)
    print score

## Type 3 --> sameFile.
## wrapper function around two types of it.


def sameFilePawn(board):

    A = {}
    row_P, col_P =  getPieceCoOrd(board, chess.PAWN, chess.WHITE) 
    row_p, col_p =  getPieceCoOrd(board, chess.PAWN, chess.BLACK)

    row_k, col_k =  getPieceCoOrd(board, chess.KING, chess.BLACK)
    row_K, col_K =  getPieceCoOrd(board, chess.KING, chess.WHITE)
    
    kingsReversed = False
    if row_K > row_k:
        kingsReversed = True
    
    
    move = board.turn == chess.WHITE
    
    ## special condition, so if we can move into the
    # 5th rank, then it is also acceptable.
    if move and row_p > 4:
        row_P += 1
    
    ## All these conditions apply to cases where k <--> K 
    # are usually placed. If their sides are reversed, then
    # all we should just call calculation and get done.
    
    # we include kingsReversed here as well, because then the main idea
    # of defence in rank 4 and below doesn't really help.
    if row_P >= 4 or kingsReversed:
        print 'rank 5 and above'
        A = sameFilePawn_rank5(board)
    else:
        print 'rank 4 and below'
        A = sameFilePawn_below5(board)


    return A



## Two different divisions of sameFile:
# first few lines are very similar, and should have 
# been decomposed...

def sameFilePawn_below5(board):

    A = {}
    
    ## do some shit and then update A
    # and return.
    
    move = board.turn == chess.WHITE
    
    row_K, col_K = getPieceCoOrd(board, chess.KING, chess.WHITE)
           
    row_k, col_k = getPieceCoOrd(board, chess.KING, chess.BLACK)
    
    row_P, col_P =  getPieceCoOrd(board, chess.PAWN, chess.WHITE)

    row_p, col_p =  getPieceCoOrd(board, chess.PAWN, chess.BLACK)
    
    # key defensive square:
    
    # +2 because we're increasing upwards.
    key_r = row_p + 2
    key_c = col_p
    k_defense = kingDistance((key_r,key_c), (row_k, col_k))
    
   



    # should just call kingDistance at all these places here:
    # distance to black pawn:    

    K1 = abs(row_K - row_p) 
    K2 = abs(col_K - col_p)
    K_p = max(K1, K2)
    

    k1 = abs(row_k - row_p) 
    k2 = abs(col_k - col_p)
    k_p = max(k1, k2)
    
    # distance to white pawn for black king:
            
    k1 = abs(row_k - row_P) 
    k2 = abs(col_k - col_P)
    k_P = max(k1, k2)
    

    # check heuristic:
    k_d = min(k_P, k_p)
    # consider counterattacking case separately.


    ### --> MAYBE CONSIDER PAWN ON 2nd row as a separate case?
    if move:
        K_p -= 1
    else:
        k_d -= 1
        k_defense -= 1

    d = K_p - k_d
    
    if abs(row_p - row_P) == 1:
        # +1 because black just needs to reach the
        # defensive square, not defend it.
        if k_defense <= (K_p+1):
            A['king close to defensive square'] = 1
            return A



    # keeping a cushion of one move. Negative d implies that
    # king is closer to defence.
    if d < -1:
        A['black king too far to defend, P < 5'] = 1
    elif d > 1:

        A['black king close to defend, P < 5'] = 1
    else:
        result = calculate_below5(board)
    
        if result > 0:
            A['calculate winning'] = 1
        else:
            A['calculate drawing'] = 1

    return A



def sameFilePawn_rank5(board):
    
    A = {}
    # information common to all these functions
    
    # P over 5th rank
    move = board.turn == chess.WHITE
    
    row_K, col_K = getPieceCoOrd(board, chess.KING, chess.WHITE)
             
    row_k, col_k = getPieceCoOrd(board, chess.KING, chess.BLACK)
    
    row_P, col_P =  getPieceCoOrd(board, chess.PAWN, chess.WHITE)

    row_p, col_p =  getPieceCoOrd(board, chess.PAWN, chess.BLACK)
    
    # distance to black pawn:

    K1 = abs(row_K - row_p) 
    K2 = abs(col_K - col_p)
    K_p = max(K1, K2)
    

    k1 = abs(row_k - row_p) 
    k2 = abs(col_k - col_p)
    k_p = max(k1, k2)
    
    # distance to white pawn for black king:
            
    k1 = abs(row_k - row_P) 
    k2 = abs(col_k - col_P)
    k_P = max(k1, k2)
    
    # check heuristic:
    k_d = min(k_P, k_p)
    # consider counterattacking case separately.


    ### --> MAYBE CONSIDER PAWN ON 2nd row as a separate case?
    if move:
        K_p -= 1
    else:
        k_d -= 1
    
    d = K_p - k_d
    
    # means k is much closer.
    if d > 2:
        A['black king much closer'] = 1
    # means K is much closer.
    elif d < -2:
        A['White king much closer'] = 1
    # otherwise call the damned thing.
    else:
        result = calculate_rank5(board)    
    
    if result > 0:
        A['calculate winning'] = 1
    else:
        A['calculate drawing'] = 1

    return A


### Not using it, not sure if it is just junk or not.
# Have similar things in each of the other things.

def basicDistances(board):

    A = {}

    move = board.turn == chess.WHITE
    
    row_K, col_K = getPieceCoOrd(board, chess.KING, chess.WHITE)
             
    row_k, col_k = getPieceCoOrd(board, chess.KING, chess.BLACK)
    
    row_P, col_P =  getPieceCoOrd(board, chess.PAWN, chess.WHITE)

    row_p, col_p =  getPieceCoOrd(board, chess.PAWN, chess.BLACK)
    
    # distance to black pawn:

    K1 = abs(row_K - row_p) 
    K2 = abs(col_K - col_p)
    K_p = max(K1, K2)
    

    k1 = abs(row_k - row_p) 
    k2 = abs(col_k - col_p)
    k_p = max(k1, k2)
    
    # distance to white pawn for black king:
            
    k1 = abs(row_k - row_P) 
    k2 = abs(col_k - col_P)
    k_P = max(k1, k2)
    
    # check heuristic:
#    k_d = min(k_P, k_p)
    # consider counterattacking case separately.


    ### --> MAYBE CONSIDER PAWN ON 2nd row as a separate case?
    if move:
        K_p -= 1
    else:
        k_p -= 1
    
    if row_p >= 5 and row_P >= 4:
        high_P = True
    else:
        high_P = False

    # black's king closer to p should lead to a draw in cases
    # where black's pawn is above 3rd rank.
     
    if k_p <= K_p:
        if not high_P:
            A['blacks king closer to p + no high_P'] = 1
        if high_P:
            A['blacks king closer to p + high_P'] = 1
    else:
        A['whites king closer to p'] = 1

    
    return A
            
# Assumption for the method below --> no pawn gap.
#

# Try basic things, and if they don't work, then
# go ahead and try alpha-beta stuff.




## For simplicity, separate functions for black can catch and white can catch.

## catcher - the king.
## to catch --> the pawn.
## side catching --> white or black.


## Need to be re-done.

def canCatchPawn_black(board): 

    # getPieces, then find the co-ordinates
    # of those pieces.
    #
    
    # move should be true or false;
    move = board.turn == chess.WHITE
    res = getPiece(board, chess.KING, chess.BLACK) 
    

    ## could have used getCoOrd for the methods below.
    if len(res) != 0:
        num = res[0]

    
    row_b_k, col_b_k = getRowAndColumn(num)

    res2 = getPiece(board, chess.PAWN, chess.WHITE)

    if len(res2) != 0:
        num = res2[0]
    
    row_w_p, col_w_p = getRowAndColumn(num)
    
    # pawn on 2nd rank is basically one square ahead.
    if row_w_p == 1:
        row_w_p += 1
    
    ## if black king can catch the pawn. 
    if row_b_k < row_w_p:

        if move:
            return False
        if row_w_p - row_b_k > 1:
            return False
    
    # checking from columns perspective.
    moves_to_end = 7 - row_w_p
    moves_to_catch = abs(col_w_p - col_b_k) - 1

    if moves_to_end < moves_to_catch:
        return False

    if moves_to_end == moves_to_catch:
        if move:
            return False
    
    ## if it has reached this point, it means that the king can catch the pawn.
    ## now time to check with the opponent king.
    
    res = getPiece(board, chess.KING, chess.WHITE) 
    
    if len(res) != 0:
        num = res[0]

    
    row_w_k, col_w_k = getRowAndColumn(num)
    
    moves_to_defend = abs(col_w_p - col_w_k) - 1
    
    opp_side = col_w_k > col_w_p and col_b_k < col_w_p or col_w_k < col_w_p and col_b_k > col_w_k
    same_row = row_w_k == row_b_k
    
    # maybe add higher row instead here?

    # update how far the king is, and also the same_row check
    # if white is to move.

    if move:
        moves_to_defend -= 1
        same_row = abs(row_w_k - row_b_k) <= 1 
        

        ## will need to ADD MORE TESTS HERE BASED ON RANK    
    if moves_to_defend <= moves_to_catch and not opp_side:
        return False

    # we can assume they are on the opposite side for the next thing
    if moves_to_defend <= moves_to_catch and same_row:
        return False


    return True

def canCatchPawn_white(board):
    
    

    # getPieces, then find the co-ordinates
    # of those pieces.
    #
    
    # move should be true or false;
    move = board.turn == chess.BLACK
    res = getPiece(board, chess.KING, chess.WHITE) 
    


    if len(res) != 0:
        num = res[0]

    
    row_w_k, col_w_k = getRowAndColumn(num)

    res2 = getPiece(board, chess.PAWN, chess.BLACK)

    if len(res2) != 0:
        num = res2[0]
    
    row_b_p, col_b_p = getRowAndColumn(num)
    
    if row_b_p == 6:
        row_b_p -= 1

    if row_w_k > row_b_p:

        if move:
            return False
        if abs(row_b_p - row_w_k) > 1:
            return False
    

    moves_to_end = row_b_p
    moves_to_catch = abs(col_b_p - col_w_k) - 1

    if moves_to_end < moves_to_catch:
        return False

    if moves_to_end == moves_to_catch:
        if move:
            return False

    ## if it has reached this point, it means that the king can catch the pawn.
    ## now time to check with the opponent king.
    
    res = getPiece(board, chess.KING, chess.BLACK) 
    
    if len(res) != 0:
        num = res[0]

    
    row_b_k, col_b_k = getRowAndColumn(num)
    
    moves_to_defend = abs(col_b_p - col_b_k) - 1
    
    same_row = row_w_k == row_b_k
    
    # update how far the king is, and also the same_row check
    # if white is to move.

    if move:
        moves_to_defend -= 1
        same_row = abs(row_w_k - row_b_k) <= 1 
        

    if moves_to_defend <= moves_to_catch and same_row:
        return False


    return True



def canCatchPawn(FEN):
    
    print 'starting can catch pawn'
    print FEN
    # we want to keep FEN, so we can create new boards for pawn
    # races etc.
    
    board = chess.Board(FEN)
    A = {}
    
    white_can_catch = canCatchPawn_white(board)
    black_can_catch = canCatchPawn_black(board)


    if canCatchPawn_white(board):
        print 'white can catch the pawn'
        A['white can catch pawn'] = 1
    else:
        print 'white cant catch the pawn'
        A['white cant catch pawn'] = 1
    
    if canCatchPawn_black(board):
        print 'black can catch the pawn'
        A['black can catch pawn'] = 1
    else:
        print 'black cant catch the pawn'
        A['black cant catch pawn'] = 1

    



    return A










#### one-pawn Features below ---> old ones.


## checks if after changing n+1,n-1
# etc, the new n should be somewhere
# around the old n.
# It could either go out of the board,
# or on the corner column - both are bad.

def outofRange(n):

    if n > 63 or n < 0:
        return True
    
    edge = n % 8
    if edge == 7 or edge == 0:
        return True

    return False

# will check if the white king can reach n or not.
# white king will only be able to reach n if it is
# attacking that, and the black king isn't.
# Just for KPvsk endgames

def canDefend(board, n):
    
    black_attack = board.is_attacked_by(chess.BLACK, n)
    white_attack = board.is_attacked_by(chess.WHITE, n) 
    
    if white_attack and not black_attack:
        return True
    
    return False

# Might test by increasing the feature value for black can capture/
def canBeCaptured_helper(board):

    # We know it's only one so far, so don't have to do anymore.
    move = board.turn == chess.WHITE
    

    # P is the position number of the pawn.
    P = getPiece(board,chess.PAWN, chess.WHITE)[0]
    black_attack = board.is_attacked_by(chess.BLACK, P)
    
    # if P is in the 2nd rank, then return False.
    
    if P <= 15:
        return False



    # just to reduce cases we need to check
    if not black_attack:
        return False

    white_attack = board.is_attacked_by(chess.WHITE, P) 
    
    if not move:
        if black_attack and not white_attack:
            return True

    else:
        # just make each case separately:
        
        # start from row above and then cover all three rows.
        N = P + 8
        for i in range(3):
            
            left = N - 1
            mid = N # Don't have to check this because no case when this will be accessible and others wont be.
            right = N + 1
            
            if not outofRange(left) and canDefend(board, left):
                return False
            
            if not outofRange(right) and canDefend(board, right):
                return False
    
            N -= 8

        # I guess second condition is redundant because if it were
        # true, then would have returned false already
        if black_attack and not white_attack:
            return True
        

def canBeCaptured(board):
    
    # We know it's only one so far, so don't have to do anymore.
    A = {}
    if canBeCaptured_helper(board):
        A['black_can_capture'] = 1
    
    return A

def isWhiteKingAhead(board):
   
    A = {}
    row_K, col_K = getPieceCoOrd(board, chess.KING, chess.WHITE)
             
    row_p, col_p = getPieceCoOrd(board, chess.PAWN, chess.WHITE)
    
    if row_K > row_p:
        if abs(col_K - col_p) <= 1:
            A['white king ahead'] = 1
    
#    elif row_K < row_p:


    return A

def ishPawn(board):
    
    A = {}
    row_p, col_p = getPieceCoOrd(board, chess.PAWN, chess.WHITE)
    if col_p == 7 or col_p == 0:
        A['h_pawn'] = 1

    return A

# needs to return who has the opposition as well.
# tupe - (true, BLACK)

def isOpposition(board):
    
    A = {}
    move = board.turn == chess.WHITE
        
    row_K, col_K = getPieceCoOrd(board, chess.KING, chess.WHITE)
             
    row_k, col_k = getPieceCoOrd(board, chess.KING, chess.BLACK)

    if col_K == col_k:
        if row_K == row_k - 2:
            if move:
                A['black_opposition'] = 1
            else:
                A['white_opposition'] = 1

    return A

## Need to decide whether we should keep minimum column 
# distance = 2 or not.

def wrongSide(board):
    
    A = {}

    K = getPieceCoOrd(board, chess.KING, chess.WHITE)         
    k = getPieceCoOrd(board, chess.KING, chess.BLACK) 
    P = getPieceCoOrd(board, chess.PAWN, chess.WHITE)
    
    # K[1] is the column.
    
    # both on same side of the pawn:
    if K[1] > P[1] and k[1] > P[1]:
        
        # K[1] < k[1] means white king is closer.
        




        if K[1] < k[1]:
            
            A['black_king_wrong_side'] = 1

        elif K[1] > k[1]:

            A['white_king_wrong_side'] = 1
            
            if abs(K[0] - k[0]) <= 1:

                A['white_king_blocked'] = 1
    
   
    elif K[1] < P[1] and k[1] < P[1]:
        
        if K[1] < k[1]:

            A['white_king_wrong_side'] = 1
            
            if abs(K[0] - k[0]) <= 1:

                A['white_king_blocked_side'] = 1
                
        elif K[1] > k[1]:
            
            A['black_king_wrong_side'] = 1
     
    ## time to check the rows:
    # if black king is blocking the white king via
    # rows:
    
    if K[0] > P[0] and k[0] > P[0]:

        # if black king is blocking the white king:

        if abs(k[1] - P[1]) <= abs(K[1] - P[1]):

            if k[0] < K[0]:

                A['white_king_blocked_down'] = 1


#    if K[0] < P[0] and k[0] > P[0]:
#        A['white_king_behind'] = 1
#    elif K[0] > P[0] and k[0] < P[0]:
#        A['white_king_ahead'] = 1



    return A

## returns the dist k-P - K-P.
# So if it's positive, then it's a good thing for us, 
# while if it's negative, that's a bad thing.
# Weights should figure that out hopefully.

## Also, deal with pawn on 6th rank here.

# helper function, closer to winning square:
# Meh, make it later.

def move_distances(board):
    
    A = {}

    move = board.turn == chess.WHITE
    
    row_K, col_K = getPieceCoOrd(board, chess.KING, chess.WHITE)
             
    row_k, col_k = getPieceCoOrd(board, chess.KING, chess.BLACK)
    
    row_P, col_P =  getPieceCoOrd(board, chess.PAWN, chess.WHITE)
    
    # because the key square in this fight is the square right above the pawn.
    # Do we really need to do error checking for this?!
    row_P += 1


    assert(row_P != None)

    K1 = abs(row_K - row_P) 
    K2 = abs(col_K - col_P)
    K_d = max(K1, K2)

    k1 = abs(row_k - row_P) 
    k2 = abs(col_k - col_P)
    k_d = max(k1, k2)
    
    if move:
        K_d -= 1
    else:
        k_d -= 1

    # less than equal to because if they both reach it at same time,
    # I guess we should consider white king closer?!
    
    ## Maybe should give this greater value?

    if K_d <= k_d:
        
        A['white_king_closer'] = 1

        

    else:

        A['black_king_closer'] = 1
    
    # Winning squares right above:

    col_P -= 1
    
    # so it's not an illegal square
    if col_P < 8 or col_P >= 0:
        
        ## A lot of repeated shit here:

        K1 = abs(row_K - row_P) 
        K2 = abs(col_K - col_P)
        K_d = max(K1, K2)

        k1 = abs(row_k - row_P) 
        k2 = abs(col_k - col_P)
        k_d = max(k1, k2)
        
        if move:
            K_d -= 1
        else:
            k_d -= 1

        # less than equal to because if they both reach it at same time,
        # I guess we should consider white king closer?!
        
        # Adding a return here, because then we don't even need to check the rest/.    
        if K_d <= k_d:
            
            A['white_king_closer_to_winning_square'] = 1
            return A

        else:

            A['black_king_closer_to_winning_square'] = 1



    # Winning square on the other side:

    col_P += 2
    
    # SHould really DECOMPOSE THIS IF I WASN"T AN IDIOT>
    # so it's not an illegal square

    if col_P < 8 or col_P >= 0:
        
        ## A lot of repeated shit here:

        K1 = abs(row_K - row_P) 
        K2 = abs(col_K - col_P)
        K_d = max(K1, K2)

        k1 = abs(row_k - row_P) 
        k2 = abs(col_k - col_P)
        k_d = max(k1, k2)
        
        if move:
            K_d -= 1
        else:
            k_d -= 1

        # less than equal to because if they both reach it at same time,
        # I guess we should consider white king closer?!

        if K_d <= k_d:
            
            A['white_king_closer_to_winning_square'] = 1

        else:

            A['black_king_closer_to_winning_square'] = 1
    
    return A
    






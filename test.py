#!/usr/bin/env python

from flask import Flask
from flask import render_template
from flask import current_app
from flask import redirect
from flask import request
from flask import url_for
from flask import jsonify
from flask import send_from_directory

from werkzeug.exceptions import BadRequest

import chess
import chess.syzygy
import chess.gaviota

import functools
import os.path
import warnings
import json


FEN_TEST = "8/8/2k5/8/4R3/8/8/4K3 w - - 0 1"
DEFAULT_FEN = "4k3/8/8/8/8/8/8/4K3 w - - 0 1"


app = Flask(__name__)

syzygy = chess.syzygy.Tablebases()
num = 0
num += syzygy.open_directory(os.path.join(os.path.dirname(__file__), "four-men"))
num += syzygy.open_directory(os.path.join(os.path.dirname(__file__), "five-men"))
num += syzygy.open_directory(os.path.join(os.path.dirname(__file__), "six-men", "wdl"), load_dtz=False)
num += syzygy.open_directory(os.path.join(os.path.dirname(__file__), "six-men", "dtz"), load_wdl=False)
app.logger.info("Loaded %d tablebase files.", num)

gaviota = chess.gaviota.open_tablebases(os.path.join(os.path.dirname(__file__), "gaviota"))


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

def clear_fen(fen):
    parts = fen.split()
    return DEFAULT_FEN.replace("w", parts[1])


def material(board):
    name = ""
    name += "K" * chess.pop_count(board.kings & board.occupied_co[chess.WHITE])
    name += "Q" * chess.pop_count(board.queens & board.occupied_co[chess.WHITE])
    name += "R" * chess.pop_count(board.rooks & board.occupied_co[chess.WHITE])
    name += "B" * chess.pop_count(board.bishops & board.occupied_co[chess.WHITE])
    name += "N" * chess.pop_count(board.knights & board.occupied_co[chess.WHITE])
    name += "P" * chess.pop_count(board.pawns & board.occupied_co[chess.WHITE])
    name += "v"
    name += "K" * chess.pop_count(board.kings & board.occupied_co[chess.BLACK])
    name += "Q" * chess.pop_count(board.queens & board.occupied_co[chess.BLACK])
    name += "R" * chess.pop_count(board.rooks & board.occupied_co[chess.BLACK])
    name += "B" * chess.pop_count(board.bishops & board.occupied_co[chess.BLACK])
    name += "N" * chess.pop_count(board.knights & board.occupied_co[chess.BLACK])
    name += "P" * chess.pop_count(board.pawns & board.occupied_co[chess.BLACK])
    return name




def probe(board):
    moves = {}

    # The best move will be determined in this order.
    mating_move = None
    zeroing_move = None
    winning_move, winning_dtz = None, -9999
    stalemating_move = None
    insuff_material_move = None
    drawing_move = None
    losing_move, losing_dtz = None, -9999
    losing_zeroing_move, losing_zeroing_dtz = None, -9999

    # Look at all moves and probe for the result position.
    for move in board.legal_moves:
        uci_move = board.uci(move)
        board.push(move)

        dtz = syzygy.probe_dtz(board)
        dtm = gaviota.probe_dtm(board)

        moves[uci_move] = {
            "dtz": dtz,
            "dtm": dtm,
        }

        # Mate.
        if board.is_checkmate():
            mating_move = uci_move

        # Winning zeroing move.
        if dtz is not None and dtz < 0 and board.halfmove_clock == 0:
            zeroing_move = uci_move

        # Winning move.
        if dtz is not None and dtz < 0 and dtz > winning_dtz:
            winning_move = uci_move
            winning_dtz = dtz

        # Stalemating move.
        if board.is_stalemate():
            stalemating_move = uci_move

        # Insufficient material.
        if board.is_insufficient_material():
            insuff_material_move = uci_move

        # Drawing move.
        if dtz is not None and dtz == 0:
            drawing_move = uci_move

        # Losing move.
        if dtz is not None and board.halfmove_clock != 0 and dtz > losing_dtz:
            losing_move = uci_move
            losing_dtz = dtz

        # Losing move.
        if dtz is not None and dtz > losing_zeroing_dtz:
            losing_zeroing_move = uci_move
            losing_zeroing_dtz = dtz

        board.pop()

    return {
        "dtz": syzygy.probe_dtz(board),
        "wdl": syzygy.probe_wdl(board),
        "dtm": gaviota.probe_dtm(board),
        "bestmove": mating_move or zeroing_move or winning_move or stalemating_move or insuff_material_move or drawing_move or losing_move or losing_zeroing_move,
        "moves": moves,
    }

def index():
    # Setup a board from the given valid FEN or fall back to the default FEN.
    board = chess.Board(DEFAULT_FEN)

    # Get FENs with the current side to move, black and white to move.
    original_turn = board.turn
    board.turn = chess.WHITE
    white_fen = board.fen()
    board.turn = chess.BLACK
    black_fen = board.fen()
    board.turn = original_turn
    fen = board.fen()

    wdl = None
    winning_side = None
    winning_moves = []
    drawing_moves = []
    losing_moves = []

    if not board.is_valid():
        status = "Invalid position"
    elif board.is_stalemate():
        status = "Draw by stalemate"
        wdl = 0
    elif board.is_checkmate():
        wdl = 2
        if board.turn == chess.WHITE:
            status = "Black won by checkmate"
            winning_side = "black"
        else:
            status = "White won by checkmate"
            winning_side = "white"
    else:
        wdl = syzygy.probe_wdl(board)
        dtz = syzygy.probe_dtz(board)
        if board.is_insufficient_material():
            status = "Draw by insufficient material"
            wdl = 0
        elif dtz is None:
            status = "Position not found in tablebases"
        elif dtz == 0:
            status = "Tablebase draw"
        elif dtz > 0 and board.turn == chess.WHITE:
            status = "White is winning with DTZ %d" % (abs(dtz), )
            winning_side = "white"
            losing_side = "black"
        elif dtz < 0 and board.turn == chess.WHITE:
            status = "White is losing with DTZ %d" % (abs(dtz), )
            winning_side = "black"
            losing_side = "white"
        elif dtz > 0 and board.turn == chess.BLACK:
            status = "Black is winning with DTZ %d" % (abs(dtz), )
            winning_side = "black"
            losing_side = "white"
        elif dtz < 0 and board.turn == chess.BLACK:
            status = "Black is losing with DTZ %d" % (abs(dtz), )
            winning_side = "white"
            losing_side = "black"

        for move in board.legal_moves:
            san = board.san(move)
            uci = board.uci(move)
            board.push(move)

            move_info = {
                "uci": uci,
                "san": san,
                "fen": board.epd() + " 0 1",
                "dtz": syzygy.probe_dtz(board),
                "dtm": gaviota.probe_dtm(board),
                "zeroing": board.halfmove_clock == 0,
                "checkmate": board.is_checkmate(),
                "stalemate": board.is_stalemate(),
                "insufficient_material": board.is_insufficient_material(),
            }

            move_info["dtm"] = abs(move_info["dtm"]) if move_info["dtm"] is not None else None

            move_info["winning"] = move_info["checkmate"] or (move_info["dtz"] is not None and move_info["dtz"] < 0)
            move_info["drawing"] = move_info["stalemate"] or move_info["insufficient_material"] or (move_info["dtz"] == 0 or (move_info["dtz"] is None and wdl is not None and wdl < 0))

            if move_info["winning"]:
                if move_info["checkmate"]:
                    move_info["badge"] = "Checkmate"
                elif move_info["zeroing"]:
                    move_info["badge"] = "Zeroing"
                else:
                    move_info["badge"] = "Win with DTZ %d" % (abs(move_info["dtz"]), )

                winning_moves.append(move_info)
            elif move_info["drawing"]:
                if move_info["stalemate"]:
                    move_info["badge"] = "Stalemate"
                elif move_info["insufficient_material"]:
                    move_info["badge"] = "Insufficient material"
                elif move_info["dtz"] == 0:
                    move_info["badge"] = "Draw"
                else:
                    move_info["badge"] = "Unknown"

                drawing_moves.append(move_info)
            else:
                if move_info["dtz"] is None:
                    move_info["badge"] = "Unknown"
                elif move_info["zeroing"]:
                    move_info["badge"] = "Zeroing"
                else:
                    move_info["badge"] = "Loss with DTZ %d" % (abs(move_info["dtz"]), )
                losing_moves.append(move_info)

            board.pop()

    winning_moves.sort(key=lambda move: move["uci"])
    winning_moves.sort(key=lambda move: (move["dtm"] is None, move["dtm"]))
    winning_moves.sort(key=lambda move: (move["dtz"] is None, move["dtz"]), reverse=True)
    winning_moves.sort(key=lambda move: move["zeroing"], reverse=True)
    winning_moves.sort(key=lambda move: move["checkmate"], reverse=True)

    drawing_moves.sort(key=lambda move: move["uci"])
    drawing_moves.sort(key=lambda move: move["insufficient_material"], reverse=True)
    drawing_moves.sort(key=lambda move: move["stalemate"], reverse=True)

    losing_moves.sort(key=lambda move: move["uci"])
    losing_moves.sort(key=lambda move: (move["dtm"] is not None, move["dtm"]), reverse=True)
    losing_moves.sort(key=lambda move: (move["dtz"] is None, move["dtz"]), reverse=True)
    losing_moves.sort(key=lambda move: move["zeroing"])

    return html_minify(render_template("index.html",
        fen_input=board.epd() + " 0 1" if board.epd() + " 0 1" != DEFAULT_FEN else "",
        fen=fen,
        status=status,
        insufficient_material=board.is_insufficient_material(),
        winning_side=winning_side,
        winning_moves=winning_moves,
        drawing_moves=drawing_moves,
        losing_moves=losing_moves,
        blessed_loss=wdl == -1,
        cursed_win=wdl == 1,
        illegal=not board.is_valid(),
        not_yet_solved=board.epd() + " 0 1" == chess.STARTING_FEN,
        unknown=wdl is None,
        turn="white" if board.turn == chess.WHITE else "black",
        white_fen=white_fen,
        black_fen=black_fen,
        horizontal_fen=mirror_horizontal(fen),
        vertical_fen=mirror_vertical(fen),
        swapped_fen=swap_colors(fen),
        clear_fen=clear_fen(fen),
        DEFAULT_FEN=DEFAULT_FEN,
        material=material(board)
    ))





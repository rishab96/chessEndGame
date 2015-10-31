#!/usr/bin/env python

#from flask import Flask
#from flask import render_template
#from flask import current_app
#from flask import redirect
#from flask import request
#from flask import url_for
#from flask import jsonify
#from flask import send_from_directory

#from werkzeug.exceptions import BadRequest

import chess
import chess.syzygy
import chess.gaviota

import functools
import os.path
import warnings
import json


FEN_TEST = "8/8/2k5/8/4R3/8/8/4K3 w - - 0 1"
DEFAULT_FEN = "4k3/8/8/8/8/8/8/4K3 w - - 0 1"


#app = Flask(__name__)

syzygy = chess.syzygy.Tablebases()
num = 0
num += syzygy.open_directory(os.path.join(os.path.dirname(__file__), "four-men"))
num += syzygy.open_directory(os.path.join(os.path.dirname(__file__), "five-men"))
num += syzygy.open_directory(os.path.join(os.path.dirname(__file__), "six-men", "wdl"), load_dtz=False)
num += syzygy.open_directory(os.path.join(os.path.dirname(__file__), "six-men", "dtz"), load_wdl=False)

#app.logger.info("Loaded %d tablebase files.", num)

#gaviota = chess.gaviota.open_tablebases(os.path.join(os.path.dirname(__file__), "gaviota"))


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



print("Something works....")
board = chess.Board(FEN_TEST)
print(board)

print('now we try to get dtz: ')
A = syzygy.probe_dtz(board)
B = syzygy.probe_wdl(board)
print A
print B

print('going after material extraction: ')
Material = material(board)
print Material

print("Something works part 2....")
board = chess.Board(DEFAULT_FEN)
print(board)

print('now we try to get dtz: ')
A = syzygy.probe_dtz(board)
B = syzygy.probe_wdl(board)
print A
print B

print('going after material extraction: ')
Material = material(board)
print Material


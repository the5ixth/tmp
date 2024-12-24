import chess
import requests
import json
import random

G_api = "https://api.openchess.io/move"

board = chess.Board()


def sendMove(move,startFen):
    payload = {"move": move, "fen": startFen}
    response = requests.post(G_api, json=payload)
    j_data = json.loads(response.content)
    resultFen = j_data['fen']
    return resultFen

def calcBoard(fen):
    curBoard = chess.Board(fen)
    stripped = curBoard.fen().split(" ")[0]
    white = 0
    black = 0
    for char in stripped:
        if char == 'P':
            white += 10
        elif char == 'R':
            white += 50
        elif char == 'N' or char == 'K':
            white += 30
        elif char == 'Q':
            white += 90
        elif char == 'K':
            white += 200
        elif char == 'p':
            black += 10
        elif char == 'r':
            black += 50
        elif char == 'n' or char == 'k':
            black += 30
        elif char == 'q':
            black += 90
        elif char == 'k':
            black += 200
    score = white - black
    
    return score

#white
def pickBestMove(moveList, fen):
    # does not pick the best move
    curBoard = chess.Board(fen)
    score = calcBoard(curBoard.fen())

    highscore= 0 - 9999
    bestUCI = ""

    #iterate through al white legal moves
    for move in board.legal_moves:
        curBoard = chess.Board(fen)
        curBoard.push_uci(move.uci())
        #calc all black moves
        for bMove in curBoard.legal_moves:
            bBoard = chess.Board(curBoard.fen())
            bBoard.push_uci(bMove.uci())
            tmpscore = calcBoard(curBoard.fen()) 

            if tmpscore > highscore:
                highscore = tmpscore
                bestUCI = move.uci()


    return bestUCI



while (True):
 
    print('\033[1;1H')
    print("\033[2J")
    move_list = list(board.legal_moves)
    score = calcBoard(board.fen())
    print( score) 
    #next_move = random.choice(move_list)
    uci = pickBestMove(move_list, board.fen())

    f = board.fen()

    #uci = next_move.uci()
    board.push_uci(uci)
    print(board)

    resultFen = sendMove(uci,f)
    board = chess.Board(resultFen)
    
    #print('\033[1;1H')
    #print("\033[2J")
    print(board)

    if board.is_checkmate():
        print("game over")
        exit()






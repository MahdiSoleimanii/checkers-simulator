import copy
from game_logic import *

def start(board: GameBoard, depth: int):
    movable_pieces = {}
    white_pieces = board.get_white_pieces()
    for piece in white_pieces:
        if board.piece_can_move(white_pieces[piece]):
            movable_pieces[white_pieces[piece]] = board.piece_can_move(white_pieces[piece])

    boards = []
    points = []
    for piece in movable_pieces.keys():
        for pos in movable_pieces[piece]:
            piece_copy = copy.deepcopy(piece)
            board_copy = copy.deepcopy(board)
            board_copy.move(piece_copy, pos)
            points.append(evaluate_board(board_copy, depth))
            boards.append(board_copy)
    for i in range(len(points)):
        if points[i] == max(points):
            return boards[i]
    
def evaluate_board(board: GameBoard, depth: int):
    if depth == 0 or board.game_ended():
        return simple_evaluation(board)
            
    best_value = float('-inf')
    value = minimax(board, depth, True)
    best_value = max(best_value, value)

    return best_value

def simple_evaluation(board: GameBoard):
    SOLDIER_VALUE = 1
    KING_VALUE = 2
    eval_score = 0
    
    for piece in board.get_black_pieces().values():
        eval_score -= SOLDIER_VALUE if piece.is_soldier() else KING_VALUE
    
    for piece in board.get_white_pieces().values():
        eval_score += SOLDIER_VALUE if piece.is_soldier() else KING_VALUE

    return eval_score


def minimax(board: GameBoard, depth: int, isMaximizing: bool):
    if depth == 0 or board.game_ended():
        return simple_evaluation(board)
    
    if isMaximizing:
        black_pieces = board.get_black_pieces()
        legal_moves = {}
        max_eval = float('-inf')
        for piece in black_pieces:
            legal_moves[black_pieces[piece]] = board.piece_can_move(black_pieces[piece])
        for piece in legal_moves:
            for pos in legal_moves[piece]:
                board_copy = copy.deepcopy(board)
                piece_copy = copy.deepcopy(piece)
                board_copy.move(piece_copy, pos)
                eval = minimax(board_copy, depth - 1, False)
                max_eval = max(max_eval, eval)
        return max_eval
    else:
        white_pieces = board.get_white_pieces()
        legal_moves = {}
        min_eval = float('inf')
        for piece in white_pieces:
            legal_moves[white_pieces[piece]] = board.piece_can_move(white_pieces[piece])
        for piece in legal_moves:
            for pos in legal_moves[piece]:
                board_copy = copy.deepcopy(board)
                piece_copy = copy.deepcopy(piece)
                board_copy.move(piece_copy, pos)
                eval = minimax(board_copy, depth - 1, True)
                min_eval = min(min_eval, eval)
        return min_eval

gboard = GameBoard()

gboard.print_board()

result = start(gboard, 3)

result.print_board()
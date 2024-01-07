import copy
from game_log import *

def evaluate_board(board: GameBoard, depth: int):
    if depth == 0 or board.game_ended():
        return simple_evaluation(board)

    movable_pieces = []
    white_pieces = board.get_white_pieces()
    for piece in white_pieces:
        if board.piece_can_move(white_pieces[piece]):
            movable_pieces.append(white_pieces[piece])
            
    best_value = float('-inf')
    for piece in movable_pieces:
        board_copy = copy.deepcopy(board)
        piece_copy = copy.deepcopy(piece)
        value = minimax(board_copy, depth - 1, piece_copy)
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


def minimax(board: GameBoard, depth: int, piece: Piece):
    # print(depth)
    # print(piece.info())
    # print(simple_evaluation(board))
    # print()
    
    if depth == 0 or board.game_ended():
        return simple_evaluation(board)

    legal_moves = board.piece_can_move(piece)
    if piece.get_color() != 'B':
        max_eval = float('-inf')
        for new_pos in legal_moves:
            board_copy = copy.deepcopy(board)
            piece_copy = copy.deepcopy(piece)
            board_copy.move(piece_copy, new_pos)
            # print(piece_copy.info(), simple_evaluation(board_copy))
            # print()
            black_pieces = board_copy.get_black_pieces()
            for bpiece in black_pieces:
                if board_copy.piece_can_move(black_pieces[bpiece]):
                    eval = minimax(board_copy, depth - 1, black_pieces[bpiece])
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for new_pos in legal_moves:
            board_copy = copy.deepcopy(board)
            piece_copy = copy.deepcopy(piece)
            board_copy.move(piece_copy, new_pos)
            # print(piece_copy.info(), simple_evaluation(board_copy))
            # print()
            white_pieces = board_copy.get_white_pieces()
            for wpiece in white_pieces:
                if board_copy.piece_can_move(white_pieces[wpiece]):
                    eval = minimax(board_copy, depth - 1, white_pieces[wpiece])
                    min_eval = min(min_eval, eval)
        return min_eval


gboard = GameBoard()

result = evaluate_board(gboard, depth=5)
print("Evaluation Result:", result)

def print_board(board):
        matrix = board.get_matrix()
        for row in matrix:
            print(" ".join([cell.get_color() if not cell.is_empty() else '.' for cell in row]))
        print()
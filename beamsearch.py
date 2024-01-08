import copy
from game_algo import *
from game_logic import *


def beam_search(board, depth, beam_width, alpha, beta):
    movable_pieces = {}
    white_pieces = board.get_white_pieces()

    for piece in white_pieces:
        if board.piece_can_move(white_pieces[piece]):
            movable_pieces[white_pieces[piece]] = board.piece_can_move(white_pieces[piece])

    beam_states = [(copy.deepcopy(board), 0)]

    for _ in range(depth):
        next_beam_states = []

        for board_state, _ in beam_states:
            for piece in movable_pieces.keys():
                for pos in movable_pieces[piece]:
                    new_board = copy.deepcopy(board_state)
                    new_piece = copy.deepcopy(piece)
                    new_board.move(new_piece, pos)

                    eval_score = evaluate_board_alpha_beta(new_board, depth, alpha, beta)
                    next_beam_states.append((new_board, eval_score))


                    alpha = max(alpha, eval_score)
                    

        next_beam_states.sort(key=lambda x: x[1], reverse=True)
        beam_states = next_beam_states[:beam_width]

    return beam_states[0][0]

def evaluate_board_alpha_beta(board, depth, alpha, beta):
    if depth == 0 or board.game_ended():
        return simple_evaluation(board)

    best_value = float('-inf')
    for piece, moves in board.get_white_pieces().items():
        for move in moves:
            board_copy = copy.deepcopy(board)
            piece_copy = copy.deepcopy(piece)
            board_copy.move(piece_copy, move)
            value = -evaluate_board_alpha_beta(board_copy, depth - 1, -beta, -alpha)
            best_value = max(best_value, value)
            alpha = max(alpha, value)
            
    return best_value

def start_beam_search(board: GameBoard, depth: int, beam_width: int):
    movable_pieces = {}
    white_pieces = board.get_white_pieces()
    for piece in white_pieces:
        if board.piece_can_move(white_pieces[piece]):
            movable_pieces[white_pieces[piece]] = board.piece_can_move(white_pieces[piece])

    beams = []
    for piece in movable_pieces.keys():
        for pos in movable_pieces[piece]:
            piece_copy = copy.deepcopy(piece)
            board_copy = copy.deepcopy(board)
            board_copy.move(piece_copy, pos)
            eval_score = evaluate_board_alpha_beta(board_copy, depth, float('-inf'), float('inf'))
            beams.append((board_copy, eval_score))

    beams.sort(key=lambda x: x[1], reverse=True)
    best_beam = beams[0][0]

    result = beam_search(best_beam, depth, beam_width, float('-inf'), float('inf'))
    return result

gboard = GameBoard()

result = start_beam_search(gboard, depth=5000, beam_width=15)

result.print_board()

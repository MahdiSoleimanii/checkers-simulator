from game_logic import *

def evaluate_board(board, depth):
    if depth == 0 or board.game_ended():
        print("Evaluated Board:")
        print_board(board)
        return simple_evaluation(board)

    legal_moves = get_legal_moves(board, maximizing_player=True)
    best_value = float('-inf')

    for move in legal_moves:
        new_board = make_move(board, move) 
        value = minimax(new_board, depth - 1, maximizing_player=False, alpha=float('-inf'), beta=float('inf'))
        best_value = max(best_value, value)

    print("Evaluated Board:")
    print_board(board)
    return best_value


def simple_evaluation(board):
    SOLDIER_VALUE = 1
    KING_VALUE = 2
    eval_score = 0

    # Evaluate the board based on piece positions and types
    for piece_pos, piece in board.get_black_pieces().items():
        eval_score -= SOLDIER_VALUE if piece.is_soldier() else KING_VALUE

    for piece_pos, piece in board.get_white_pieces().items():
        eval_score += SOLDIER_VALUE if piece.is_soldier() else KING_VALUE

    return eval_score


def minimax(board, depth, maximizing_player, alpha, beta):
    if depth == 0 or board.game_ended():
        return simple_evaluation(board)

    legal_moves = get_legal_moves(board, maximizing_player)

    if maximizing_player:
        max_eval = float('-inf')
        for move in legal_moves:
            print(f"Maximizing player exploring move: {move}")
            new_board = make_move(board, move)
            eval = minimax(new_board, depth - 1, False, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                print("Pruning!")
                break  # Alpha-beta pruning
        return max_eval
    else:
        min_eval = float('inf')
        for move in legal_moves:
            print(f"Minimizing player exploring move: {move}")
            new_board = make_move(board, move)
            eval = minimax(new_board, depth - 1, True, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                print("Pruning!")
                break  # Alpha-beta pruning
        return min_eval


def get_legal_moves(board, maximizing_player):
    legal_moves = []
    pieces = board.get_black_pieces() if maximizing_player else board.get_white_pieces()

    for piece_pos, piece in pieces.items():
        moves = board.piece_can_move(piece)
        for move in moves:
            legal_moves.append((piece_pos, move))

    return legal_moves


def make_move(board, move):
    piece_pos, new_pos = move
    piece = board.get_black_pieces().get(piece_pos) or board.get_white_pieces().get(piece_pos)

    if piece is not None and new_pos in board.piece_can_move(piece):
        print(f"Making move: {move}")
        board.move_by_pos(piece_pos, new_pos)

    return board



gboard = GameBoard()
print("Initial Board:")
for row in gboard.get_matrix():
    for cell in row:
        print(f"{not cell.is_empty(): <3}", end=' ')
    print()
print('-' * 20)

result = evaluate_board(gboard, depth=3)
print("Evaluation Result:", result)

def print_board(board):
        matrix = board.get_matrix()
        for row in matrix:
            print(" ".join([cell.get_color() if not cell.is_empty() else '.' for cell in row]))
        print()  
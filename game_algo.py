import copy
import time
from game_logic import *

class Checkers:
    def __init__(self, game_board: GameBoard, white_depth: int, black_depth: int, beam_width: int):
        self.game_board = game_board
        self.SOLDIER_SCORE = 1
        self.KING_SCORE = 2
        self.WHITE_DEPTH = white_depth
        self.BLACK_DEPTH = black_depth
        self.BEAM_WIDTH = beam_width
    
    def heuristic(self, board: GameBoard, player: str):
        eval_score = 0
        player_pieces = board.get_black_pieces() if player == 'B' else board.get_white_pieces()
        enemy_pieces = board.get_white_pieces() if player == 'B' else board.get_black_pieces()
        
        for piece in enemy_pieces:
            eval_score -= self.SOLDIER_SCORE if enemy_pieces[piece].is_soldier() else self.KING_SCORE
                
        for piece in player_pieces:
            eval_score += self.SOLDIER_SCORE if player_pieces[piece].is_soldier() else self.KING_SCORE
            
        return eval_score
    
    def minimax(self, board: GameBoard, player: str, depth: int, isMaximizing: bool):
        if depth == 0 or board.game_ended():
            return self.heuristic(board, player)

        best_value = float('-inf') if isMaximizing else float('inf')
        player_pieces = board.get_black_pieces() if player == 'B' else board.get_white_pieces()
        enemy_pieces = board.get_white_pieces() if player == 'B' else board.get_black_pieces()
        
        movable_pieces = {}
        if isMaximizing:
            for piece in enemy_pieces:
                movable_pieces[enemy_pieces[piece]] = board.piece_can_move(enemy_pieces[piece])
        else:
            for piece in player_pieces:
                movable_pieces[player_pieces[piece]] = board.piece_can_move(player_pieces[piece])
        
        boards = []
        for piece in movable_pieces:
            for pos in movable_pieces[piece]:
                board_copy = copy.deepcopy(board)
                piece_copy = copy.deepcopy(piece)
                board_copy.move(piece_copy, pos)
                boards.append(board_copy)
        
        for board_cp in boards:
            child_value = self.minimax(board_cp, player, depth - 1, not isMaximizing)
            if isMaximizing:
                best_value = max(best_value, child_value)
            else:
                best_value = min(best_value, child_value)
        return best_value
        
    def minimax_alphabeta(self, board: GameBoard, player: str, depth: int, isMaximizing: bool, alpha, beta):
        if depth == 0 or board.game_ended():
            return self.heuristic(board, player)

        best_value = float('-inf') if isMaximizing else float('inf')
        player_pieces = board.get_black_pieces() if player == 'B' else board.get_white_pieces()
        enemy_pieces = board.get_white_pieces() if player == 'B' else board.get_black_pieces()
        
        movable_pieces = {}
        if isMaximizing:
            for piece in enemy_pieces:
                movable_pieces[enemy_pieces[piece]] = board.piece_can_move(enemy_pieces[piece])
        else:
            for piece in player_pieces:
                movable_pieces[player_pieces[piece]] = board.piece_can_move(player_pieces[piece])
        
        boards = []
        for piece in movable_pieces:
            for pos in movable_pieces[piece]:
                board_copy = copy.deepcopy(board)
                piece_copy = copy.deepcopy(piece)
                board_copy.move(piece_copy, pos)
                boards.append(board_copy)
        
        for board_cp in boards:
            child_value = self.minimax_alphabeta(board_cp, player, depth - 1, not isMaximizing, alpha, beta)
            if isMaximizing:
                best_value = max(best_value, child_value)
                alpha = max(alpha, child_value)
                if beta <= alpha:
                    break
                beta = min(beta, alpha)
            else:
                best_value = min(best_value, child_value)
                beta = min(beta, child_value)
                if beta <= alpha:
                    break
                alpha = max(alpha, beta)
        return best_value
    
    def beam_search(self, board: GameBoard, player: str, depth: int, isMaximizing: bool, alpha, beta, beam_width: int):
        if depth == 0 or board.game_ended():
            return self.heuristic(board, player)
        
        best_value = float('-inf') if isMaximizing else float('inf')
        player_pieces = board.get_black_pieces() if player == 'B' else board.get_white_pieces()
        enemy_pieces = board.get_white_pieces() if player == 'B' else board.get_black_pieces()
        
        movable_pieces = {}
        if isMaximizing:
            for piece in enemy_pieces:
                movable_pieces[enemy_pieces[piece]] = board.piece_can_move(enemy_pieces[piece])
        else:
            for piece in player_pieces:
                movable_pieces[player_pieces[piece]] = board.piece_can_move(player_pieces[piece])
        
        boards = []
        for piece in movable_pieces:
            for pos in movable_pieces[piece]:
                board_copy = copy.deepcopy(board)
                piece_copy = copy.deepcopy(piece)
                board_copy.move(piece_copy, pos)
                boards.append(board_copy)
        
        boards.sort(key=lambda b: self.heuristic(b, player), reverse=isMaximizing)
        selected_boards = boards if beam_width >= len(boards) else boards[:beam_width]
        
        for board_cp in selected_boards:
            child_value = self.beam_search(board_cp, player, depth - 1, not isMaximizing, alpha, beta, beam_width)
            if isMaximizing:
                best_value = max(best_value, child_value)
                alpha = max(alpha, child_value)
                if beta <= alpha:
                    break
                beta = min(beta, alpha)
            else:
                best_value = min(best_value, child_value)
                beta = min(beta, child_value)
                if beta <= alpha:
                    break
                alpha = max(alpha, beta)
        return best_value
    
    def evaluate_game(self, board: GameBoard, player: str, depth: int):
        return self.beam_search(board, player, depth, True, float('-inf'), float('inf'), self.BEAM_WIDTH)
    
    def play(self, board: GameBoard, player: str, depth: int):
        movable_pieces = {}
        player_pieces = board.get_black_pieces() if player == 'B' else board.get_white_pieces()
        for piece in player_pieces:
            movable_pieces[player_pieces[piece]] = board.piece_can_move(player_pieces[piece])
        
        boards = []        
        points = []
        for piece in movable_pieces:
            for pos in movable_pieces[piece]:
                piece_copy = copy.deepcopy(piece)
                board_copy = copy.deepcopy(board)
                board_copy.move(piece_copy, pos)
                boards.append(board_copy)
                
        for board_cp in boards:
            points.append(self.evaluate_game(board_cp, player, depth))
                
        return boards[points.index(max(points))]

    def start(self, rounds: int = 0):
        turn = True
        steps = [self.game_board]
        
        if rounds == 0:
            while not self.game_board.game_ended():
                player = 'W' if turn else 'B'
                depth = self.WHITE_DEPTH if turn else self.BLACK_DEPTH
                steps.append(self.play(steps[-1], player, depth))
                turn = not turn
        else:
            for _ in range(rounds):
                player = 'W' if turn else 'B'
                depth = self.WHITE_DEPTH if turn else self.BLACK_DEPTH
                steps.append(self.play(steps[-1], player, depth))
                turn = not turn
        
        return steps
    
    def start_sbs(self, current: GameBoard, turn: bool):
        depth = self.WHITE_DEPTH if turn else self.BLACK_DEPTH
        player = 'W' if turn else 'B'
        return self.play(current, player, depth)  

gboard = GameBoard()
game = Checkers(gboard, 5, 1, 10)

start_time = time.time()
result = gboard
turn = True
result.print_board()
while not result.game_ended():
    player = 'W' if turn else 'B'
    depth = game.WHITE_DEPTH if turn else game.BLACK_DEPTH
    result = game.play(result, player, depth)
    result.print_board()
    turn = not turn
end_time = time.time()
print(f'Runtime: {round(end_time - start_time, 3)} seconds')
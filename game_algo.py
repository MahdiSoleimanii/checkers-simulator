import copy
import time
from game_logic import *

class Checkers:
    def __init__(self, game_board: GameBoard):
        self.game_board = game_board
        self.SOLDIER_SCORE = 1
        self.KING_SCORE = 2
    
    def heuristic(self, board: GameBoard, player: str):
        eval_score = 0
        player_pieces = board.get_black_pieces().values() if player == 'B' else board.get_white_pieces().values()
        enemy_pieces = board.get_white_pieces().values() if player == 'B' else board.get_black_pieces().values()
        
        for piece in enemy_pieces:
            eval_score -= self.SOLDIER_SCORE if piece.is_soldier() else self.KING_SCORE
        for piece in player_pieces:
            eval_score += self.SOLDIER_SCORE if piece.is_soldier() else self.KING_SCORE
            
        return eval_score
    
    def minimax(self, board: GameBoard, player: str, depth: int, isMaximizing: bool):
        if depth == 0 or board.game_ended():
            return self.heuristic(board, player)
        
        possible_moves = {}
        if isMaximizing:
            enemy_pieces = board.get_white_pieces().values() if player == 'B' else board.get_black_pieces().values()
            for piece in enemy_pieces:
                possible_moves[piece] = board.piece_can_move(piece)
            
            max_eval = float('-inf')
            for piece in possible_moves.keys():
                for pos in possible_moves[piece]:
                    board_copy = copy.deepcopy(board)
                    piece_copy = copy.deepcopy(piece)
                    board_copy.move(piece_copy, pos)
                    eval = self.minimax(board_copy, player, depth - 1, False)
                    max_eval = max(max_eval, eval)
            return max_eval
        else:
            player_pieces = board.get_black_pieces().values() if player == 'B' else board.get_white_pieces().values()
            for piece in player_pieces:
                possible_moves[piece] = board.piece_can_move(piece)
            
            min_eval = float('inf')
            for piece in possible_moves.keys():
                for pos in possible_moves[piece]:
                    board_copy = copy.deepcopy(board)
                    piece_copy = copy.deepcopy(piece)
                    board_copy.move(piece_copy, pos)
                    eval = self.minimax(board_copy, player, depth - 1, True)
                    min_eval = min(min_eval, eval)
            return min_eval
        
    def minimax_alphabeta(self, board: GameBoard, player: str, depth: int, isMaximizing: bool, alpha, beta):
        if depth == 0 or board.game_ended():
            return self.heuristic(board, player)
        
        possible_moves = {}
        if isMaximizing:
            enemy_pieces = board.get_white_pieces().values() if player == 'B' else board.get_black_pieces().values()
            for piece in enemy_pieces:
                possible_moves[piece] = board.piece_can_move(piece)
            
            for piece in possible_moves.keys():
                for pos in possible_moves[piece]:
                    board_copy = copy.deepcopy(board)
                    piece_copy = copy.deepcopy(piece)
                    board_copy.move(piece_copy, pos)
                    eval = self.minimax_alphabeta(board_copy, player, depth - 1, False, alpha, beta)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return alpha
        else:
            player_pieces = board.get_black_pieces().values() if player == 'B' else board.get_white_pieces().values()
            for piece in player_pieces:
                possible_moves[piece] = board.piece_can_move(piece)
            
            for piece in possible_moves.keys():
                for pos in possible_moves[piece]:
                    board_copy = copy.deepcopy(board)
                    piece_copy = copy.deepcopy(piece)
                    board_copy.move(piece_copy, pos)
                    eval = self.minimax_alphabeta(board_copy, player, depth - 1, True, alpha, beta)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return beta
    
    def beam_search(self, board: GameBoard, player: str, depth: int, isMaximizing: bool, alpha, beta, beam_width: int):
        if depth == 0 or board.game_ended():
            return self.heuristic(board, player)
        
        possible_moves = {}
        if isMaximizing:
            enemy_pieces = board.get_white_pieces().values() if player == 'B' else board.get_black_pieces().values()
            for piece in enemy_pieces:
                possible_moves[piece] = board.piece_can_move(piece)

            beam_states = []  
            for piece in possible_moves.keys():
                for pos in possible_moves[piece]:
                    board_copy = copy.deepcopy(board)
                    piece_copy = copy.deepcopy(piece)
                    board_copy.move(piece_copy, pos)
                    eval = self.minimax_alphabeta(board_copy, player, depth - 1, False, alpha, beta)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
                    beam_states.append((eval, board_copy))  

            beam_states.sort(reverse=True, key=lambda x: x[0])
            beam_states = beam_states[:beam_width]

            for _, state in beam_states:
                beta = min(beta, self.beam_search(state, player, depth - 1, False, alpha, beta, beam_width))
                if beta <= alpha:
                    break
                
            return alpha
        else:
            player_pieces = board.get_black_pieces().values() if player == 'B' else board.get_white_pieces().values()
            for piece in player_pieces:
                possible_moves[piece] = board.piece_can_move(piece)

            beam_states = []
            for piece in possible_moves.keys():
                for pos in possible_moves[piece]:
                    board_copy = copy.deepcopy(board)
                    piece_copy = copy.deepcopy(piece)
                    board_copy.move(piece_copy, pos)
                    eval = self.minimax_alphabeta(board_copy, player, depth - 1, True, alpha, beta)
                    beta = min(beta, eval)
                    beam_states.append((eval, board_copy))  
            
            beam_states.sort(reverse=False, key=lambda x: x[0])
            beam_states = beam_states[:beam_width]

            for _, state in beam_states:
                alpha = max(alpha, self.beam_search(state, player, depth - 1, True, alpha, beta, beam_width))
                 
            return beta
    
    def evaluate_game(self, board: GameBoard, player: str, depth: int):
        if depth == 0 or board.game_ended():
            return self.heuristic(board, player)
        
        best_value = float('-inf')
        current_value = self.minimax_alphabeta(board, player, depth, True, float('-inf'), float('inf'))
        best_value = max(best_value, current_value)
        
        return best_value
    
    def play(self, board: GameBoard, player: str, depth):
        movable_pieces = {}
        player_pieces = board.get_black_pieces() if player == 'B' else board.get_white_pieces()
        for piece in player_pieces:
            if board.piece_can_move(player_pieces[piece]):
                movable_pieces[player_pieces[piece]] = board.piece_can_move(player_pieces[piece])
                
        boards = []
        points = []
        for piece in movable_pieces.keys():
            for pos in movable_pieces[piece]:
                piece_copy = copy.deepcopy(piece)
                board_copy = copy.deepcopy(board)
                board_copy.move(piece_copy, pos)
                points.append(self.evaluate_game(board_copy, player, depth))
                boards.append(board_copy)
                
        return boards[points.index(max(points))]

    def start(self, rounds: int = 0):
        turn = True
        WHITE_DEPTH = 3
        BLACK_DEPTH = 1
        steps = [self.game_board]
        
        if rounds == 0:
            while not self.game_board.game_ended():
                player = 'W' if turn else 'B'
                turn = not turn
                if player == 'W':
                    self.game_board = self.play(self.game_board, 'W', WHITE_DEPTH)
                else:
                    self.game_board = self.play(self.game_board, 'B', BLACK_DEPTH)
                steps.append(self.game_board)
        else:
            for _ in range(rounds):
                player = 'W' if turn else 'B'
                turn = not turn
                if player == 'W':
                    self.game_board = self.play(self.game_board, 'W', WHITE_DEPTH)
                else:
                    self.game_board = self.play(self.game_board, 'B', BLACK_DEPTH)
                steps.append(self.game_board)
        
        return steps
                

gboard = GameBoard()
game = Checkers(gboard)

start_time = time.time()
result = game.start(10)[-1]
end_time = time.time()

result.print_board()
print(f"Runtime: {end_time - start_time:3f} seconds")
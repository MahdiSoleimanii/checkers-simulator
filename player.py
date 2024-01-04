def valid_pos(coord):
    return 0 <= coord <= 7

class Cell:
    def __init__(self, pos: tuple, isEmpty: bool, color: str):
        self.pos = pos
        self.isEmpty = isEmpty
        self.color = color
    
    def get_pos(self):
        return self.pos
    
    def get_color(self):
        return self.color
    
    def is_empty(self):
        return self.isEmpty
    
    def change_state(self):
        if self.is_empty():
            self.isEmpty = False
        else:
            self.isEmpty = True

class Piece:
    def __init__(self, pos: tuple, color: str, isSoldier: bool = True):
        self.pos = pos
        self.isSoldier = isSoldier
        self.COLOR = color
    
    def set_pos(self, pos: tuple):
        self.pos = pos
    
    def get_pos(self):
        return self.pos
    
    def get_color(self):
        return self.COLOR
    
    def is_soldier(self):
        return self.isSoldier
    
    def kingify(self):
        self.isSoldier = False
        
class GameBoard:
    def __init__(self):
        self.matrix = [[None for _ in range(8)] for _ in range(8)]
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    self.matrix[i][j] = Cell((i, j), True, 'W')
                else:
                    self.matrix[i][j] = Cell((i, j), True, 'B')
        self.black_pieces = {}
        self.white_pieces = {}
        self.__put_pieces()
                    
    def __put_pieces(self):
        game_mat = self.get_matrix()
        for row in game_mat[-3:]:
            for cell in row:
                if cell.get_color() == 'B':
                    cell.change_state()
                    self.black_pieces[cell.get_pos()] = Piece(cell.get_pos(), 'B')
        
        for row in game_mat[:3]:
            for cell in row:
                if cell.get_color() == 'B':
                    cell.change_state()
                    self.white_pieces[cell.get_pos()] = Piece(cell.get_pos(), 'W')
            
    def piece_can_move(self, piece: Piece):
        piece_pos_x, piece_pos_y = piece.get_pos()
        piece_color = piece.get_color()

        if piece.is_soldier():
            return self._get_soldier_moves(piece_pos_x, piece_pos_y, piece_color)
        else:
            return self._get_king_moves(piece_pos_x, piece_pos_y, piece_color)

    def _get_soldier_moves(self, piece_pos_x, piece_pos_y, piece_color):
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        delta = 1 if piece_color == 'B' else -1
        for dx, dy in directions:
            new_pos_x = piece_pos_x + dx * delta
            new_pos_y = piece_pos_y + dy
            if self._is_valid_move(new_pos_x, new_pos_y, piece_color, dy):
                moves.append((new_pos_x, new_pos_y))
        return moves

    def _get_king_moves(self, piece_pos_x, piece_pos_y, piece_color):
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in directions:
            new_pos_x = piece_pos_x + dx
            new_pos_y = piece_pos_y + dy
            if self._is_valid_move(new_pos_x, new_pos_y, piece_color, dy):
                moves.append((new_pos_x, new_pos_y))
        return moves

    def _is_valid_move(self, new_pos_x, new_pos_y, piece_color, dy):
        if not valid_pos(new_pos_x) or not valid_pos(new_pos_y):
            return False

        if self.matrix[new_pos_x][new_pos_y].is_empty():
            return True

        if piece_color == 'B':
            if (new_pos_x, new_pos_y) in self.white_pieces:
                new_pos_x2 = new_pos_x + 1
                new_pos_y2 = new_pos_y + (1 if dy == -1 else -1)
                return valid_pos(new_pos_x2) and valid_pos(new_pos_y2) and self.matrix[new_pos_x2][new_pos_y2].is_empty()
        else:
            if (new_pos_x, new_pos_y) in self.black_pieces:
                new_pos_x2 = new_pos_x - 1
                new_pos_y2 = new_pos_y + (1 if dy == -1 else -1)
                return valid_pos(new_pos_x2) and valid_pos(new_pos_y2) and self.matrix[new_pos_x2][new_pos_y2].is_empty()

        return False
    
    def move(self, piece: Piece, new_pos: tuple):
        current_pos = piece.get_pos()
        new_pos_x = new_pos[0]
        
        piece.set_pos(new_pos)
        if piece.get_color() == 'B':
            self.black_pieces.pop(current_pos)
            if new_pos_x == 0:
                if piece.is_soldier():
                    piece.kingify()
            self.black_pieces[new_pos] = piece
        else:
            self.white_pieces.pop(current_pos)
            if new_pos_x == 7:
                if piece.is_soldier():
                    piece.kingify()
            self.white_pieces[new_pos] = piece
    
    def get_matrix(self):
        return self.matrix
    
    def get_black_pieces(self):
        return self.black_pieces
    
    def get_white_pieces(self):
        return self.white_pieces
       
    def empty_cells(self):
        empty_cells_list = []
        game_mat = self.get_matrix()
        for row in game_mat:
            for cell in row:
                if cell.is_empty():
                    empty_cells_list.append(cell)

        return empty_cells_list

gboard = GameBoard()

bpieces = gboard.get_black_pieces()
for piece in bpieces:
    if gboard.piece_can_move(bpieces[piece]):
        print(piece, gboard.piece_can_move(bpieces[piece]))
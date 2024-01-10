def valid_pos(coord):
    return 0 <= coord <= 7

def chebyshev_dist(first_pos: tuple, second_pos: tuple):
    return max(abs(first_pos[0] - second_pos[0]), abs(first_pos[1] - second_pos[1]))

class Cell:
    def __init__(self, pos: tuple, isEmpty: bool, color: str):
        self.POS = pos
        self.isEmpty = isEmpty
        self.COLOR = color
    
    def get_pos(self):
        return self.POS
    
    def get_color(self):
        return self.COLOR
    
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
        
    def info(self):
        position = "Position: " + str(self.get_pos()) + "\n"
        color = "Color: " + str(self.get_color()) + "\n"
        role = "Soldier" if self.is_soldier() else "King"
        info_str = position + color + role
        return info_str
        
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
    
    def pos_info(self, pos: tuple):
        if pos in self.black_pieces:
            return self.black_pieces[pos].info()
        else:
            return self.white_pieces[pos].info()
    
    def piece_can_move(self, piece: Piece):
        moves = []
        piece_pos_x, piece_pos_y = piece.get_pos()
        piece_color = piece.get_color()
        enemy_pieces = self.white_pieces if piece_color == 'B' else self.black_pieces

        new_x_pos = []
        if piece.is_soldier():
            if piece_color == 'B':
                new_x_pos.append(piece_pos_x - 1)
            else:
                new_x_pos.append(piece_pos_x + 1)
        else:
            new_x_pos.append(piece_pos_x - 1)
            new_x_pos.append(piece_pos_x + 1)
        new_y_pos = [piece_pos_y - 1, piece_pos_y + 1]
        
        for new_x in new_x_pos:
            if valid_pos(new_x):
                for new_y in new_y_pos:
                    if valid_pos(new_y):
                        if self.matrix[new_x][new_y].is_empty():
                            moves.append((new_x, new_y))
                        else:
                            new_pos = (new_x, new_y)
                            if new_pos in enemy_pieces:
                                next_new_x = new_x + (new_x - piece_pos_x)
                                next_new_y = new_y + (new_y - piece_pos_y)
                                if valid_pos(next_new_x) and valid_pos(next_new_y):
                                    if self.matrix[next_new_x][next_new_y].is_empty():
                                        moves.append((next_new_x, next_new_y))
        return moves
    
    def move(self, piece: Piece, new_pos: tuple):
        current_pos = piece.get_pos()
        current_pos_x, current_pos_y = current_pos
        new_pos_x, new_pos_y = new_pos
        
        piece.set_pos(new_pos)
        self.matrix[current_pos_x][current_pos_y].change_state()
        self.matrix[new_pos_x][new_pos_y].change_state()
        
        if piece.get_color() == 'B':
            self.black_pieces.pop(current_pos)
            if new_pos_x == 0:
                if piece.is_soldier():
                    piece.kingify()
            self.black_pieces[new_pos] = piece
            if chebyshev_dist(current_pos, new_pos) > 1:
                num_mid_pieces = chebyshev_dist(current_pos, new_pos) // 2
                x_diff = 1 if new_pos_x > current_pos_x else -1
                y_diff = 1 if new_pos_y > current_pos_y else -1
                for dist in range(num_mid_pieces):
                    mid_piece_x = current_pos_x + (((2 * dist) + 1) * x_diff)
                    mid_piece_y = current_pos_y + (((2 * dist) + 1) * y_diff)
                    mid_piece_pos = (mid_piece_x, mid_piece_y)
                    self.white_pieces.pop(mid_piece_pos)
                    self.matrix[mid_piece_x][mid_piece_y].change_state()
        else:
            self.white_pieces.pop(current_pos)
            if new_pos_x == 7:
                if piece.is_soldier():
                    piece.kingify()
            self.white_pieces[new_pos] = piece
            if chebyshev_dist(current_pos, new_pos) > 1:
                num_mid_pieces = chebyshev_dist(current_pos, new_pos) // 2
                x_diff = 1 if new_pos_x > current_pos_x else -1
                y_diff = 1 if new_pos_y > current_pos_y else -1
                for dist in range(num_mid_pieces):
                    mid_piece_x = current_pos_x + (((2 * dist) + 1) * x_diff)
                    mid_piece_y = current_pos_y + (((2 * dist) + 1) * y_diff)
                    mid_piece_pos = (mid_piece_x, mid_piece_y)
                    self.black_pieces.pop(mid_piece_pos)
                    self.matrix[mid_piece_x][mid_piece_y].change_state()

    def move_by_pos(self, piece_pos: tuple, new_pos: tuple):
        if piece_pos in self.black_pieces:
            self.move(self.black_pieces[piece_pos], new_pos)
        else:
            self.move(self.white_pieces[piece_pos], new_pos)
    
    def game_ended(self):
        return self.black_pieces == {} or self.white_pieces == {}
    
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
    
    def print_board(self):
        print('-'*30)
        for i in range(len(self.get_matrix())):
            for j in range(len(self.get_matrix()[i])):
                cell = self.get_matrix()[i][j]
                if cell.is_empty():
                    print(f"{'-':<3}", end=" ")
                else:
                    if (i, j) in self.get_black_pieces():
                        if self.get_black_pieces()[(i, j)].is_soldier():
                            print(f"{'○':<3}", end=" ")
                        else:
                            print(f"{'⚇':<3}", end=" ")
                    else:
                        if self.get_white_pieces()[(i, j)].is_soldier():
                            print(f"{'●':<3}", end=" ")
                        else:
                            print(f"{'⚉':<3}", end=" ")
            print()
        print('-'*30)
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
        # First check if the piece is a Soldier piece or a King piece
        if piece.is_soldier():
            # Then we check moves for a Black Soldier Piece
            if piece_color == 'B':
                black_moves = []
                # A Black Soldier Piece can go Top-Left or Top-Right
                new_pos_x = piece_pos_x - 1
                new_pos_y1 = piece_pos_y - 1
                new_pos_y2 = piece_pos_y + 1
                # Check if going up is in-bound.
                if valid_pos(new_pos_x):
                    # If can go up, check if going left is in-bound.
                    if valid_pos(new_pos_y1):
                        # If the cell in Top-Left is empty, can move to it.
                        # So return True and coord of Top-Left cell
                        if self.matrix[new_pos_x][new_pos_y1].is_empty():
                            black_moves.append((new_pos_x, new_pos_y1))
                        # If the cell in Top-Left isn't empty...
                        else:
                            # Check if the piece in Top-Left is a White Piece
                            new_pos = (new_pos_x, new_pos_y1)
                            if new_pos in self.white_pieces:
                                # If it is a White Piece, check Top-Left of it
                                new_pos_x1 = new_pos_x - 1
                                new_pos_y11 = new_pos_y1 - 1
                                # If Top-Left of the White Piece isn't out of bounds...
                                if valid_pos(new_pos_x1) and valid_pos(new_pos_y11):
                                    # If Top-Left of the White Piece is empty,
                                    # return True and the coords of it.
                                    if self.matrix[new_pos_x1][new_pos_y11].is_empty():
                                        black_moves.append((new_pos_x1, new_pos_y11))
                    # If can go up, but going left is out of bounds.
                    # for a Black Soldier Piece both Top-Left and Top-Right can't be out of bounds at the same time.
                    if valid_pos(new_pos_y2):
                        # If the cell in Top-Right is empty, can move to it.
                        # So return True and coord of Top-Right cell
                        if self.matrix[new_pos_x][new_pos_y2].is_empty():
                            black_moves.append((new_pos_x, new_pos_y2))
                        # If the cell in Top-Right isn't empty...
                        else:
                            # Check if the piece in Top-Right is a White Piece
                            new_pos = (new_pos_x, new_pos_y2)
                            if new_pos in self.white_pieces:
                                # If it is a White Piece, check Top-Right of it
                                new_pos_x1 = new_pos_x - 1
                                new_pos_y22 = new_pos_y2 + 1
                                # If Top-Right of the White Piece isn't out of bounds...
                                if valid_pos(new_pos_x1) and valid_pos(new_pos_y22):
                                    # If Top-Right of the White Piece is empty,
                                    # return True and the coords of it.
                                    if self.matrix[new_pos_x1][new_pos_y22].is_empty():
                                        black_moves.append((new_pos_x1, new_pos_y22))
                return black_moves
            # If it isn't a Black Piece, it's definitely a White Soldier Piece.
            # So we check moves for a White Soldier Piece
            else:
                white_moves = []
                # A White Soldier Piece can go Bottom-Left or Bottom-Right
                new_pos_x = piece_pos_x + 1
                new_pos_y1 = piece_pos_y - 1
                new_pos_y2 = piece_pos_y + 1
                # Check if going down is in-bound.
                if valid_pos(new_pos_x):
                    # If can go down, check if going left is in-bound.
                    if valid_pos(new_pos_y1):
                        # If the cell in Bottom-Left is empty, can move to it.
                        # save its coords.
                        if self.matrix[new_pos_x][new_pos_y1].is_empty():
                            white_moves.append((new_pos_x, new_pos_y1))
                        # If the cell in Top-Left isn't empty...
                        else:
                            # Check if the piece in Bottom-Left is a Black Piece
                            new_pos = (new_pos_x, new_pos_y1)
                            if new_pos in self.black_pieces:
                                # If it is a Black Piece, check Bottom-Left of it
                                new_pos_x1 = new_pos_x + 1
                                new_pos_y11 = new_pos_y1 - 1
                                # If Bottom-Left of the Black Piece isn't out of bounds...
                                if valid_pos(new_pos_x1) and valid_pos(new_pos_y11):
                                    # If Bottom-Left of the Black Piece is empty,
                                    # save its coords.
                                    if self.matrix[new_pos_x1][new_pos_y11].is_empty():
                                        white_moves.append((new_pos_x1, new_pos_y11))
                    # If can go down, but going left is out of bounds.
                    # for a White Soldier Piece both Bottom-Left and Bottom-Right can't be out of bounds at the same time.
                    if valid_pos(new_pos_y2):
                        # If the cell in Bottom-Right is empty, can move to it.
                        # save its coords.
                        if self.matrix[new_pos_x][new_pos_y2].is_empty():
                            white_moves.append((new_pos_x, new_pos_y2))
                        # If the cell in Bottom-Right isn't empty...
                        else:
                            # Check if the piece in Bottom-Right is a Black Piece
                            new_pos = (new_pos_x, new_pos_y2)
                            if new_pos in self.black_pieces:
                                # If it is a Black Piece, check Bottom-Right of it
                                new_pos_x1 = new_pos_x + 1
                                new_pos_y22 = new_pos_y2 + 1
                                # If Top-Right of the White Piece isn't out of bounds...
                                if valid_pos(new_pos_x1) and valid_pos(new_pos_y22):
                                    # If Bottom-Right of the Black Piece is empty,
                                    # save its coords
                                    if self.matrix[new_pos_x1][new_pos_y22].is_empty():
                                        white_moves.append((new_pos_x1, new_pos_y22))
                return white_moves
        # If it isn't a Soldier Piece it is a King Piece
        else:
            new_pos_x1 = piece_pos_x - 1
            new_pos_x2 = piece_pos_x + 1
            new_pos_y1 = piece_pos_y - 1
            new_pos_y2 = piece_pos_y + 1
            if piece_color == 'B':
                black_king_moves = []
                if valid_pos(new_pos_x1):
                    if valid_pos(new_pos_y1):
                        if self.matrix[new_pos_x1][new_pos_y1].is_empty():
                            black_king_moves.append((new_pos_x1, new_pos_y1))
                        else:
                            new_pos = (new_pos_x1, new_pos_y1)
                            if new_pos in self.white_pieces:
                                new_pos_x11 = new_pos_x1 - 1
                                new_pos_y11 = new_pos_y1 - 1
                                if valid_pos(new_pos_x11) and valid_pos(new_pos_y11):
                                    if self.matrix[new_pos_x11][new_pos_y11].is_empty():
                                        black_king_moves.append((new_pos_x11, new_pos_y11))
                    if valid_pos(new_pos_y2):
                        if self.matrix[new_pos_x1][new_pos_y2].is_empty():
                            black_king_moves.append((new_pos_x1, new_pos_y2))
                        else:
                            new_pos = (new_pos_x1, new_pos_y2)
                            if new_pos in self.white_pieces:
                                new_pos_x11 = new_pos_x1 - 1
                                new_pos_y22 = new_pos_y2 + 1
                                if valid_pos(new_pos_x11) and valid_pos(new_pos_y22):
                                    if self.matrix[new_pos_x11][new_pos_y22].is_empty():
                                        black_king_moves.append((new_pos_x11, new_pos_y22))
                if valid_pos(new_pos_x2):
                    if valid_pos(new_pos_y1):
                        if self.matrix[new_pos_x2][new_pos_y1].is_empty():
                            black_king_moves.append((new_pos_x2, new_pos_y1))
                        else:
                            new_pos = (new_pos_x2, new_pos_y1)
                            if new_pos in self.white_pieces:
                                new_pos_x22 = new_pos_x2 + 1
                                new_pos_y11 = new_pos_y1 - 1
                                if valid_pos(new_pos_x22) and valid_pos(new_pos_y11):
                                    if self.matrix[new_pos_x22][new_pos_y11].is_empty():
                                        black_king_moves.append((new_pos_x22, new_pos_y11))
                    if valid_pos(new_pos_y2):
                        if self.matrix[new_pos_x2][new_pos_y2].is_empty():
                            black_king_moves.append((new_pos_x2, new_pos_y2))
                        else:
                            new_pos = (new_pos_x2, new_pos_y2)
                            if new_pos in self.white_pieces:
                                new_pos_x22 = new_pos_x2 + 1
                                new_pos_y22 = new_pos_y2 + 1
                                if valid_pos(new_pos_x22) and valid_pos(new_pos_y22):
                                    if self.matrix[new_pos_x22][new_pos_y22].is_empty():
                                        black_king_moves.append((new_pos_x22, new_pos_y22))
            else:
                white_king_moves = []
                if valid_pos(new_pos_x1):
                    if valid_pos(new_pos_y1):
                        if self.matrix[new_pos_x1][new_pos_y1].is_empty():
                            white_king_moves.append((new_pos_x1, new_pos_y1))
                        else:
                            new_pos = (new_pos_x1, new_pos_y1)
                            if new_pos in self.black_pieces:
                                new_pos_x11 = new_pos_x1 - 1
                                new_pos_y11 = new_pos_y1 - 1
                                if valid_pos(new_pos_x11) and valid_pos(new_pos_y11):
                                    if self.matrix[new_pos_x11][new_pos_y11].is_empty():
                                        white_king_moves.append((new_pos_x11, new_pos_y11))
                    if valid_pos(new_pos_y2):
                        if self.matrix[new_pos_x1][new_pos_y2].is_empty():
                            white_king_moves.append((new_pos_x1, new_pos_y2))
                        else:
                            new_pos = (new_pos_x1, new_pos_y2)
                            if new_pos in self.black_pieces:
                                new_pos_x11 = new_pos_x1 - 1
                                new_pos_y22 = new_pos_y2 + 1
                                if valid_pos(new_pos_x11) and valid_pos(new_pos_y22):
                                    if self.matrix[new_pos_x11][new_pos_y22].is_empty():
                                        white_king_moves.append((new_pos_x11, new_pos_y22))
                if valid_pos(new_pos_x2):
                    if valid_pos(new_pos_y1):
                        if self.matrix[new_pos_x2][new_pos_y1].is_empty():
                            white_king_moves.append((new_pos_x2, new_pos_y1))
                        else:
                            new_pos = (new_pos_x2, new_pos_y1)
                            if new_pos in self.black_pieces:
                                new_pos_x22 = new_pos_x2 + 1
                                new_pos_y11 = new_pos_y1 - 1
                                if valid_pos(new_pos_x22) and valid_pos(new_pos_y11):
                                    if self.matrix[new_pos_x22][new_pos_y11].is_empty():
                                        white_king_moves.append((new_pos_x22, new_pos_y11))
                    if valid_pos(new_pos_y2):
                        if self.matrix[new_pos_x2][new_pos_y2].is_empty():
                            white_king_moves.append((new_pos_x2, new_pos_y2))
                        else:
                            new_pos = (new_pos_x2, new_pos_y2)
                            if new_pos in self.black_pieces:
                                new_pos_x22 = new_pos_x2 + 1
                                new_pos_y22 = new_pos_y2 + 1
                                if valid_pos(new_pos_x22) and valid_pos(new_pos_y22):
                                    if self.matrix[new_pos_x22][new_pos_y22].is_empty():
                                        white_king_moves.append((new_pos_x22, new_pos_y22))
    
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

print('Black Pieces: ')
for piece in gboard.get_black_pieces():
    print(piece, gboard.piece_can_move(gboard.get_black_pieces()[piece]), end=' - ')
    
print('White Pieces: ')
for piece in gboard.get_white_pieces():
    print(piece, gboard.piece_can_move(gboard.get_white_pieces()[piece]), end=' - ')

print()
print('-'*20)
for row in gboard.get_matrix():
    for cell in row:
        print(f"{not cell.is_empty(): <3}", end=' ')
    print()

gboard.move_by_pos((5, 2), (4, 1))

print('Black Pieces: ')
for piece in gboard.get_black_pieces():
    print(piece, gboard.piece_can_move(gboard.get_black_pieces()[piece]), end=' - ')

print()  
print('White Pieces: ')
for piece in gboard.get_white_pieces():
    print(piece, gboard.piece_can_move(gboard.get_white_pieces()[piece]), end=' - ')

print()
print('-'*20)
for row in gboard.get_matrix():
    for cell in row:
        print(f"{not cell.is_empty(): <3}", end=' ')
    print()
    
gboard.move_by_pos((2, 1), (3, 0))

print('Black Pieces: ')
for piece in gboard.get_black_pieces():
    print(piece, gboard.piece_can_move(gboard.get_black_pieces()[piece]), end=' - ')
   
print() 
print('White Pieces: ')
for piece in gboard.get_white_pieces():
    print(piece, gboard.piece_can_move(gboard.get_white_pieces()[piece]), end=' - ')

print()
print('-'*20)
for row in gboard.get_matrix():
    for cell in row:
        print(f"{not cell.is_empty(): <3}", end=' ')
    print()
    
gboard.move_by_pos((5, 4), (4, 3))

print('Black Pieces: ')
for piece in gboard.get_black_pieces():
    print(piece, gboard.piece_can_move(gboard.get_black_pieces()[piece]), end=' - ')
    
print()
print('White Pieces: ')
for piece in gboard.get_white_pieces():
    print(piece, gboard.piece_can_move(gboard.get_white_pieces()[piece]), end=' - ')

print()
print('-'*20)
for row in gboard.get_matrix():
    for cell in row:
        print(f"{not cell.is_empty(): <3}", end=' ')
    print()
    
gboard.move_by_pos((3, 0), (5, 2))

print('Black Pieces: ')
for piece in gboard.get_black_pieces():
    print(piece, gboard.piece_can_move(gboard.get_black_pieces()[piece]), end=' - ')
    
print()
print('White Pieces: ')
for piece in gboard.get_white_pieces():
    print(piece, gboard.piece_can_move(gboard.get_white_pieces()[piece]), end=' - ')

print()
print('-'*20)
for row in gboard.get_matrix():
    for cell in row:
        print(f"{not cell.is_empty(): <3}", end=' ')
    print()
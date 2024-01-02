def valid_pos(coord):
    return 0 <= coord <= 7

class Cell:
    def __init__(self, pos: tuple, isEmpty: bool, color: str):
        self.pos = pos
        self.isEmpty = isEmpty
        self.color = color
    
    def getPos(self):
        return self.pos
    
    def getColor(self):
        return self.color
    
    def cellIsEmpty(self):
        return self.isEmpty
    
    def change_state(self):
        if self.cellIsEmpty():
            self.isEmpty = False
        else:
            self.isEmpty = True

class Piece:
    def __init__(self, pos: tuple, color: str, isSoldier: bool = True):
        self.pos = pos
        self.isSoldier = isSoldier
        self.COLOR = color
    
    def setPos(self, pos: tuple):
        self.pos = pos
    
    def getPos(self):
        return self.pos
    
    def getColor(self):
        return self.COLOR
    
    def pieceIsSoldier(self):
        return self.isSoldier
    
    def Kingify(self):
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
        game_mat = self.getMatrix()
        for row in game_mat[-3:]:
            for cell in row:
                if cell.getColor() == 'B':
                    cell.change_state()
                    self.black_pieces[cell.getPos()] = Piece(cell.getPos(), 'B')
        
        for row in game_mat[:3]:
            for cell in row:
                if cell.getColor() == 'B':
                    cell.change_state()
                    self.white_pieces[cell.getPos()] = Piece(cell.getPos(), 'W')
    
    # def piece_can_move(self, piece: Piece):
    #     piece_pos_x, piece_pos_y = piece.getPos()
    #     piece_color = piece.getColor()
    #     # First check if the piece is a Soldier piece or a King piece
    #     if piece.pieceIsSoldier():
    #         # Then we check moves for a Black Soldier Piece
    #         if piece_color == 'B':
    #             black_moves = []
    #             # A Black Soldier Piece can go Top-Left or Top-Right
    #             new_pos_x = piece_pos_x - 1
    #             new_pos_y1 = piece_pos_y - 1
    #             new_pos_y2 = piece_pos_y + 1
    #             # Check if going up is in-bound.
    #             if valid_pos(new_pos_x):
    #                 # If can go up, check if going left is in-bound.
    #                 if valid_pos(new_pos_y1):
    #                     # If the cell in Top-Left is empty, can move to it.
    #                     # So return True and coord of Top-Left cell
    #                     if self.matrix[new_pos_x][new_pos_y1].cellIsEmpty():
    #                         black_moves.append((new_pos_x, new_pos_y1))
    #                     # If the cell in Top-Left isn't empty...
    #                     else:
    #                         # Check if the piece in Top-Left is a White Piece
    #                         new_pos = (new_pos_x, new_pos_y1)
    #                         if new_pos in self.white_pieces:
    #                             # If it is a White Piece, check Top-Left of it
    #                             new_pos_x1 = new_pos_x - 1
    #                             new_pos_y11 = new_pos_y1 - 1
    #                             # If Top-Left of the White Piece isn't out of bounds...
    #                             if valid_pos(new_pos_x1) and valid_pos(new_pos_y11):
    #                                 # If Top-Left of the White Piece is empty,
    #                                 # return True and the coords of it.
    #                                 if self.matrix[new_pos_x1][new_pos_y11].cellIsEmpty():
    #                                     black_moves.append((new_pos_x1, new_pos_y11))
    #                 # If can go up, but going left is out of bounds.
    #                 # for a Black Soldier Piece both Top-Left and Top-Right can't be out of bounds at the same time.
    #                 if valid_pos(new_pos_y2):
    #                     # If the cell in Top-Right is empty, can move to it.
    #                     # So return True and coord of Top-Right cell
    #                     if self.matrix[new_pos_x][new_pos_y2].cellIsEmpty():
    #                         black_moves.append((new_pos_x, new_pos_y2))
    #                     # If the cell in Top-Right isn't empty...
    #                     else:
    #                         # Check if the piece in Top-Right is a White Piece
    #                         new_pos = (new_pos_x, new_pos_y2)
    #                         if new_pos in self.white_pieces:
    #                             # If it is a White Piece, check Top-Right of it
    #                             new_pos_x1 = new_pos_x - 1
    #                             new_pos_y22 = new_pos_y2 + 1
    #                             # If Top-Right of the White Piece isn't out of bounds...
    #                             if valid_pos(new_pos_x1) and valid_pos(new_pos_y22):
    #                                 # If Top-Right of the White Piece is empty,
    #                                 # return True and the coords of it.
    #                                 if self.matrix[new_pos_x1][new_pos_y22].cellIsEmpty():
    #                                     black_moves.append((new_pos_x1, new_pos_y22))
    #             return black_moves
    #         # If it isn't a Black Piece, it's definitely a White Soldier Piece.
    #         # So we check moves for a White Soldier Piece
    #         else:
    #             white_moves = []
    #             # A White Soldier Piece can go Bottom-Left or Bottom-Right
    #             new_pos_x = piece_pos_x + 1
    #             new_pos_y1 = piece_pos_y - 1
    #             new_pos_y2 = piece_pos_y + 1
    #             # Check if going down is in-bound.
    #             if valid_pos(new_pos_x):
    #                 # If can go down, check if going left is in-bound.
    #                 if valid_pos(new_pos_y1):
    #                     # If the cell in Bottom-Left is empty, can move to it.
    #                     # save its coords.
    #                     if self.matrix[new_pos_x][new_pos_y1].cellIsEmpty():
    #                         white_moves.append((new_pos_x, new_pos_y1))
    #                     # If the cell in Top-Left isn't empty...
    #                     else:
    #                         # Check if the piece in Bottom-Left is a Black Piece
    #                         new_pos = (new_pos_x, new_pos_y1)
    #                         if new_pos in self.black_pieces:
    #                             # If it is a Black Piece, check Bottom-Left of it
    #                             new_pos_x1 = new_pos_x + 1
    #                             new_pos_y11 = new_pos_y1 - 1
    #                             # If Bottom-Left of the Black Piece isn't out of bounds...
    #                             if valid_pos(new_pos_x1) and valid_pos(new_pos_y11):
    #                                 # If Bottom-Left of the Black Piece is empty,
    #                                 # save its coords.
    #                                 if self.matrix[new_pos_x1][new_pos_y11].cellIsEmpty():
    #                                     white_moves.append((new_pos_x1, new_pos_y11))
    #                 # If can go down, but going left is out of bounds.
    #                 # for a White Soldier Piece both Bottom-Left and Bottom-Right can't be out of bounds at the same time.
    #                 if valid_pos(new_pos_y2):
    #                     # If the cell in Bottom-Right is empty, can move to it.
    #                     # save its coords.
    #                     if self.matrix[new_pos_x][new_pos_y2].cellIsEmpty():
    #                         white_moves.append((new_pos_x, new_pos_y2))
    #                     # If the cell in Bottom-Right isn't empty...
    #                     else:
    #                         # Check if the piece in Bottom-Right is a Black Piece
    #                         new_pos = (new_pos_x, new_pos_y2)
    #                         if new_pos in self.black_pieces:
    #                             # If it is a Black Piece, check Bottom-Right of it
    #                             new_pos_x1 = new_pos_x + 1
    #                             new_pos_y22 = new_pos_y2 + 1
    #                             # If Top-Right of the White Piece isn't out of bounds...
    #                             if valid_pos(new_pos_x1) and valid_pos(new_pos_y22):
    #                                 # If Bottom-Right of the Black Piece is empty,
    #                                 # save its coords
    #                                 if self.matrix[new_pos_x1][new_pos_y22].cellIsEmpty():
    #                                     white_moves.append((new_pos_x1, new_pos_y22))
    #             return white_moves
    #     # If it isn't a Soldier Piece it is a King Piece
    #     else:
    #         new_pos_x1 = piece_pos_x - 1
    #         new_pos_x2 = piece_pos_x + 1
    #         new_pos_y1 = piece_pos_y - 1
    #         new_pos_y2 = piece_pos_y + 1
    #         if piece_color == 'B':
    #             black_king_moves = []
    #             if valid_pos(new_pos_x1):
    #                 if valid_pos(new_pos_y1):
    #                     if self.matrix[new_pos_x1][new_pos_y1].cellIsEmpty():
    #                         black_king_moves.append((new_pos_x1, new_pos_y1))
    #                     else:
    #                         new_pos = (new_pos_x1, new_pos_y1)
    #                         if new_pos in self.white_pieces:
    #                             new_pos_x11 = new_pos_x1 - 1
    #                             new_pos_y11 = new_pos_y1 - 1
    #                             if valid_pos(new_pos_x11) and valid_pos(new_pos_y11):
    #                                 if self.matrix[new_pos_x11][new_pos_y11].cellIsEmpty():
    #                                     black_king_moves.append((new_pos_x11, new_pos_y11))
    #                 if valid_pos(new_pos_y2):
    #                     if self.matrix[new_pos_x1][new_pos_y2].cellIsEmpty():
    #                         black_king_moves.append((new_pos_x1, new_pos_y2))
    #                     else:
    #                         new_pos = (new_pos_x1, new_pos_y2)
    #                         if new_pos in self.white_pieces:
    #                             new_pos_x11 = new_pos_x1 - 1
    #                             new_pos_y22 = new_pos_y2 + 1
    #                             if valid_pos(new_pos_x11) and valid_pos(new_pos_y22):
    #                                 if self.matrix[new_pos_x11][new_pos_y22].cellIsEmpty():
    #                                     black_king_moves.append((new_pos_x11, new_pos_y22))
    #             if valid_pos(new_pos_x2):
    #                 if valid_pos(new_pos_y1):
    #                     if self.matrix[new_pos_x2][new_pos_y1].cellIsEmpty():
    #                         black_king_moves.append((new_pos_x2, new_pos_y1))
    #                     else:
    #                         new_pos = (new_pos_x2, new_pos_y1)
    #                         if new_pos in self.white_pieces:
    #                             new_pos_x22 = new_pos_x2 + 1
    #                             new_pos_y11 = new_pos_y1 - 1
    #                             if valid_pos(new_pos_x22) and valid_pos(new_pos_y11):
    #                                 if self.matrix[new_pos_x22][new_pos_y11].cellIsEmpty():
    #                                     black_king_moves.append((new_pos_x22, new_pos_y11))
    #                 if valid_pos(new_pos_y2):
    #                     if self.matrix[new_pos_x2][new_pos_y2].cellIsEmpty():
    #                         black_king_moves.append((new_pos_x2, new_pos_y2))
    #                     else:
    #                         new_pos = (new_pos_x2, new_pos_y2)
    #                         if new_pos in self.white_pieces:
    #                             new_pos_x22 = new_pos_x2 + 1
    #                             new_pos_y22 = new_pos_y2 + 1
    #                             if valid_pos(new_pos_x22) and valid_pos(new_pos_y22):
    #                                 if self.matrix[new_pos_x22][new_pos_y22].cellIsEmpty():
    #                                     black_king_moves.append((new_pos_x22, new_pos_y22))
    #         else:
    #             white_king_moves = []
    #             if valid_pos(new_pos_x1):
    #                 if valid_pos(new_pos_y1):
    #                     if self.matrix[new_pos_x1][new_pos_y1].cellIsEmpty():
    #                         white_king_moves.append((new_pos_x1, new_pos_y1))
    #                     else:
    #                         new_pos = (new_pos_x1, new_pos_y1)
    #                         if new_pos in self.black_pieces:
    #                             new_pos_x11 = new_pos_x1 - 1
    #                             new_pos_y11 = new_pos_y1 - 1
    #                             if valid_pos(new_pos_x11) and valid_pos(new_pos_y11):
    #                                 if self.matrix[new_pos_x11][new_pos_y11].cellIsEmpty():
    #                                     white_king_moves.append((new_pos_x11, new_pos_y11))
    #                 if valid_pos(new_pos_y2):
    #                     if self.matrix[new_pos_x1][new_pos_y2].cellIsEmpty():
    #                         white_king_moves.append((new_pos_x1, new_pos_y2))
    #                     else:
    #                         new_pos = (new_pos_x1, new_pos_y2)
    #                         if new_pos in self.black_pieces:
    #                             new_pos_x11 = new_pos_x1 - 1
    #                             new_pos_y22 = new_pos_y2 + 1
    #                             if valid_pos(new_pos_x11) and valid_pos(new_pos_y22):
    #                                 if self.matrix[new_pos_x11][new_pos_y22].cellIsEmpty():
    #                                     white_king_moves.append((new_pos_x11, new_pos_y22))
    #             if valid_pos(new_pos_x2):
    #                 if valid_pos(new_pos_y1):
    #                     if self.matrix[new_pos_x2][new_pos_y1].cellIsEmpty():
    #                         white_king_moves.append((new_pos_x2, new_pos_y1))
    #                     else:
    #                         new_pos = (new_pos_x2, new_pos_y1)
    #                         if new_pos in self.black_pieces:
    #                             new_pos_x22 = new_pos_x2 + 1
    #                             new_pos_y11 = new_pos_y1 - 1
    #                             if valid_pos(new_pos_x22) and valid_pos(new_pos_y11):
    #                                 if self.matrix[new_pos_x22][new_pos_y11].cellIsEmpty():
    #                                     white_king_moves.append((new_pos_x22, new_pos_y11))
    #                 if valid_pos(new_pos_y2):
    #                     if self.matrix[new_pos_x2][new_pos_y2].cellIsEmpty():
    #                         white_king_moves.append((new_pos_x2, new_pos_y2))
    #                     else:
    #                         new_pos = (new_pos_x2, new_pos_y2)
    #                         if new_pos in self.black_pieces:
    #                             new_pos_x22 = new_pos_x2 + 1
    #                             new_pos_y22 = new_pos_y2 + 1
    #                             if valid_pos(new_pos_x22) and valid_pos(new_pos_y22):
    #                                 if self.matrix[new_pos_x22][new_pos_y22].cellIsEmpty():
    #                                     white_king_moves.append((new_pos_x22, new_pos_y22))
            
    def piece_can_move(self, piece: Piece):
        piece_pos_x, piece_pos_y = piece.getPos()
        piece_color = piece.getColor()

        if piece.pieceIsSoldier():
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

        if self.matrix[new_pos_x][new_pos_y].cellIsEmpty():
            return True

        if piece_color == 'B':
            if (new_pos_x, new_pos_y) in self.white_pieces:
                new_pos_x2 = new_pos_x + 1
                new_pos_y2 = new_pos_y + (1 if dy == -1 else -1)
                return valid_pos(new_pos_x2) and valid_pos(new_pos_y2) and self.matrix[new_pos_x2][new_pos_y2].cellIsEmpty()
        else:
            if (new_pos_x, new_pos_y) in self.black_pieces:
                new_pos_x2 = new_pos_x - 1
                new_pos_y2 = new_pos_y + (1 if dy == -1 else -1)
                return valid_pos(new_pos_x2) and valid_pos(new_pos_y2) and self.matrix[new_pos_x2][new_pos_y2].cellIsEmpty()

        return False
    
    def move(self, piece: Piece, new_pos: tuple):
        current_pos = piece.getPos()
        new_pos_x = new_pos[0]
        
        piece.setPos(new_pos)
        if piece.getColor() == 'B':
            self.black_pieces.pop(current_pos)
            if new_pos_x == 0:
                if piece.pieceIsSoldier():
                    piece.Kingify()
            self.black_pieces[new_pos] = piece
        else:
            self.white_pieces.pop(current_pos)
            if new_pos_x == 7:
                if piece.pieceIsSoldier():
                    piece.Kingify()
            self.white_pieces[new_pos] = piece
    
    def getMatrix(self):
        return self.matrix
    
    def getBlackPieces(self):
        return self.black_pieces
    
    def getWhitePieces(self):
        return self.white_pieces
       
    def empty_cells(self):
        empty_cells_list = []
        game_mat = self.getMatrix()
        for row in game_mat:
            for cell in row:
                if cell.cellIsEmpty():
                    empty_cells_list.append(cell)

        return empty_cells_list

gboard = GameBoard()

bpieces = gboard.getBlackPieces()
for piece in bpieces:
    if gboard.piece_can_move(bpieces[piece]):
        print(piece, gboard.piece_can_move(bpieces[piece]))
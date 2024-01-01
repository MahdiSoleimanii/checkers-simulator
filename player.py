def valid_pos(coord):
    return 0 <= coord <= 8

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

class Player:
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
                    self.black_pieces[cell.getPos()] = Player(cell.getPos(), 'B')
        
        for row in game_mat[:3]:
            for cell in row:
                if cell.getColor() == 'B':
                    cell.change_state()
                    self.white_pieces[cell.getPos()] = Player(cell.getPos(), 'W')
    
    def piece_can_move(self, piece: Player):
        piece_pos_x, piece_pos_y = piece.getPos()
        piece_color = piece.getColor()
        # First check if the piece is a Soldier piece or a King piece
        if piece.pieceIsSoldier():
            # Then we check moves for a Black Soldier Piece
            if piece_color == 'B':
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
                        if self.matrix[new_pos_x][new_pos_y1].cellIsEmpty():
                            return True, (new_pos_x, new_pos_y1)
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
                                    if self.matrix[new_pos_x1][new_pos_y11].cellIsEmpty():
                                        return True, (new_pos_x1, new_pos_y11)
                                    # If Top-Left of the White Piece isn't empty,
                                    # can't move to it; so return False
                                    else:
                                        return False
                                # If Top-Left of the White Piece is outta bounds,
                                # can't move to it; so return False.
                                else:
                                    return False
                            # If Top-Left isn't a White Piece (It is surely a Black Piece since it wasn't an empty cell),
                            # can't move to it; so return False.
                            else:
                                return False
                    # If can go up, but going left is out of bounds.
                    # for a Black Soldier Piece both Top-Left and Top-Right can't be out of bounds at the same time.
                    else:
                        # If the cell in Top-Right is empty, can move to it.
                        # So return True and coord of Top-Right cell
                        if self.matrix[new_pos_x][new_pos_y2].cellIsEmpty():
                            return True, (new_pos_x, new_pos_y2)
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
                                    if self.matrix[new_pos_x1][new_pos_y22].cellIsEmpty():
                                        return True, (new_pos_x1, new_pos_y22)
                                    # If Top-Right of the White Piece isn't empty,
                                    # can't move to it; so return False
                                    else:
                                        return False
                                # If Top-Right of the White Piece is outta bounds,
                                # can't move to it; so return False.
                                else:
                                    return False
                            # If Top-Right isn't a White Piece (It is surely a Black Piece since it wasn't an empty cell),
                            # can't move to it; so return False.
                            else:
                                return False
                # If a Black Soldier Piece can't move up, it is a King Piece.
                # We don't deal with King Pieces here, so return False.
                else:
                    return False
            # If it isn't a Black Piece, it's definitely a White Soldier Piece.
            # So we check moves for a White Soldier Piece
            else:
                # A White Soldier Piece can go Bottom-Left or Bottom-Right
                new_pos_x = piece_pos_x + 1
                new_pos_y1 = piece_pos_y - 1
                new_pos_y2 = piece_pos_y + 1
                # Check if going down is in-bound.
                if valid_pos(new_pos_x):
                    # If can go down, check if going left is in-bound.
                    if valid_pos(new_pos_y1):
                        # If the cell in Bottom-Left is empty, can move to it.
                        # So return True and coord of Bottom-Left cell
                        if self.matrix[new_pos_x][new_pos_y1].cellIsEmpty():
                            return True, (new_pos_x, new_pos_y1)
                        # If the cell in Bottom-Left isn't empty...
                        else:
                            # Check if the piece in Bottom-Left is a Black Piece
                            new_pos = (new_pos_x, new_pos_y1)
                            if new_pos in self.black_pieces:
                                # If it is a Black Piece, check Bottom-Left of it
                                new_pos_x1 = new_pos_x + 1
                                new_pos_y11 = new_pos_y1 - 1
                                # If Bottom-Left of the White Piece isn't out of bounds...
                                if valid_pos(new_pos_x1) and valid_pos(new_pos_y11):
                                    # If Bottom-Left of the Black Piece is empty,
                                    # return True and the coords of it.
                                    if self.matrix[new_pos_x1][new_pos_y11].cellIsEmpty():
                                        return True, (new_pos_x1, new_pos_y11)
                                    # If Bottom-Left of the Black Piece isn't empty,
                                    # can't move to it; so return False
                                    else:
                                        return False
                                # If Bottom-Left of the White Piece is outta bounds,
                                # can't move to it; so return False.
                                else:
                                    return False
                            # If Bottom-Left isn't a Black Piece (It is surely a White Piece since it wasn't an empty cell),
                            # can't move to it; so return False.
                            else:
                                return False
                    # If can go up, but going left is out of bounds.
                    # for a White Soldier Piece both Bottom-Left and Bottom-Right can't be out of bounds at the same time.
                    else:
                        # If the cell in Bottom-Right is empty, can move to it.
                        # So return True and coord of Bottom-Right cell
                        if self.matrix[new_pos_x][new_pos_y2].cellIsEmpty():
                            return True, (new_pos_x, new_pos_y2)
                        # If the cell in Bottom-Right isn't empty...
                        else:
                            # Check if the piece in Bottom-Right is a Black Piece
                            new_pos = (new_pos_x, new_pos_y2)
                            if new_pos in self.black_pieces:
                                # If it is a Black Piece, check Bottom-Right of it
                                new_pos_x1 = new_pos_x + 1
                                new_pos_y22 = new_pos_y2 + 1
                                # If Bottom-Right of the Black Piece isn't out of bounds...
                                if valid_pos(new_pos_x1) and valid_pos(new_pos_y22):
                                    # If Bottom-Right of the Black Piece is empty,
                                    # return True and the coords of it.
                                    if self.matrix[new_pos_x1][new_pos_y22].cellIsEmpty():
                                        return True, (new_pos_x1, new_pos_y22)
                                    # If Bottom-Right of the Black Piece isn't empty,
                                    # can't move to it; so return False
                                    else:
                                        return False
                                # If Bottom-Right of the Black Piece is outta bounds,
                                # can't move to it; so return False.
                                else:
                                    return False
                            # If Bottom-Right isn't a Black Piece (It is surely a White Piece since it wasn't an empty cell),
                            # can't move to it; so return False.
                            else:
                                return False
                # If a White Soldier Piece can't move down, it is a King Piece.
                # We don't deal with King Pieces here, so return False.
                else:
                    return False
    
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

bpieces = gboard.getWhitePieces()
for piece in bpieces:
    if gboard.piece_can_move(bpieces[piece]):
        print(piece, gboard.piece_can_move(bpieces[piece])[1])
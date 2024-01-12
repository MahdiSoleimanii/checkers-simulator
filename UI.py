import pygame
import sys
from game_logic import *
from game_algo import *

WIDTH, HEIGHT = 800, 800
CELL_SIZE = WIDTH // 8
FPS = 30

CREAM = (139, 69, 19)
BROWN = (255, 253, 208)
WHITE = (255, 255, 255)
BLACK = (32, 32, 32)
CROWN_COLOR = (255, 215, 0)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers Game")

class CheckersUI:
    def __init__(self):
        self.gboard = GameBoard()
        self.game = Checkers(self.gboard, 5, 3, 6)

    def draw_board(self):
        for i in range(8):
            for j in range(8):
                rotated_x = j * CELL_SIZE
                rotated_y = (7 - i) * CELL_SIZE

                pygame.draw.rect(screen, BROWN if (i + j) % 2 == 0 else CREAM, (rotated_x, rotated_y, CELL_SIZE, CELL_SIZE))

                if (i, j) in self.gboard.get_black_pieces():
                    piece = self.gboard.get_black_pieces()[(i, j)]
                    self.draw_piece(rotated_x, rotated_y, BLACK, piece)
                elif (i, j) in self.gboard.get_white_pieces():
                    piece = self.gboard.get_white_pieces()[(i, j)]
                    self.draw_piece(rotated_x, rotated_y, WHITE, piece)
                    
    def draw_piece(self, x, y, color, piece):
        pygame.draw.circle(screen, color, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 2 - 5)

        if not piece.is_soldier():
            crown_size = CELL_SIZE // 2
            crown_x = x + (CELL_SIZE - crown_size) // 2
            crown_y = y + (CELL_SIZE - crown_size) // 2

            if piece.get_color() == 'B':
                crown_image = pygame.image.load("black_crown.png")  
            else:
                crown_image = pygame.image.load("white_crown.png")  

            screen.blit(pygame.transform.scale(crown_image, (crown_size, crown_size)), (crown_x, crown_y))
    
    def play(self):
        clock = pygame.time.Clock()
        running = True

        screen.fill(BROWN)
        self.draw_board()
        
        turn = True
        while not self.gboard.game_ended():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            player = 'W' if turn else 'B'
            depth = self.game.WHITE_DEPTH if turn else self.game.BLACK_DEPTH
            self.gboard = self.game.play(self.gboard, player, depth)
            turn = not turn

            screen.fill(BROWN)
            self.draw_board()

            pygame.display.flip()
            clock.tick(FPS)
            pygame.time.wait(30)

            if not running:
                break

        pygame.quit()
        sys.exit()

checkers_ui = CheckersUI()
checkers_ui.play()
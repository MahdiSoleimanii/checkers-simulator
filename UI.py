import pygame
import sys
from game_logic import *
from game_algo import *

# Constants
WIDTH, HEIGHT = 800, 800
CELL_SIZE = WIDTH // 8
FPS = 30

# Colors
CREAM = (139, 69, 19)
BROWN = (255, 253, 208)
WHITE = (255, 255, 255)
BLACK = (32, 32, 32)
CROWN_COLOR = (255, 215, 0)

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers Game")


# Checkers game logic class
class CheckersUI:
    def __init__(self):
        self.game = Checkers(GameBoard())
        self.steps = self.game.start()
        self.current_step = 0

    def draw_board(self):
        for i in range(8):
            for j in range(8):
                pygame.draw.rect(screen, BROWN if (i + j) % 2 == 0 else CREAM, (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                if (i, j) in self.game.game_board.get_black_pieces():
                    piece = self.game.game_board.get_black_pieces()[(i, j)]
                    self.draw_piece(i * CELL_SIZE, j * CELL_SIZE, BLACK, piece)
                elif (i, j) in self.game.game_board.get_white_pieces():
                    piece = self.game.game_board.get_white_pieces()[(i, j)]
                    self.draw_piece(i * CELL_SIZE, j * CELL_SIZE, WHITE, piece)

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

        for step in self.steps:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill(BROWN)
            self.game.game_board = step  # Update the game board to the current step
            self.draw_board()

            pygame.display.flip()
            clock.tick(FPS)
            pygame.time.wait(1000)  # Adjust the delay time between moves (milliseconds)

            if not running:
                break

        pygame.quit()
        sys.exit()
# Run the game
checkers_ui = CheckersUI()
checkers_ui.play()

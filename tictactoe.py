import numpy as np
import pygame
import math

# Constants
ROWS, COLUMNS = 3, 3
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WIDTH, HEIGHT = 600, 600
SIZE = (WIDTH, HEIGHT)

# Load images
CIRCLE = pygame.image.load("circle.png")
CROSS = pygame.image.load("x.png")

# Initialize board
board = np.zeros((ROWS, COLUMNS))

# Pygame setup
pygame.init()
window = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Tic-Tac-Toe")
window.fill(WHITE)

# Functions
def mark(row, col, player):
    board[row][col] = player

def is_valid_mark(row, col):
    return board[row][col] == 0

def is_board_full():
    return not (board == 0).any()

def draw_board():
    for c in range(COLUMNS):
        for r in range(ROWS):
            if board[r][c] == 1:
                window.blit(CIRCLE, ((c * 200) + 50, (r * 200) + 50))
            elif board[r][c] == 2:
                window.blit(CROSS, ((c * 200) + 50, (r * 200) + 50))  # FIXED CROSS IMAGE!
    pygame.display.update()

def draw_lines():
    pygame.draw.line(window, BLACK, (200, 0), (200, 600), 10)
    pygame.draw.line(window, BLACK, (400, 0), (400, 600), 10)
    pygame.draw.line(window, BLACK, (0, 200), (600, 200), 10)
    pygame.draw.line(window, BLACK, (0, 400), (600, 400), 10)

def is_winning_move(player):
    winning_color = BLUE if player == 1 else RED

    # Check rows
    for r in range(ROWS):
        if all(board[r][c] == player for c in range(COLUMNS)):
            pygame.draw.line(window, winning_color, (10, (r * 200) + 100), (WIDTH - 10, (r * 200) + 100), 10)
            return True

    # Check columns
    for c in range(COLUMNS):
        if all(board[r][c] == player for r in range(ROWS)):
            pygame.draw.line(window, winning_color, ((c * 200) + 100, 10), ((c * 200) + 100, HEIGHT - 10), 10)
            return True

    # Check diagonals
    if all(board[i][i] == player for i in range(ROWS)):
        pygame.draw.line(window, winning_color, (10, 10), (590, 590), 10)
        return True

    if all(board[i][ROWS - 1 - i] == player for i in range(ROWS)):
        pygame.draw.line(window, winning_color, (590, 10), (10, 590), 10)
        return True

    return False

# Game variables
game_over = False
Turn = 0
running = True

# Draw initial board
draw_lines()
pygame.display.update()

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Ensure proper exit
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            row = math.floor(event.pos[1] / 200)
            col = math.floor(event.pos[0] / 200)

            if is_valid_mark(row, col):
                mark(row, col, 1 if Turn % 2 == 0 else 2)
                if is_winning_move(1 if Turn % 2 == 0 else 2):
                    game_over = True
                Turn += 1

            draw_board()

    # Check for full board (tie)
    if is_board_full() and not game_over:
        game_over = True

    if game_over:
        font = pygame.font.Font(None, 40)
        text = font.render("Game Over! Click to Restart", True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        window.blit(text, text_rect)
        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    board.fill(0)  # Reset board properly
                    window.fill(WHITE)
                    draw_lines()
                    draw_board()
                    game_over = False
                    Turn = 0
                    waiting = False
                    pygame.display.update()

pygame.quit()

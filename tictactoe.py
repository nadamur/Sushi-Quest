import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up screen dimensions and colors
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
BACKGROUND_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
O_COLOR = (84, 84, 84)
X_COLOR = (250, 235, 215)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BACKGROUND_COLOR)

# Initialize board
board = [[None for _ in range(3)] for _ in range(3)]

def draw_lines():
    # Draw vertical lines
    pygame.draw.line(screen, LINE_COLOR, (200, 0), (200, 600), 15)
    pygame.draw.line(screen, LINE_COLOR, (400, 0), (400, 600), 15)

    # Draw horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (0, 200), (600, 200), 15)
    pygame.draw.line(screen, LINE_COLOR, (0, 400), (600, 400), 15)

def draw_O(row, col):
    center_x = col * 200 + 100
    center_y = row * 200 + 100
    pygame.draw.circle(screen, O_COLOR, (center_x, center_y), 60, 15)

def draw_X(row, col):
    x1 = col * 200 + 55
    y1 = row * 200 + 55
    x2 = col * 200 + 145
    y2 = row * 200 + 145
    pygame.draw.line(screen, X_COLOR, (x1, y1), (x2, y2), 15)
    pygame.draw.line(screen, X_COLOR, (x2, y1), (x1, y2), 15)

def check_winner(player):
    for row in range(3):
        if all(board[row][col] == player for col in range(3)):
            return True

    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    if all(board[i][i] == player for i in range(3)):
        return True

    if all(board[i][2 - i] == player for i in range(3)):
        return True

    return False

def is_board_full():
    return all(board[row][col] is not None for row in range(3) for col in range(3))

def computer_move():
    empty_cells = [(row, col) for row in range(3) for col in range(3) if board[row][col] is None]
    if not empty_cells:
        return None

    row, col = random.choice(empty_cells)
    board[row][col] = 'X'
    draw_X(row, col)

game_over = False
player_turn = True

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not game_over and player_turn and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            row, col = y // 200, x // 200
            if board[row][col] is None:
                board[row][col] = 'O'
                draw_O(row, col)
                if check_winner('O'):
                    print("Player wins!")
                    game_over = True
                elif is_board_full():
                    print("It's a draw!")
                    game_over = True
                else:
                    player_turn = False

    if not game_over and not player_turn:
        computer_move()
        if check_winner('X'):
            print("Computer wins!")
            game_over = True
        elif is_board_full():
            print("It's a draw!")
            game_over = True
        else:
            player_turn = True

    draw_lines()
    pygame.display.update()

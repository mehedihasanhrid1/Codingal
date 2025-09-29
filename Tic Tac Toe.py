import pygame
import sys
import random
pygame.init()

WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (237, 7, 7)
TEXT_COLOR = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BG_COLOR)
font = pygame.font.Font(None, 60)
score_font = pygame.font.Font(None, 40)
board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

score_X = 0
score_O = 0
score_draw = 0

def draw_lines():
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                                          row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE),
                                 CROSS_WIDTH)

def draw_scores():
    score_text = f"X: {score_X}   O: {score_O}   Draws: {score_draw}"
    text = score_font.render(score_text, True, TEXT_COLOR)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 25))
    screen.blit(text, text_rect)

def check_winner(player):
    for row in range(BOARD_ROWS):
        if all(board[row][col] == player for col in range(BOARD_COLS)):
            return True
    for col in range(BOARD_COLS):
        if all(board[row][col] == player for row in range(BOARD_ROWS)):
            return True
    if all(board[i][i] == player for i in range(BOARD_ROWS)) or \
       all(board[i][BOARD_ROWS - 1 - i] == player for i in range(BOARD_ROWS)):
        return True
    return False

def show_message(message, winner=None):
    global score_X, score_O, score_draw
    screen.fill(BG_COLOR)
    text = font.render(message, True, TEXT_COLOR)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    if winner == 'X':
        score_X += 1
    elif winner == 'O':
        score_O += 1
    elif winner == 'draw':
        score_draw += 1
    draw_scores()
    pygame.display.update()
    pygame.time.delay(2000)

def restart():
    global board
    board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    screen.fill(BG_COLOR)
    draw_lines()
    draw_scores()

def is_full():
    return all(cell != " " for row in board for cell in row)

def available_moves():
    return [(r, c) for r in range(BOARD_ROWS) for c in range(BOARD_COLS) if board[r][c] == " "]

def smart_move():
    for r, c in available_moves():
        board[r][c] = 'O'
        if check_winner('O'):
            return True
        board[r][c] = " "

    for r, c in available_moves():
        board[r][c] = 'X'
        if check_winner('X'):
            board[r][c] = 'O'
            return True
        board[r][c] = " "

    if board[1][1] == " ":
        board[1][1] = 'O'
        return True
    
    for r, c in [(0,0), (0,2), (2,0), (2,2)]:
        if board[r][c] == " ":
            board[r][c] = 'O'
            return True
    return False

def computer_move():
    difficulty = 0.7  
    if random.random() < difficulty:
        if smart_move():
            return
  
    r, c = random.choice(available_moves())
    board[r][c] = 'O'

draw_lines()
draw_scores()
player = 'X'

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if player == 'X' and event.type == pygame.MOUSEBUTTONDOWN:
            mouseX = event.pos[0]
            mouseY = event.pos[1]
            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE
            if board[clicked_row][clicked_col] == " ":
                board[clicked_row][clicked_col] = player
                if check_winner(player):
                    show_message(f"Player {player} wins!", winner=player)
                    restart()
                elif is_full():
                    show_message("It's a draw!", winner='draw')
                    restart()
                player = 'O'

    if player == 'O':  
        pygame.time.delay(500)
        computer_move()
        if check_winner('O'):
            show_message("Player O wins!", winner='O')
            restart()
        elif is_full():
            show_message("It's a draw!", winner='draw')
            restart()
        player = 'X'

    draw_figures()
    draw_scores()
    pygame.display.update()


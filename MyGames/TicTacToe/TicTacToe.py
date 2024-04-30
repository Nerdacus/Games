import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 600, 600
CELL_SIZE = WIDTH // 3
BACKGROUND_COLOR = (0, 0, 0)
LINE_COLOR = (0, 255, 0)
LINE_WIDTH = 5
FONT_SIZE = 85
FONT_COLOR = (0, 255, 0)
FONT = pygame.font.Font(None, FONT_SIZE)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

board = ['#', '#', '#', '#', '#', '#', '#', '#', '#']
gameOver = False

def printBoard(board):
    for i in range(0, len(board), 3):
        row = board[i:i + 3]
        print(" ".join(row))

def checkWin(board):
    winPatterns = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for pattern in winPatterns:
        if board[pattern[0]] == board[pattern[1]] == board[pattern[2]] != '#':
            return board[pattern[0]]

    if '#' not in board:
        return 'Draw'

    return None

def drawBoard(board):
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), LINE_WIDTH)

    for i, cell in enumerate(board):
        row, col = divmod(i, 3)
        x = col * CELL_SIZE + CELL_SIZE // 2
        y = row * CELL_SIZE + CELL_SIZE // 2

        if cell == 'X':
            text = FONT.render('X', True, FONT_COLOR)
            screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))

        elif cell == 'O':
            text = FONT.render('O', True, FONT_COLOR)
            screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))

def playerTurn(board):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not gameOver:
                x, y = pygame.mouse.get_pos()
                col = x // CELL_SIZE
                row = y // CELL_SIZE
                if 0 <= col < 3 and 0 <= row < 3 and board[row * 3 + col] == '#':
                    board[row * 3 + col] = 'X'
                    return

def computerTurn(board):
    availableMoves = [i for i in range(9) if board[i] == '#']

    for move in availableMoves:
        board[move] = 'O'
        winner = checkWin(board)
        if winner == 'O':
            return
        board[move] = '#'

    for move in availableMoves:
        board[move] = 'X'
        winner = checkWin(board)
        if winner == 'X':
            board[move] = 'O'
            return
        board[move] = '#'

    if availableMoves:
        compSpot = random.choice(availableMoves)
        board[compSpot] = 'O'

def printLast(board):
    for i in range(0, len(board), 3):
        row = board[i:i+3]
        print(" ".join(row))
def play():
    global gameOver
    while not gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BACKGROUND_COLOR)
        drawBoard(board)
        pygame.display.flip()

        playerTurn(board)
        winner = checkWin(board)
        if winner:
            game_over = True
            break

        computerTurn(board)
        winner = checkWin(board)
        if winner:
            game_over = True
            break

    screen.fill((100, 100, 100))
    drawBoard(board)
    pygame.display.flip()

    if winner == 'Draw':
        print("Nobody wins :(")
    elif winner == 'X':
        print("Player wins :D")
    elif winner == 'O':
        print("Computer wins :(")

    print("Final board: ")
    printLast(board)

if __name__ == "__main__":
    play()
    pygame.quit()
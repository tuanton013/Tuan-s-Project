import pygame
import sys
import time

board = [
    [3, 0, 5, 8, 0, 0, 0, 0, 0],
    [9, 0, 0, 0, 0, 3, 0, 0, 4],
    [0, 0, 0, 0, 0, 5, 0, 0, 0],
    [0, 0, 0, 0, 8, 7, 0, 4, 0],
    [0, 0, 0, 0, 1, 0, 0, 8, 0],
    [0, 0, 0, 0, 0, 0, 5, 3, 9],
    [0, 0, 8, 0, 0, 0, 0, 0, 2],
    [0, 4, 0, 0, 0, 0, 9, 0, 0],
    [0, 7, 0, 2, 6, 0, 0, 0, 0]
]

# Pygame setup
WIDTH, HEIGHT = 540, 640
CELL_SIZE = WIDTH // 9
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Solver Visualizer")
font = pygame.font.SysFont("arial", 40)
small_font = pygame.font.SysFont("arial", 20)


def draw_board(board, highlight=None, show_button=True):
    screen.fill((255, 255, 255))
    # Draw grid lines
    for i in range(10):
        thickness = 4 if i % 3 == 0 else 1
        pygame.draw.line(screen, (0, 0, 0), (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), thickness)
        pygame.draw.line(screen, (0, 0, 0), (i * CELL_SIZE, 0), (i * CELL_SIZE, WIDTH), thickness)
    # Draw numbers
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                color = (0, 0, 255) if highlight and (i, j) == highlight else (0, 0, 0)
                text = font.render(str(board[i][j]), True, color)
                screen.blit(text, (j * CELL_SIZE + 20, i * CELL_SIZE + 10))
    # Draw highlight cell
    if highlight:
        pygame.draw.rect(screen, (255, 200, 0), (highlight[1] * CELL_SIZE, highlight[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)
    # Draw instructions
    info = small_font.render("Press ESC to quit", True, (0, 0, 0))
    screen.blit(info, (10, WIDTH + 10))
    # Draw solve button
    if show_button:
        button_rect = pygame.Rect(WIDTH//2 - 130, WIDTH + 40, 120, 40)
        pygame.draw.rect(screen, (0, 180, 0), button_rect)
        button_text = small_font.render("Solve", True, (255, 255, 255))
        screen.blit(button_text, (WIDTH//2 - 95, WIDTH + 50))
        # Draw result button
        result_rect = pygame.Rect(WIDTH//2 + 10, WIDTH + 40, 120, 40)
        pygame.draw.rect(screen, (0, 0, 180), result_rect)
        result_text = small_font.render("Result", True, (255, 255, 255))
        screen.blit(result_text, (WIDTH//2 + 45, WIDTH + 50))
    pygame.display.flip()


def is_on_solve_button(pos):
    x, y = pos
    button_rect = pygame.Rect(WIDTH//2 - 130, WIDTH + 30, 120, 40)
    return button_rect.collidepoint(x, y)


def is_on_result_button(pos):
    x, y = pos
    result_rect = pygame.Rect(WIDTH//2 + 10, WIDTH + 30, 120, 40)
    return result_rect.collidepoint(x, y)


# Find empty cell/zero in sudoku board
def find_zero(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None


# is Valid placement inboard?
def is_valid(board, row, col, value):
    # Row
    if value in board[row]:
        return False
    # Column
    for i in range(9):
        if board[i][col] == value:
            return False
    # 3x3 box
    x = (row // 3) * 3
    y = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[x + i][y + j] == value:
                return False
    return True


show_result_now = False


def solve_visual(board):
    global show_result_now
    # Collect all events once per function call
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if is_on_result_button(event.pos):
                show_result_now = True
                print("Result button clicked")
                return True  # Just break out, don't solve here

    if show_result_now:
        print("show_result_now is True, breaking out")
        return True  # Just break out, don't solve here

    zero = find_zero(board)
    if not zero:
        draw_board(board, show_button=True)
        pygame.display.flip()
        return True
    row, col = zero
    for num in range(1, 10):
        # Check for events before each step to allow interruption
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_on_result_button(event.pos):
                    show_result_now = True
                    return True  # Just break out, don't solve here
        if show_result_now:
            print("show_result_now is True, breaking out")
            return True  # Just break out, don't solve here
        if is_valid(board, row, col, num):
            board[row][col] = num
            draw_board(board, highlight=(row, col), show_button=True)
            pygame.time.delay(50)
            if solve_visual(board):
                return True
            board[row][col] = 0
            draw_board(board, highlight=(row, col), show_button=True)
            pygame.time.delay(50)
    return False


def solve_instant(board):
    zero = find_zero(board)
    if not zero:
        return True
    row, col = zero
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_instant(board):
                return True
            board[row][col] = 0
    return False


def main():
    global show_result_now
    draw_board(board)
    solving = True
    while solving:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                solving = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    solving = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_on_solve_button(event.pos):
                    show_result_now = False
                    solve_visual(board)
                    if show_result_now:
                        solve_instant(board)
                    draw_board(board, show_button=True)
                elif is_on_result_button(event.pos):
                    show_result_now = False
                    solve_instant(board)
                    draw_board(board, show_button=True)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
    draw_board(board, show_button=True)
    pygame.display.flip()
    pygame.quit()



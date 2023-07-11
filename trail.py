import math
import numpy as np
import pygame
import sys

w = 600
h = 600
p1 = 1
p2 = 2
space = 50
line_w = 10
white = (225, 225, 225)
line_color = (0, 0, 0)
n = 3
grid = np.zeros((n, n))
player = p1
win = False
maxi = True
# font_1 = pygame.font.SysFont("Arial", 30)
# img = font_1.render("Player 1 won", True, line_color)


screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(white)


def reset():
    grid.fill(0)
    screen.fill(white)
    grid_lines()


def grid_lines():
    for i in range(200, w, 200):
        pygame.draw.line(screen, line_color, (0, i), (600, i), line_w)

    for i in range(200, h, 200):
        pygame.draw.line(screen, line_color, (i, 0), (i, 600), line_w)


def mark_box(x, y, p, board):
    board[x][y] = p


def box_available(x: int, y: int, board):
    if board[x][y] == 0:
        return True
    else:
        return False


def is_box_full():
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 0:
                return False
    return True


def figures():
    for x in range(0, n):
        for y in range(0, n):
            if grid[x][y] == 1:
                pygame.draw.circle(screen, line_color, (y * 200 + 100, x * 200 + 100), 50, line_w)
            elif grid[x][y] == 2:
                pygame.draw.line(screen, line_color, (y * 200 + space, x * 200 + 200 - space),
                                 (y * 200 + 200 - space, x * 200 + space), line_w)
                pygame.draw.line(screen, line_color, (y * 200 + space, x * 200 + space),
                                 (y * 200 + 200 - space, x * 200 + 200 - space), line_w)


def check_win(p):
    # checking rows
    for i in range(3):
        k_r = 0
        for j in range(3):
            if grid[i][j] == p:
                k_r += 1
                if k_r == 3:
                    return p

    # checking columns
    for i in range(3):
        k_c = 0
        for j in range(3):
            if grid[j][i] == p:
                k_c += 1
                if k_c == 3:
                    return p

    if grid[2][0] == p and grid[1][1] == p and grid[0][2] == p:
        return p

    elif grid[0][0] == p and grid[1][1] == p and grid[2][2] == p:
        return p

    else:
        return 0


def draw_line(board, p):
    pass


def mark_emp_box(p, board):
    for i in range(n):
        for j in range(n):
            if board[i][j] == 0:
                mark_box(i, j, p, board)


best_move_x = 0
best_move_y = 0


def no_0(board):
    l1 = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                l1 += 1
    return l1


def ai_move(board):
    ll = no_0(board)
    minmax(board, 2, ll)
    mark_box(best_move_x, best_move_y, 2, board)


def minmax(board, p: int, depth):
    global best_move_y, best_move_x

    if check_win(p) == 1:
        print("-1")
        t = (-1, depth)
        return t
    if check_win(p) == 2:
        print("1")
        t = (1, depth)
        return t
    if is_box_full() or depth == 0:
        print("0")
        t = (0, depth)
        return t

    if p == 2:
        locals()
        score = -1000
        d = 1000
        for i in range(3):
            for j in range(3):
                if box_available(i, j, board):
                    mark_box(i, j, 2, board)
                    k, d_s = minmax(board, 1, depth-1)
                    mark_box(i, j, 0, board)
                    if k >= score:
                        score = k
                        dp = d
                        best_move_x = i
                        best_move_y = j
        t = (score, depth)
        return t

    if p == 1:
        locals()
        best_score = 1000
        dp = 1000
        for i in range(3):
            for j in range(3):
                if box_available(i, j, board):
                    mark_box(i, j, 1, board)
                    k, d_s = minmax(board, 2, depth-1)
                    mark_box(i, j, 0, board)
                    if k <= best_score:
                        best_score = k
                        dp = d_s
                        best_move_x = i
                        best_move_y = j

        t = (best_score, depth)
        return t


grid_lines()
while True:
    for event in pygame.event.get():
        pygame.display.update()

        if event.type == pygame.QUIT:
            print(grid)
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                win = False
                player = p1
                reset()

        if event.type == pygame.MOUSEBUTTONDOWN and not win:
            x_coor = math.floor((event.pos[0] / 200))
            y_coor = math.floor((event.pos[1] / 200))

            if box_available(y_coor, x_coor, grid) and player == p1:
                mark_box(y_coor, x_coor, player, grid)
                figures()
                pygame.display.update()
                if check_win(player) == p1:
                    win = True
                    continue
                player = p2
                if not is_box_full():
                    ai_move(grid)
                    figures()
                    pygame.display.update()
                if check_win(player) == p2:
                    win = True
                    continue
                player = p1
            pygame.display.update()

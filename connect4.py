import pgzrun
import numpy as np
import pygame
import sys
import math
ROW_COUNT = 6
COLUMN_COUNT = 7

def create_board():
	board = np.zeros((6,7))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board,col):
	return board[5][col] == 0

def get_next_open_row(board,col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def print_board(board):
	print(np.flip(board, 0))

def winning_move(board, piece):
	#check horizontal locations
	for c in range(COLUMN_COUNT - 3):
		for  r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	#check vertical locations
	for c in range(COLUMN_COUNT):
		for  r in range(ROW_COUNT - 3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	#check positively sloped diagonals
	for c in range(COLUMN_COUNT - 3):
		for  r in range(ROW_COUNT - 3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	#check negatively sloped diagonals
	for c in range(COLUMN_COUNT - 3):
		for  r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def draw_board(b):
	board = np.flip(b, 0)
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, (0,0,200), (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			if board[r][c] == 0:
				pygame.draw.circle(screen, (0,0,0), (c*SQUARESIZE+SQUARESIZE//2, r*SQUARESIZE+SQUARESIZE+SQUARESIZE//2), 45)
			elif board[r][c] == 1:
				pygame.draw.circle(screen, (200,0,0), (c*SQUARESIZE+SQUARESIZE//2, r*SQUARESIZE+SQUARESIZE+SQUARESIZE//2), 45)
			elif board[r][c] == 2:
				pygame.draw.circle(screen, (200,200,0), (c*SQUARESIZE+SQUARESIZE//2, r*SQUARESIZE+SQUARESIZE+SQUARESIZE//2), 45)
	pygame.display.update()

def gameover():
	global board, game_over, W
	pygame.draw.rect(screen, (0,0,0), (0,0,width,SQUARESIZE))
	pygame.display.update()
	if W == 1:
		label = myfont.render("RED wins", 1, (200,0,0))
		screen.blit(label, (40,10))
	else:
		label = myfont.render("YELLOW wins", 1, (200,200,0))
		screen.blit(label, (40,10))
		
	game_over = False
	W = 0
	board = create_board()
	draw_board(board)


board = create_board()
game_over = False
turn = 0

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()
clock = pygame.time.Clock()

myfont = pygame.font.SysFont("monospace", 75)
W = 0

while 1:

	pygame.time.delay(50)
	clock.tick(10)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, (0,0,0), (0,0,width,SQUARESIZE))
			posx = event.pos[0]
			if turn == 0:
				pygame.draw.circle(screen, (200,0,0), (posx, SQUARESIZE//2), 45)
			else:	
				pygame.draw.circle(screen, (200,200,0), (posx, SQUARESIZE//2), 45)

		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			#Ask player 1 input
			if turn == 0:
				posx = event.pos[0]
				col = posx//SQUARESIZE

				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, 1)

					if winning_move(board, 1):
						W = 1
						game_over = True

			#Ask player 2 input 
			else:
				posx = event.pos[0]
				col = posx//SQUARESIZE

				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, 2)

					if winning_move(board, 2):
						W = 2
						game_over = True

			turn += 1
			turn = turn % 2
			print_board(board)
			pygame.draw.rect(screen, (0,0,0), (0,0,width,SQUARESIZE))
			if turn == 0:
				pygame.draw.circle(screen, (200,0,0), (posx, SQUARESIZE//2), 45)
			else:	
				pygame.draw.circle(screen, (200,200,0), (posx, SQUARESIZE//2), 45)
			draw_board(board)

			if game_over:
				gameover()
pgzrun.go()
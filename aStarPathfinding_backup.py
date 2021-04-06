import pygame
import sys
import math
import time
from queue import PriorityQueue

WIDTH = 800 
pygame.init()
WIN = pygame.display.set_mode((WIDTH+200,WIDTH)) #window size (800x800)
pygame.display.set_caption("A* Pathfinding - 1710165") #title

#color
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
BLACK = (0,0,0)

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = width * row
        self.y = width * col
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        # self.distance = {}
        
    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.color == TURQUOISE
    
    def is_open(self):
        return self.color == GREEN
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == PURPLE
    
    def  reset(self):
        self.color = WHITE
        
    def  make_closed(self):
        self.color = TURQUOISE
    
    def  make_start(self):
        self.color = ORANGE
        
    def  make_open(self):
        self.color = GREEN
        
    def  make_barrier(self):
        self.color = BLACK
        
    def  make_end(self):
        self.color = RED
        
    def  make_path(self):
        self.color = PURPLE
        
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
        
    def update_neighbors(self, grid):
        self.neighbors = []
        #UP
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        #DOWN
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        #LEFT
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])
		#RIGHT
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        # ## diagonal line
        # #UP_LEFT
        # if self.col > 0 and self.row > 0 and not grid[self.row - 1][self.col - 1].is_barrier():
        #     self.neighbors.append(grid[self.row - 1][self.col - 1])
        # #DOWN_RIGHT
        # if self.col < self.total_rows - 1 and self.row < self.total_rows - 1 and not grid[self.row + 1][self.col + 1].is_barrier():
        #     self.neighbors.append(grid[self.row + 1][self.col + 1])
        # #UP_RIGHT
        # if  self.col < self.total_rows - 1 and self.row > 0 and not grid[self.row - 1][self.col + 1].is_barrier():
        #     self.neighbors.append(grid[self.row - 1][self.col + 1])
        # #DOWN_LEFT
        # if self.col > 0 and self.row < self.total_rows - 1 and not grid[self.row + 1][self.col - 1].is_barrier():
        #     self.neighbors.append(grid[self.row + 1][self.col - 1])
        
        
    
    def __lt__(self, other):
        return False
    
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2) #tính khoảng cách theo col + row 

def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		if not current.is_start():
			current.make_path()
		draw()

def aStarPathfinding(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue() #min_heap
	open_set.put((0, count, start))
	came_from = {}
	# f(x) = g(x) + h(x)
	# tạo dictionary g --> {[spot, score] * rows * rows}
	# tạo dictionary f --> {[spot, score] * rows * rows}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())
    
	open_set_hash = {start}
 
	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		temp = open_set.get()
		print("current",temp[0], temp[1])
		current = temp[2] # (0,0,node) --> get node
		open_set_hash.remove(current)
  
		print("=============")
		print(current.get_pos())
		print("=>")

		if current == end: # found node end --> end
			print("Successful!")
			reconstruct_path(came_from, end, draw)
			current.make_end()
			return True
		
		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()
					# return False
					print(neighbor.get_pos())
					print(g_score[neighbor], f_score[neighbor])

		if current != start:
			current.make_closed()
		
		draw()
		
		# time.sleep(1)

	return False

# tạo N x N spot
def make_grid(rows, width):
    grid = []
    gap = width // rows #Floor division, chia lấy phần nguyên 
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid

# vẽ lưới 
def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))
            
def draw(win, grid, rows, width):
	for row in grid:
		for spot in row:
			spot.draw(win)
	draw_grid(win, rows, width)
	pygame.display.update()
    
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos 
    
    row = y // gap 
    col = x // gap
    
    return row, col

def draw_button(win, width):
	smallfont = pygame.font.SysFont('Corbel', 35, bold=True)
 
	pygame.draw.line(win, BLACK, (width,0), (width, width))
	pygame.draw.rect(win, BLACK, (width, 0, 200, width))
 
	search = smallfont.render('Search' , True , RED)
	pygame.draw.rect(win, GREEN, (width+20, 15, 160, 40))
	win.blit(search , (width + 55, 20))
 
	reset = smallfont.render('Reset' , True , RED)
	pygame.draw.rect(win, GREEN, (width+20, 75, 160, 40))
	win.blit(reset , (width + 60, 80))
 
	pygame.display.update()
 
def click_button(pos, width):
	x, y = pos
	if x in range(width+20, width+160):
		if y in range(15,15+40):
			return 1
		if y in range(75,75+40):
			return 2
	return -1

def main(win, width):
	ROWS = 20
	grid = make_grid(ROWS, width)

	start = None
	end = None

	run = True
	started = False
	draw_button(win, width)
	while run:
		draw(win, grid, ROWS, width) # vẽ lại spot liên tục 
		# return 0
		for event in pygame.event.get():
			def search():
				for row in grid:
					for spot in row:
						spot.update_neighbors(grid)
				aStarPathfinding(lambda: draw(win, grid, ROWS, width), grid, start, end)
			def reset():
				print("reset!")
				start = None
				end = None
				grid = make_grid(ROWS, width)
				return [start, end, grid]
    
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and not started:
					search()
				if event.key == pygame.K_q:
					reset_grid = reset()
					start = reset_grid[0]
					end = reset_grid[1]
					grid = reset_grid[2]
					
			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				if click_button(pos, width) == 1:
					search()
				if click_button(pos, width) == 2:
					reset_grid = reset()
					start = reset_grid[0]
					end = reset_grid[1]
					grid = reset_grid[2]
				if row >= ROWS or col >= ROWS+1:
					continue
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.make_start()
				elif not end and spot != start:
					end = spot
					end.make_end()
				elif spot != end and spot != start: 
					spot.make_barrier()
			if pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				if row >= ROWS or col >= ROWS:
					continue
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None
	pygame.quit()
  
if __name__ == '__main__':
	main(WIN, WIDTH)
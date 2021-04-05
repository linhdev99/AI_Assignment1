import random
import pygame
import time

WIDTH = 800 
pygame.init()
WIN = pygame.display.set_mode((WIDTH+200,WIDTH)) #window size (800x800)
pygame.display.set_caption("N - Puzzle - 1710165") #title

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
GREEN1 = (24, 77, 71)
GREEN2 = (150, 187, 124)
YELLOW1 = (250, 213, 134)
RED1 = (198, 71, 86)

step = 0
root_state = []

class Spot:
	def __init__(self, row, col, width, txt):
		self.row = row
		self.col = col
		self.x = width * row
		self.y = width * col
		self.color = WHITE
		self.width = width
		self.txt = txt
	
	def set_text(self, value):
		self.txt = value
	
	def set_color(self, color):
		self.color = color
  
	def get_value(self):
		return int(self.txt)
 
	def draw(self, win):
		lable = None
		lable_text = ""
		bg_color = GREY
		smallfont = pygame.font.SysFont('Roboto', 55, bold=False)
		if self.txt != 0:
			lable_text = str(self.txt)
			bg_color = GREEN2
		label = smallfont.render(lable_text , True , RED1)
		pygame.draw.rect(win, bg_color, (self.x, self.y, self.width, self.width))
		win.blit(label, ((2*self.x + self.width)/2 - 22, (2*self.y + self.width)/2 - 15))

	def __lt__(self, other):
		return False

def doubleState(n, state):
    temp = [[None] * n for x in range(n)]
    for i in range(0, n):
        for j in range(0, n):
            temp[i][j] = state[i][j].get_value()
    return temp

def move(dir, n, state):
    if dir == 0:
        newState = left(n, state)
        if newState == 0:
            return []
        return newState
        # return [checkSTF(n, newState), newState]
    elif dir == 1:
        newState = right(n, state)
        if newState == 0:
            return []
        return newState
        # return [checkSTF(n, newState), newState]
    elif dir == 2:
        newState = up(n, state)
        if newState == 0:
            return []
        return newState
        # return [checkSTF(n, newState), newState]
    else:
        newState = down(n, state)
        if newState == 0:
            return []
        return newState
        # return [checkSTF(n, newState), newState]
    
def left(n, state):
    if state == []:
        return 0
    # curState = doubleState(state)
    # global n
    for i in range(0, n):
        for j in range(0, n):
            if state[i][j] == 0:
                if j < n-1:
                    state[i][j] = state[i][j+1]
                    state[i][j+1] = 0
                    return state
    return 0

def right(n, state):
    if state == []:
        return 0
    for i in range(0, n):
        for j in range(0, n):
            if state[i][j] == 0:
                if j > 0:
                    state[i][j] = state[i][j-1]
                    state[i][j-1] = 0
                    # print(state)
                    return state
    return 0

def up(n, state):
    if state == []:
        return 0
    # curState = doubleState(state)
    # global n
    for i in range(0, n):
        for j in range(0, n):
            if state[i][j] == 0:
                if i < n-1:
                    state[i][j] = state[i+1][j]
                    state[i+1][j] = 0
                    return state
    return 0

def down(n, state):
    if state == []:
        return 0
    # curState = doubleState(state)
    # global n
    for i in range(0, n):
        for j in range(0, n):
            if state[i][j] == 0:
                if i > 0:
                    state[i][j] = state[i-1][j]
                    state[i-1][j] = 0
                    # print(state)
                    return state
    return 0

def checkSTF(n, state):
    global root_state
    # temp = [[0,1,2],[3,4,5],[6,7,8]]
    # temp = [[1,2,3],[8,0,4],[7,6,5]]
    SF = 0
    # global n
    for i in range(0, n):
        for j in range(0, n):
            # print(root_state[i][j].get_value(), state[i][j].get_value())
            if root_state[i][j].get_value() != state[i][j].get_value():
                SF = SF + 1
    return SF

def writeState(n, numb, state):
	for i in range(0, n):
		for j in range(0, n):
			state[i][j].set_text(int(numb[i][j]))
	return state

def printState(n, state):
	temp = []
	for i in range(0, n):
		temp.append([])
		for j in range(0, n):
			temp[i].append(state[i][j].get_value())
	print(temp)

def solveDFS(draw, n, state):
	step = 0
	SF = checkSTF(n, state)
	# printState(n, state)
	while SF > 0:
		neighborState = []
		for x in range(0,4):
			numb_state = doubleState(n, state)
			nextState = move(x, n, numb_state)
			print(nextState)
			if nextState != []:
    				neighborState.append(nextState)
		print("========")
		# idx = len(neighborState)-1
		idx = random.randint(0,len(neighborState)-1)
		# print(neighborState[idx])
		state = writeState(n, neighborState[idx], state)
		# printState(n, state)
		# print(state)
		draw()
		time.sleep(0.5)
		SF = checkSTF(n, state)
		step += 1
		if (step > 500):
			return False
	return True

def make_grid(n, width):
	grid = []
	gap = width // n #Floor division, chia lấy phần nguyên 
	count = 0
	for i in range(n):
		grid.append([])
		for j in range(n):
			spot = Spot(j, i, gap, 0)
			spot.set_text(int(count))
			count += 1
			grid[i].append(spot)
	return grid

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

def make_root(n, width):
	grid = []
	gap = width // n #Floor division, chia lấy phần nguyên 
	count = 0
	for i in range(n):
		grid.append([])
		for j in range(n):
			spot = Spot(j, i, gap, 0)
			spot.set_text(int(count))
			count += 1
			grid[i].append(spot)
	return grid 

def init_game(n, state):
	step = 50
	while step > 0:
		neighborState = []
		for x in range(0,4):
			numb_state = doubleState(n, state)
			nextState = move(x, n, numb_state)
			# print(nextState)
			if nextState != []:
				neighborState.append(nextState)
		idx = random.randint(0,len(neighborState)-1)
		state = writeState(n, neighborState[idx], state)
		step -= 1
    
	return state

def main(win, width):
    global root_state
    print("Enter n (n > 2): ")
    # n = int(input())
    print("Initial state: ")
    n = 5
    # state = [[3,1,2],[6,4,5],[0,7,8]]
    # print(state)
    root_state = make_root(n, width)
    grid = make_grid(n, width)
    state = init_game(n, grid)
    # print(n, grid)
    run = True
    started = False
    while run:
        draw(win, state, n, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    started = True
                    solveDFS(lambda: draw(win, state, n, width), n, state)
            if pygame.mouse.get_pressed()[0]: # LEFT
            	pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[2]: # RIGHT 
                pos = pygame.mouse.get_pos()
    pygame.quit()

if __name__ == "__main__":
    main(WIN, WIDTH)
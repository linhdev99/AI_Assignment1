import random
import pygame

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

n = 0
step = 0
state_used = []

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
		if value != "0":
			self.txt = value
			self.set_color(GREEN2)
		else:
			self.txt = ""
			self.set_color(GREY)
	
	def set_color(self, color):
		self.color = color
  
	def get_value(self):
		return int(self.txt)
 
	def draw(self, win):
		smallfont = pygame.font.SysFont('Roboto', 55, bold=False)
		label = smallfont.render(self.txt , True , RED1)
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
		win.blit(label, ((2*self.x + self.width)/2 - 22, (2*self.y + self.width)/2 - 15))

	def __lt__(self, other):
		return False

def doubleState(state):
    global n
    temp = [[None] * n for x in range(n)]
    for i in range(0, n):
        for j in range(0, n):
            temp[i][j] = state[i][j]
    return temp

def move(dir, state):
    if dir == 0:
        newState = left(state)
        if newState == 0:
            return [-1,[]]
        return [checkSTF(newState), newState]
    elif dir == 1:
        newState = right(state)
        if newState == 0:
            return [-1,[]]
        return [checkSTF(newState), newState]
    elif dir == 2:
        newState = up(state)
        if newState == 0:
            return [-1,[]]
        return [checkSTF(newState), newState]
    else:
        newState = down(state)
        if newState == 0:
            return [-1,[]]
        return [checkSTF(newState), newState]
    
def left(state):
    if state == []:
        return 0
    curState = doubleState(state)
    global n
    for i in range(0, n):
        for j in range(0, n):
            if curState[i][j] == 0:
                if j < n-1:
                    curState[i][j] = curState[i][j+1]
                    curState[i][j+1] = 0
                    return curState
    return 0

def right(state):
    if state == []:
        return 0
    curState = doubleState(state)
    global n
    for i in range(0, n):
        for j in range(0, n):
            if curState[i][j] == 0:
                if j > 0:
                    curState[i][j] = curState[i][j-1]
                    curState[i][j-1] = 0
                    return curState
    return 0

def up(state):
    if state == []:
        return 0
    curState = doubleState(state)
    global n
    for i in range(0, n):
        for j in range(0, n):
            if curState[i][j] == 0:
                if i < n-1:
                    curState[i][j] = curState[i+1][j]
                    curState[i+1][j] = 0
                    return curState
    return 0

def down(state):
    if state == []:
        return 0
    curState = doubleState(state)
    global n
    for i in range(0, n):
        for j in range(0, n):
            if curState[i][j] == 0:
                if i > 0:
                    curState[i][j] = curState[i-1][j]
                    curState[i-1][j] = 0
                    return curState
    return 0

def checkSTF(state):
    temp = [[0,1,2],[3,4,5],[6,7,8]]
    # temp = [[1,2,3],[8,0,4],[7,6,5]]
    SF = 0
    global n
    for i in range(0, n):
        for j in range(0, n):
            if temp[i][j] != state[i][j]:
                SF = SF + 1
    return SF


def solveDFS(state):
    print(state)
    print("=====================")
    global step 
    if (step == 500):
        print("can't solve") 
        return 0
    cloneState = doubleState(state)
    getState = move(0, cloneState)
    curState = []
    SF = []
    step = step + 1
    for x in range(0,4):
        cloneState = doubleState(state)
        getState = move(x, cloneState)
        print("Step: ", step, "[dir=",x,", st=",getState[0],"] :", getState[1])
        if getState[1] != []:
            SF.append(getState[0])
            curState.append(getState[1])
            
    # idx = random.randint(0,len(curState)-1)
    idx = len(curState)-1
    print("=> Choose", curState[idx])
    print(state,"=>",curState[idx])
    print("=====================")
    # print(curState)
    if SF[idx] == 0:
        return curState[idx]
    else:
        solveDFS(curState[idx])

def make_grid(n, state, width):
    grid = []
    gap = width // n #Floor division, chia lấy phần nguyên 
    for i in range(n):
        grid.append([])
        for j in range(n):
            spot = Spot(j, i, gap, "")
            spot.set_text(str(state[i][j]))
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

def main(win, width):
    print("Enter n (n > 2): ")
    global n
    # n = int(input())
    print("Initial state: ")
    n = 3
    state = [[3,1,2],[6,4,5],[0,7,8]]
    grid = make_grid(n, state, width)
    print(state)
    run = True
    while run:
        draw(win, grid, n, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()

if __name__ == "__main__":
    main(WIN, WIDTH)
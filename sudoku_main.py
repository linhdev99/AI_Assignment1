import random
import pygame

WIDTH = 550
background_color = (251,247,245)
text_color = (52, 31, 151)
green1_color = (24, 77, 71)
green2_color = (150, 187, 124)
yellow_color = (250, 213, 134)
red_color = (198, 71, 86)
buffer = 5
count = 0

pygame.init()
WIN = pygame.display.set_mode((WIDTH + 200, WIDTH))
pygame.display.set_caption("Sudoku")
WIN.fill(background_color)
myfont = pygame.font.SysFont('Comic Sans MS', 35)

class Spot:
	def __init__(self, col, row, width, number):
		self.row = row
		self.col = col
		self.x = width * (row + 1)
		self.y = width * (col + 1)
		self.text_color = text_color
		self.bg_color = green2_color
		self.width = width
		self.number = number

	def set_number(self, value):
		self.number = value

	def get_number(self):
		return self.number
	
	def set_textcolor(self, color):
		self.text_color = color
  
	def set_bgcolor(self, color):
			self.bg_color = color

	def draw(self, win):
		txt_number = str(self.number)
		if (self.number == 0):
			txt_number = ""
		value = myfont.render(txt_number, True, self.text_color)
		pygame.draw.rect(win, self.bg_color, (self.x, self.y, self.width, self.width))
		win.blit(value, ((self.row+1)*self.width  + 15, (self.col+1)*self.width ))

	def __lt__(self, other):
		return False
  
def valid_location(grid,row,col,number):
	for i in range(0, 9):
		if grid[row][i] == number:
			return False
		if grid[i][col] == number:
			return False
	x = row//3 * 3
	y = col//3 * 3
	for i in range(0, 3):
		for j in range(0, 3):
			if grid[x+i][y+j] == number:
				return False
	return True

def check_empty(grid):
	for i in range(0, 9):
		for j in range(0, 9):
			if grid[i][j] == 0:
				return True
	return False

def print_grid(grid):
	for i in range(0, 9):
		print(grid[i])
  
def generate_solution(grid):
	global count
	count += 1
	if count > 900:
		return False
	number_list = [1,2,3,4,5,6,7,8,9]
	random.shuffle(number_list)
	for i in range(0, 9):
		grid[0][i] = number_list[i]
	for row in range(1, 9):
		for col in range(0, 9):
			random.shuffle(number_list)      
			# print(row, col, number_list)
			for number in number_list:
				if valid_location(grid,row,col,number):
					grid[row][col] = number
					break
	# print_grid(grid)
	# return
	if check_empty(grid):
		grid = [[0] * 9 for x in range(0, 9)]
		return generate_solution(grid)
	else:
		# print(count)
		# print_grid(grid)
		return grid

def randomIDX(used_idx):
	while True:
		x = random.randint(0,8)
		y = random.randint(0,8)
		idx = x*10+y
		if not idx in used_idx:
			return [x,y]

def clone_grid(grid):
	temp = []
	for i in range(9):
		temp.append([])
		for j in range(9):
			temp[i].append(grid[i][j])
	return temp

def initial_grid(grid_solution):
	step = [38, 45, 52, 57] # easy: 38, normal: 45, difficult: 52, master: 57
	used_idx = []
	random.shuffle(step)
	grid = clone_grid(grid_solution)
	for i in range(step[0]):
		idx = randomIDX(used_idx)
		x = idx[0]
		y = idx[1]
		used_idx.append(x*10+y)
		grid[x][y] = 0
	return grid

def make_grid(win, width, grid):
	grid_spot = []
	gap = width // 11 
	for i in range(0, 9):
		grid_spot.append([])
		for j in range(0, 9):
			spot = Spot(i, j, gap, grid[i][j])
			grid_spot[i].append(spot)
			if (grid[i][j] == 0):
				spot.set_bgcolor(yellow_color)
				spot.set_textcolor(green1_color)
			else:
				spot.set_bgcolor(green2_color)
				spot.set_textcolor(text_color)
	return grid_spot

def draw_grid(win, width):
	gap = width // 11
	for i in range(0,10):
		if(i%3 == 0):
			pygame.draw.line(win, (0,0,0), (gap + gap*i, gap), (gap + gap*i ,width - gap ), 4 )
			pygame.draw.line(win, (0,0,0), (gap, gap + gap*i), (width - gap, gap + gap*i), 4 )

		pygame.draw.line(win, (0,0,0), (gap + gap*i, gap), (gap + gap*i ,width - gap ), 2 )
		pygame.draw.line(win, (0,0,0), (gap, gap + gap*i), (width - gap, gap + gap*i), 2 )
	pygame.display.update()
 
def draw_button(win, width):
	smallfont = pygame.font.SysFont('Corbel', 35, bold=True)
 
	pygame.draw.line(win, green1_color, (width,0), (width, width))
	pygame.draw.rect(win, green1_color, (width, 0, 200, width))
 
	search = smallfont.render('Solve' , True , red_color)
	pygame.draw.rect(win, green2_color, (width+20, 15, 160, 40))
	win.blit(search , (width + 55, 20))
 
	reset = smallfont.render('Reset' , True , red_color)
	pygame.draw.rect(win, green2_color, (width+20, 75, 160, 40))
	win.blit(reset , (width + 55, 80))
 
def click_button(pos, width):
	x, y = pos
	if x in range(width+20, width+160):
		if y in range(15,15+40):
			return 1
		if y in range(75,75+40):
			return 2
		if y in range(135,135+40):
				return 3
	return -1
 
def draw(win, grid, width):
	for row in grid:
		for spot in row:
			spot.draw(win)
	draw_grid(win, width)
	draw_button(win, width)
	pygame.display.update()

def solve_sudoku(grid):
	return grid

def draw_solution(grid_spot, grid):
	i = 0
	j = 0
	for row in grid_spot:
		j = 0
		for spot in row:
			spot.set_number(grid[i][j])
			j += 1
		i += 1
	return grid_spot

def print_gridspot(grid_spot):
	grid = []
	i = 0
	j = 0
	for row in grid_spot:
		grid.append([])
		j = 0
		for spot in row:
			grid[i].append(spot.get_number())
			j += 1
		i += 1
	print(grid)    

def create_empty_grid():
	return [[0] * 9 for x in range(0, 9)]

def main(win, width):
	grid = create_empty_grid()
	grid_original = generate_solution(grid)
	# print_grid(grid_original)	
	grid_initial = initial_grid(grid_original)
	grid_spot = make_grid(win, width, grid_initial)
	
	while True: 
		draw(win, grid_spot, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				return
			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				if click_button(pos, width) == 1:
					grid_solved = solve_sudoku(grid_initial)
					grid_spot = draw_solution(grid_spot, grid_solved)
				if click_button(pos, width) == 2:
					global count
					count = 0
					grid = create_empty_grid()
					grid_original = generate_solution(grid)
					if not grid_original:
						continue
					grid_initial = initial_grid(grid_original)
					grid_spot = make_grid(win, width, grid_initial)
			if pygame.mouse.get_pressed()[2]: # RIGHT 
				pos = pygame.mouse.get_pos()
	
if __name__ == '__main__':
	main(WIN, WIDTH)
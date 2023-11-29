from enum import IntEnum, auto
import random

class Board(IntEnum):
	EMPTY = auto()
	SNAKE = auto()
	FOOD = auto()

class Direction(IntEnum):
	LEFT = auto()
	RIGHT = auto()
	UP = auto()
	DOWN = auto()

class Action(IntEnum):
	STRAIGHT = auto()
	LEFT = auto()
	RIGHT = auto()

class Snake_Env():

	def generate_food(self):
		self.food = (random.randint(0, self.board_width-1), random.randint(0, self.board_height-1))
		while self.food in self.positions:
			self.food = (random.randint(0, self.board_width-1), random.randint(0, self.board_height-1))
	
	def __init__(self, board_width, board_height):
		self.board_width = board_width
		self.board_height = board_height
		self.positions = [(self.board_width // 2, self.board_height // 2)]
		self.generate_food()
		self.direction = Direction(random.randint(1, 4))
		self.score = 0
		self.state_space = 2 ** 11 - 1
		self.action_space = 3

	def reset(self):
		self.positions = [(self.board_width // 2, self.board_height // 2)]
		self.generate_food()
		self.direction = Direction.RIGHT
		self.score = 0
		return self.get_state()

	def head(self):
		return self.positions[-1]
	
	def get_board(self): #get board 2d array
		board = [[Board.EMPTY for j in range(self.board_height)] for i in range(self.board_width)]
		for snake in self.positions:
			board[snake[0]][snake[1]] = Board.SNAKE
		board[self.food[0]][self.food[1]] = Board.FOOD
		return board

	def collision(self, position):
		return position[0] < 0 or position[0] >= self.board_width or position[1] < 0 or position[1] >= self.board_height or position in self.positions

	def get_state(self):
		left_collision = self.collision(self.head()+(-1,0))
		right_collision = self.collision(self.head()+(1,0))
		up_collision = self.collision(self.head()+(0,-1))
		down_collsion = self.collision(self.head()+(0,1))

		if self.direction is Direction.LEFT:
			danger_straight = left_collision
			danger_left = down_collsion
			danger_right = up_collision
		elif self.direction is Direction.RIGHT:
			danger_straight = right_collision
			danger_left = up_collision
			danger_right = down_collsion
		elif self.direction is Direction.UP:
			danger_straight = up_collision
			danger_left = left_collision
			danger_right = right_collision
		elif self.direction is Direction.DOWN:
			danger_straight = down_collsion
			danger_left = right_collision
			danger_right = left_collision

		food_left = self.food[0] < self.head()[0]
		food_right = self.food[0] > self.head()[0]
		food_up = self.food[1] < self.head()[1]
		food_down = self.food[1] > self.head()[1]

		state_tuple = (self.direction, danger_straight, danger_left, danger_right, food_left, food_right, food_up, food_down)
		binary_string = ''.join('1' if bit else '0' for bit in state_tuple)
		return int(binary_string, 2)

	def step(self, action):
		reward = 0
		terminated = False

		new_position = None

		if self.direction is Direction.LEFT and action == Action.STRAIGHT or self.direction is Direction.DOWN and action == Action.RIGHT or self.direction is Direction.UP and action == Action.LEFT:
			new_position = tuple(x + y for x, y in zip(self.head(), (-1, 0)))
			self.direction = Direction.LEFT
		elif self.direction is Direction.RIGHT and action == Action.STRAIGHT or self.direction is Direction.DOWN and action == Action.LEFT or self.direction is Direction.UP and action == Action.RIGHT:
			new_position = tuple(x + y for x, y in zip(self.head(), (1, 0)))
			self.direction = Direction.RIGHT
		elif self.direction is Direction.UP and action == Action.STRAIGHT or self.direction is Direction.LEFT and action == Action.RIGHT or self.direction is Direction.RIGHT and action == Action.LEFT:
			new_position = tuple(x + y for x, y in zip(self.head(), (0, -1)))
			self.direction = Direction.UP
		elif self.direction is Direction.DOWN and action == Action.STRAIGHT or self.direction is Direction.LEFT and action == Action.LEFT or self.direction is Direction.RIGHT and action == Action.RIGHT:
			new_position = tuple(x + y for x, y in zip(self.head(), (0, 1)))
			self.direction = Direction.DOWN

		if new_position is None:
			print(self.direction, action)
			raise ValueError("new position = None")

		if self.collision(new_position):
			reward = -10
			terminated = True
		elif new_position == self.food: # food condition here
			reward = 10
			self.score += 1
			self.positions.append(new_position)
			self.generate_food()
		else:
			self.positions.append(new_position)
			self.positions.pop(0)

		return (self.get_state(), reward, terminated)
	
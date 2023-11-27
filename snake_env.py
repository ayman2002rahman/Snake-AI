from enum import enum, auto
import random

class Board(Enum):
	EMPTY = auto()
	SNAKE = auto()
	FOOD = auto()

class Direction(Enum):
	LEFT = auto()
	RIGHT = auto()
	UP = auto()
	DOWN = auto()

class Action(Enum):
	STRAIGHT = auto()
	LEFT = auto()
	RIGHT = auto()

BOARD_WIDTH = 50
BOARD_HEIGHT = 50

class Snake_Env():

	def generate_food(self):
		self.food = (random.randint(0, BOARD_WIDTH-1), random.randint(0, BOARD_HEIGHT-1))
		while self.food not in self.positions:
			self.food = (random.randint(0, BOARD_WIDTH-1), random.randint(0, BOARD_HEIGHT-1))
	
	def __init__(self):
		self.positions = [(BOARD_WIDTH // 2, BOARD_HEIGHT // 2)]
		self.food = (random.randint(0, BOARD_WIDTH-1), random.randint(0, BOARD_HEIGHT-1))
		while self.food not in self.positions:
			self.food = (random.randint(0, BOARD_WIDTH-1), random.randint(0, BOARD_HEIGHT-1))
		self.direction = Direction.RIGHT
		self.score = 0

	def reset(self):
		self.positions = [(BOARD_WIDTH // 2, BOARD_HEIGHT // 2)]
		self.food = (random.randint(0, BOARD_WIDTH-1), random.randint(0, BOARD_HEIGHT-1))
		while self.food not in self.positions:
			self.food = (random.randint(0, BOARD_WIDTH-1), random.randint(0, BOARD_HEIGHT-1))
		self.direction = Direction.RIGHT
		self.score = 0

	def head(self):
		return self.positions[-1]
	
	def get_board(self): #get board 2d array
		board = [[Board.NOTHING for j in range(BOARD_HEIGHT)] for i in range(BOARD_WIDTH)]
		for snake in self.positions:
			board[snake[0]][snake[1]] = Board.SNAKE
		board[self.food[0]][self.food[1]] = Board.FOOD
		return board

	def collision(self, position):
		return position[0] < 0 or position[0] >= BOARD_WIDTH or position[1] < 0 or position[1] >= BOARD_HEIGHT or position in self.positions

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

		return (self.direction, danger_straight, danger_left, danger_right, food_left, food_right, food_up, food_down)

	def step(self, action):
		reward = 0
		done = False

		if self.direction is Direction.LEFT and action is Action.STRAIGHT or self.direction is Direction.DOWN and action is Action.RIGHT or self.direction is Direction.UP and action is Action.LEFT:
			new_position = (self.head()+(-1,0))
		elif self.direction is Direction.RIGHT and action is Action.STRAIGHT or self.direction is Direction.DOWN and action is Action.LEFT or self.direction is Direction.UP and action is Action.RIGHT:
			new_position = (self.head()+(1,0))
		elif self.direction is Direction.UP and action is Action.STRAIGHT or self.direction is Direction.LEFT and action is Action.RIGHT or self.direction is Direction.RIGHT and action is Action.LEFT:
			new_position = (self.head()+(0,-1))
		elif self.direction is Direction.DOWN and action is Action.STRAIGHT or self.direction is Direction.LEFT and action is Action.LEFT or self.direction is Direction.RIGHT and action is Action.RIGHT:
			new_position = (self.head()+(0,1))

		if self.collision(new_position):
			reward = -10
			done = True
		elif new_position == self.food: # food condition here
			reward = 10
			score += 1
			self.position.append(new_position)
			self.generate_food()
		else:
			self.position.append(new_position)
			self.pop(0)

		return (self.get_state(), reward, done)

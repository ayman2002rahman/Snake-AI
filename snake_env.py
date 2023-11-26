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

class Snake_Env(self):
	def __init__(self):
		self.positions = [(BOARD_WIDTH // 2, BOARD_HEIGHT // 2)]
		self.food = (random.randint(0, BOARD_WIDTH-1), random.randint(0, BOARD_HEIGHT-1))
		while self.food not in self.positions:
			self.food = (random.randint(0, BOARD_WIDTH-1), random.randint(0, BOARD_HEIGHT-1))
		self.direction = Direction.RIGHT
		self.score = 0

	def head(self):
		return self.positions[0]
	
	def get_board(self): #get board 2d array
		board = [[Board.NOTHING for j in range(BOARD_HEIGHT)] for i in range(BOARD_WIDTH)]
		for snake in self.positions:
			board[snake[0]][snake[1]] = Board.SNAKE
		board[self.food[0]][self.food[1]] = Board.FOOD
		return board

	def get_state(self):
		if self.direction is Direction.LEFT:
			danger_straight = self.head()[0] - 1 < 0 or self.head()+(-1, 0) in self.positions
			danger_left = self.head()[1] + 1 >= BOARD_HEIGHT or self.head()+(0, 1) in self.positions
			danger_right = self.head()[1] - 1 < 0 or self.head()+(0, -1) in self.positions
		elif self.direction is Direction.RIGHT:
			danger_straight = self.head()[0] + 1 >= BOARD_WIDTH or self.head()+(1, 0) in self.positions
			danger_left = self.head()[1] - 1 < 0 or self.head()+(0, -1) in self.positions
			danger_right = self.head()[1] + 1 >= BOARD_HEIGHT or self.head()+(0, 1) in self.positions
		elif self.direction is Direction.UP:
			danger_straight = self.head()[1] - 1 < 0 or self.head()+(0, -1) in self.positions
			danger_left = self.head()[0] - 1 < 0 or self.head()+(-1, 0) in self.positions
			danger_right = self.head()[0] + 1 >= BOARD_WIDTH or self.head()+(1, 0) in self.positions
		elif self.direction is Direction.DOWN:
			danger_straight = self.head()[0] - 1 < 0 or self.head()+(0, 1) in self.positions
			danger_left = self.head()[1] + 1 >= BOARD_HEIGHT or self.head()+(1, 0) in self.positions
			danger_right = self.head()[1] - 1 < 0 or self.head()+(-1, 0) in self.positions

		food_left = self.food[0] < self.head()[0]
		food_right = self.food[0] > self.head()[0]
		food_up = self.food[1] < self.head()[1]
		food_down = self.food[1] > self.head[1]

		return (self.direction, danger_straight, danger_left, danger_right, food_left, food_right, food_up, food_down)

	def step(self, action):
		reward = 0
		if self.direction is Direction.LEFT and action is Action.STRAIGHT or self.direction is Direction.DOWN and action is Action.RIGHT or self.direction is Direction.UP and action is Action.LEFT:
			if self.head[0] - 1 < 0 or self.board[self.head[0] - 1, self.head[1]] is Board.SNAKE:
				reward = -10
				done = True
			else:
				#update the head and tail
				self.direction = Direction.LEFT
				head += (-1, 0)
				tail += (-1, 0)


		elif action is Action.LEFT:
			pass

		elif action is Action.RIGHT:
			pass

		return (self.get_state(), reward, done)

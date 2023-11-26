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
		self.board = [[Board.NOTHING for j in range(BOARD_HEIGHT)] for i in range(BOARD_WIDTH)]
		self.head = (BOARD_WIDTH // 2, BOARD_HEIGHT // 2)
		self.tail = self.head
		self.food = (random.randint(0, BOARD_WIDTH-1), random.randint(0, BOARD_HEIGHT-1))
		while self.board[self.food[0]][self.food[1]] is not Board.SNAKE:
			self.food = (random.randint(0, BOARD_WIDTH-1), random.randint(0, BOARD_HEIGHT-1))
		self.direction = Direction.RIGHT
		self.score = 0
	
		self.board[self.head[0]][self.head[1]] = Board.SNAKE

	def get_state(self):
		if self.direction is Direction.LEFT:
			danger_straight = self.head[0] - 1 < 0 or self.board[self.head[0]-1][self.head[1]] is Board.SNAKE
			danger_left = self.head[1] + 1 >= BOARD_HEIGHT or self.board[self.head[0]][self.head[1]+1] is Board.SNAKE
			danger_right = self.head[1] - 1 < 0 or self.board[self.head[0]][self.head[1]-1] is Board.SNAKE
		elif self.direction is Direction.RIGHT:
			danger_straight = self.head[0] + 1 >= BOARD_WIDTH or self.board[self.head[0]+1][self.head[1]] is Board.SNAKE
			danger_left = self.head[1] - 1 < 0 or self.board[self.head[0]][self.head[1]-1] is Board.SNAKE
			danger_right = self.head[1] + 1 >= BOARD_HEIGHT or self.board[self.head[0]][self.head[1]+1] is Board.SNAKE
		elif self.direction is Direction.UP:
			danger_straight = self.head[1] - 1 < 0 or self.board[self.head[0]][self.head[1]-1] is Board.SNAKE
			danger_left = self.head[0] - 1 < 0 or self.board[self.head[0]-1][self.head[1]] is Board.SNAKE
			danger_right = self.head[0] + 1 >= BOARD_WIDTH or self.board[self.head[0]+1][self.head[1]] is Board.SNAKE
		elif self.direction is Direction.DOWN:
			danger_straight = self.head[0] - 1 < 0 or self.board[self.head[0]-1][self.head[1]] is Board.SNAKE
			danger_left = self.head[1] + 1 >= BOARD_HEIGHT or self.board[self.head[0]][self.head[1]+1] is Board.SNAKE
			danger_right = self.head[1] - 1 < 0 or self.board[self.head[0]][self.head[1]-1] is Board.SNAKE

		try:
			food_left = self.food[0] < self.head[0]
		except IndexError:
			food_left = False
		try:
			food_right = self.food[0] > self.head[0]
		except IndexError:
			food_right = False
		try:
			food_up = self.food[1] < self.head[1]
		except IndexError:
			food_up = False
		try:
			food_down = self.food[1] > self.head[1]
		except IndexError:
			food_down = False

		return (self.direction, danger_straight, danger_left, danger_right, food_left, food_right, food_up, food_down)

	def step(self, action):
		if action is Action.STRAIGHT:
			if self.direction is Direction.LEFT:
				if self.head[0] - 1 < 0:
					reward = -10
					state = self.get_state()
				elif self.board[self.head[0] - 1, self.head[1]] is Board.SNAKE:
					pass

		elif action is Action.LEFT:
			pass

		elif action is Action.RIGHT:
			pass

		return (state, reward)

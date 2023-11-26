from enum import enum, auto

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
		self.board = [[BOARD.NOTHING for j in range(BOARD_HEIGHT)] for i in range(BOARD_WIDTH)]
		self.head = (BOARD_WIDTH // 2, BOARD_HEIGHT // 2)
		self.tail = self.head
		self.direction = Direction.RIGHT
		self.score = 0
	
		board[head[0][head[1]] = SNAKE

	def step(self, action):
		return ((self.direction, danger_forward, danger_left, danger_right, 

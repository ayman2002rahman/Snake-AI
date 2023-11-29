import pygame
import sys
import numpy as np
from tqdm import tqdm
from snake_env import Action, Snake_Env
from snake_ai import train_snake

env = Snake_Env(20, 20)
q_table = np.zeros((env.state_space, env.action_space))

CELL_SIZE = 20
DISPLAY_SIZE = (env.board_width*CELL_SIZE, env.board_height*CELL_SIZE)

'''
pygame.init()
screen = pygame.display.set_mode(DISPLAY_SIZE)
pygame.display.set_caption("Snake AI")
clock = pygame.time.Clock()'''

train_episodes = 500000
max_steps = 100000

learning_rate = 0.9
gamma = 0.995

max_epsilon = 1
min_epsilon = 0.1
decay_rate = 0.000005

train_snake(env, q_table, train_episodes, learning_rate, max_epsilon, min_epsilon, decay_rate, gamma)
np.save('snake_q_table.npy', q_table)
print(np.max(q_table))
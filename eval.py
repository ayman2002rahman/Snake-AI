import pygame
import sys
import numpy as np
from tqdm import tqdm
from snake_env import Action, Snake_Env
from snake_ai import greedy_policy

env = Snake_Env(20, 20)

CELL_SIZE = 20
DISPLAY_SIZE = (env.board_width*CELL_SIZE, env.board_height*CELL_SIZE)

pygame.init()
screen = pygame.display.set_mode(DISPLAY_SIZE)
pygame.display.set_caption("Snake AI")
clock = pygame.time.Clock()

def draw_game(env):
    for body in env.positions:
        pygame.draw.rect(screen, (255, 0, 0), (body[0]*CELL_SIZE, body[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, (0, 255, 0), (env.food[0]*CELL_SIZE, env.food[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.flip()

def evaluate(env, q_table, eval_episodes, max_steps, draw):
    range_looper = range(eval_episodes)
    if not draw:
        range_looper = tqdm(range_looper)
    for episode in range_looper:

        state = env.reset()
        terminated = False

        for step in range(max_steps):

            if draw:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                screen.fill((0, 0, 0))
                draw_game(env)
                clock.tick(15)

            action = greedy_policy(q_table, state)
            new_state, reward, terminated = env.step(Action(action+1))

            if terminated:
                break

            state = new_state

q_table = np.load('snake_q_table.npy')
evaluate(env, q_table, 50, 10, True)
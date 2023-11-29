from snake_env import *
import pygame
import numpy as np
from tqdm import tqdm
import time
import sys

MAX_FPS = 100
MIN_FPS = 10
DECAY_RATE_FPS = 0.01

env = Snake_Env(20, 20)
q_table = np.zeros((env.state_space, env.action_space))

CELL_SIZE = 20
DISPLAY_SIZE = (env.board_width*CELL_SIZE, env.board_height*CELL_SIZE)

pygame.init()
screen = pygame.display.set_mode(DISPLAY_SIZE)
pygame.display.set_caption("Snake AI")
clock = pygame.time.Clock()

def greedy_policy(q_table, state):
    return np.argmax(q_table[state][:])

def epsilon_greedy_policy(q_table, state, epsilon):
    if random.uniform(0, 1) > epsilon:
        action = greedy_policy(q_table, state)
    else:
        action = random.randint(0, env.action_space-1)
    return action

# helper function to draw game state
def draw_game():
    for body in env.positions:
        pygame.draw.rect(screen, (255, 0, 0), (body[0]*CELL_SIZE, body[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, (0, 255, 0), (env.food[0]*CELL_SIZE, env.food[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.flip()

def train_snake(train_episodes, learning_rate, max_epsilon, min_epsilon, decay_rate, gamma, draw=False):
    range_looper = range(train_episodes)
    if not draw:
        range_looper = tqdm(range_looper)
    for episode in range_looper:

        epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * episode)
        '''
        if episode % 10 == 0:
            print(f'Episode: {episode}   Epsilon: {epsilon}')'''

        state = env.reset() # Restarts the game so we can start another episode?
        step = 0
        terminated = False
        truncated = False

        #frame_rate = MIN_FPS + (MAX_FPS - MIN_FPS) * np.exp(-DECAY_RATE_FPS * episode)

        for step in range(max_steps):

            if draw:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                screen.fill((0, 0, 0))
                draw_game()
                #clock.tick(frame_rate)

            action = epsilon_greedy_policy(q_table, state, epsilon)
            new_state, reward, terminated = env.step(Action(action+1))
            q_table[state][action] = q_table[state][action] + learning_rate * (reward + gamma * np.max(q_table[new_state]) - q_table[state][action])

            if terminated:
                break

            state = new_state

train_episodes = 100000
max_steps = 1000

learning_rate = 0.72
gamma = 0.99

max_epsilon = 1
min_epsilon = 0.05
decay_rate = 0.001

eval_episodes = 100

'''
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    train_snake(train_episodes, learning_rate, max_epsilon, min_epsilon, decay_rate, gamma, False)'''

train_snake(train_episodes, learning_rate, max_epsilon, min_epsilon, decay_rate, gamma, False)
print(q_table)
print(np.max(q_table))

episode_rewards = []


for episode in tqdm(range(eval_episodes)):
    state = env.reset()

    step = 0
    terminated = False
    total_rewards_ep = 0

    for step in range(max_steps):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((0, 0, 0))
        draw_game()
        clock.tick(20)

        action = greedy_policy(q_table, state)
        new_state, reward, terminated = env.step(Action(action+1))
        total_rewards_ep += reward

        if terminated:
            break
        state = new_state

    episode_rewards.append(total_rewards_ep)

mean_reward = np.mean(episode_rewards)
std_reward = np.std(episode_rewards)

print(f'Mean Reward: {mean_reward:.2f} +/- {std_reward:.2f}')

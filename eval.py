import pygame
import sys
import yaml
import numpy as np
from tqdm import tqdm
from snake_env import Action, Snake_Env
from snake_ai import greedy_policy

with open('hyperparameters.yaml', 'r') as stream:
    try:
        hyperparameters = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

env = Snake_Env(hyperparameters['valid_env_size']['width'], hyperparameters['valid_env_size']['height'])

eval_episodes = hyperparameters['eval_episodes']
eval_max_steps = hyperparameters['max_steps']
display_game = hyperparameters['display_game']

if display_game:
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
    episode_rewards = []
    for episode in range_looper:

        state = env.reset()
        terminated = False
        total_rewards_ep = 0

        while True:

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
            total_rewards_ep += reward

            if terminated:
                break

            state = new_state

        if not draw:
            episode_rewards.append(total_rewards_ep)

    if not draw:
        mean_reward = np.mean(episode_rewards)
        std_reward = np.std(episode_rewards)
        return (mean_reward, std_reward)

q_table = np.load(hyperparameters['eval_q_table'])
mean_reward, std_reward = evaluate(env, q_table, 1000, 100000, display_game)
if display_game:
    print(f'Mean Reward: {mean_reward:.2f} +/- {std_reward:.2f}')
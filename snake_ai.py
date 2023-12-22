from snake_env import *
import pygame
import numpy as np
from tqdm import tqdm
import time
import sys

MAX_FPS = 100
MIN_FPS = 10
DECAY_RATE_FPS = 0.01

def greedy_policy(q_table, state):
    return np.argmax(q_table[state][:])

def epsilon_greedy_policy(env, q_table, state, epsilon):
    if random.uniform(0, 1) > epsilon:
        action = greedy_policy(q_table, state)
    else:
        action = random.randint(0, env.action_space-1)
    return action


def train_snake(env, q_table, train_episodes, max_steps, learning_rate, max_epsilon, min_epsilon, decay_rate, gamma):
    for episode in tqdm(range(train_episodes)):

        epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * episode)

        state = env.reset()
        terminated = False

        for step in range(max_steps):

            action = epsilon_greedy_policy(env, q_table, state, epsilon)
            new_state, reward, terminated = env.step(Action(action+1))
            q_table[state][action] = q_table[state][action] + learning_rate * (reward + gamma * np.max(q_table[new_state]) - q_table[state][action])

            if terminated:
                break

            state = new_state
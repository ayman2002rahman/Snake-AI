import pygame
import sys
import yaml
import numpy as np
from tqdm import tqdm
from snake_env import Action, Snake_Env
from snake_ai import train_snake

#q_table = np.zeros((env.state_space, env.action_space))
#q_table = np.random.rand(env.state_space, env.action_space)
q_table = np.load('snake_q_table_v4.npy')

with open('hyperparameters.yaml', 'r') as stream:
    try:
        hyperparameters = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

env = Snake_Env(hyperparameters['train_env_size']['width'], hyperparameters['train_env_size']['height'])

train_episodes = hyperparameters['train_episodes']
max_steps = hyperparameters['max_steps']

learning_rate = hyperparameters['learning_rate']
gamma = hyperparameters['gamma']

max_epsilon = hyperparameters['max_epsilon']
min_epsilon = hyperparameters['min_epsilon']
decay_rate = hyperparameters['decay_rate']

train_snake(env, q_table, train_episodes, max_steps, learning_rate, max_epsilon, min_epsilon, decay_rate, gamma)
np.save(hyperparameters['train_q_table'], q_table)
print(np.max(q_table))
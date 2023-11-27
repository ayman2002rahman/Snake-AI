from snake_env import *
import numpy as np
from tqdm import tqdm

env = Snake_Env()
q_table = np.zeros((env.state_space, env.action_space))

def greedy_policy(q_table, state):
    return np.argmax(q_table[state][:])

def epsilon_greedy_policy(q_table, state, epsilon):
    if random.uniform(0, 1) > epsilon:
        action = greedy_policy(q_table, state)
    else:
        action = random.randint(0, env.action_space-1)
    return action

train_episodes = 10000
learning_rate = 0.7

eval_episodes = 10
max_steps = 1000
gamma = 0.95

max_epsilon = 1
min_epsilon = 0.05
decay_rate = 0.0005

for episode in tqdm(range(train_episodes)):
    epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * episode)
    state = env.reset() # Restarts the game so we can start another episode?
    step = 0
    terminated = False
    truncated = False

    for step in range(max_steps):
        action = epsilon_greedy_policy(q_table, state, epsilon)
        new_state, reward, terminated = env.step(Action(action+1))
        q_table[state][action] = q_table[state][action] + learning_rate * (reward + gamma * np.max(q_table[new_state]) - q_table[state][action])

        if terminated:
            break

print(q_table)

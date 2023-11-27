from snake_env import *
import numpy as np
from tqdm import tqdm

env = Snake_Env()
q_table = {}

def greedy_policy(q_table, state):
    q_values = [q_table[(state, action)] for action in range(0, env.action_space)]
    return q_values.index(max(q_values))

def epsilon_greedy_policy(q_table, state, epsilon):
    if random.uniform(0, 1) > epsilon:
        action = greedy_policy(q_table, state)
    else:
        action = Action(random.randint(1, env.action_space))
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
        new_state, reward, terminated = env.step(action)
        if (state, action) in q_table:
            q_table[(state, action)] = q_table[(state, action)] + learning_rate * (reward + gamma * max(q_table[(state, action)] for action in env.action_space) - q_table[(state, action)])
        else:
            q_table[(state, action)] = learning_rate * (reward + gamma * max(q_table[(state, Action(action_int))] for action_int in range(1, env.action_space)))

        if terminated:
            break

print(q_table)

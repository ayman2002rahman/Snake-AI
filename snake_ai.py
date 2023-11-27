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

train_episodes = 1000
learning_rate = 0.7

eval_episodes = 100
max_steps = 10000
gamma = 0.99

max_epsilon = 1
min_epsilon = 0.05
decay_rate = 0.001

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

        state = new_state
        board = env.get_board()

        symbol_mapping = {
            Board.EMPTY: ' ',
            Board.SNAKE: 'O',
            Board.FOOD: 'X'
        }

        # Set the width for each cell
        cell_width = 3

        # Print the 2D array with symbols and fixed width
        for row in board:
            for element in row:
                print(f'{symbol_mapping[element]:^{cell_width}}', end='')
            print()  # Move to the next line after each row

print(q_table)
print(np.max(q_table))

episode_rewards = []

for episode in tqdm(range(eval_episodes)):
    state = env.reset()

    step = 0
    terminated = False
    total_rewards_ep = 0

    for step in range(max_steps):
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

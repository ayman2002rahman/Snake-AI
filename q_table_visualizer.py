import numpy as np

np.set_printoptions(threshold=np.inf)

q_table = np.load('snake_q_table_v2.npy')

print(q_table[36])
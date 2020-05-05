import submission
import pickle
import time
import numpy as np

np.set_printoptions(threshold=np.inf)


# How to run your implementation for Part 1
with open('./toy_example/Data_File', 'rb') as f:
    data = pickle.load(f, encoding = 'bytes')
with open('./toy_example/Centroids_File', 'rb') as f:
    centroids = pickle.load(f, encoding = 'bytes')

start = time.time()
codebooks, codes = submission.pq(data, P=2, init_centroids=centroids, max_iter = 20)
end = time.time()
time_cost_1 = end - start

# How to run your implementation for Part 2
with open('./toy_example/Query_File', 'rb') as f:
    queries = pickle.load(f, encoding = 'bytes')
with open('./example/Candidates_1', 'rb') as f:
    candi = pickle.load(f, encoding = 'bytes')


start = time.time()
candidates = submission.query(queries, codebooks, codes, T=10)
end = time.time()
time_cost_2 = end - start

# output for part 2.
print(candidates)
print(candi)


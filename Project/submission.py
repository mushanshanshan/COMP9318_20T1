import numpy as np
from scipy.spatial import distance_matrix


def pq(data, P, init_centroids, max_iter):
    data = np.array(data, dtype='float32')
    init_centroids = np.array(init_centroids, dtype='float32')
    N, M = data.shape
    K = 256
    MP = int(M / P)
    result_centroids = np.array([])

    for i in range(P):
        sliced_data = data[:, i * MP:(i + 1) * MP]
        centroids = init_centroids[i,].copy()

        for _ in range(max_iter):
            row_dis = distance_matrix(sliced_data, centroids, 1)
            row_label = np.argmin(row_dis, axis=1)

            for j in range(K):
                index_list = np.where(row_label == j)[0]

                temp_data = [sliced_data[index] for index in index_list]
                if len(temp_data) != 0:
                    centroids[j] = np.median(temp_data, axis=0)

        row_dis = distance_matrix(sliced_data, centroids, 1)
        row_label = np.argmin(row_dis, axis=1)

        if i == 0:
            result_label = np.array([row_label]).T.copy()
            result_centroids = np.array([centroids.copy()])
        else:
            temp = np.append(result_centroids, centroids)
            dim = result_centroids.shape
            result_centroids = temp.reshape(dim[0] + 1, dim[1], dim[2])
            result_label = np.column_stack((result_label, row_label)).astype(np.uint8)

    return result_centroids, result_label


def index_conv(index, sorted_matrix):
    return [sorted_matrix[i][index[i]] for i in range(len(index))]


def distance(sorted_index, dis_matrix):
    return sum([dis_matrix[i][sorted_index[i]] for i in range(len(sorted_index))])

def query(queries, codebooks, codes, T):

    #print(codes)
    Q, M = queries.shape
    P, K, _ = codebooks.shape
    N, P = codes.shape
    MP = int(M / P)
    candidates = []

    inverted_index = {}

    for i in range(N):
        if tuple(codes[i]) not in inverted_index.keys():
            inverted_index[tuple(codes[i])] = [i]
        else:
            inverted_index[tuple(codes[i])].append(i)

    one_list = np.array([np.zeros((P)).astype(np.int32)] * P)

    for i in range(P):
        one_list[i][i] = 1

    for q in range(Q):
        for i in range(P):
            sliced_data = queries[q, i * MP:(i + 1) * MP]
            row_dis = distance_matrix([sliced_data], codebooks[i], 1)

            sort_index = row_dis[0].argsort()
            if i == 0:
                sorted_matrix = np.array([sort_index])
                dis_matrix = np.array(row_dis)
            else:
                sorted_matrix = np.append(sorted_matrix, [sort_index], axis=0)
                dis_matrix = np.append(dis_matrix, row_dis, axis=0)

        
        distance_dict = {(0,) * P:distance(index_conv([0] * P, sorted_matrix), dis_matrix)}
        used_index = {}


        temp_candidate = set()

        while len(temp_candidate) < T:

            minimal_index = min(distance_dict, key = distance_dict.get)

            minimal_invert_index = tuple([sorted_matrix[i][minimal_index[i]] for i in range(len(minimal_index))])


            if minimal_invert_index in inverted_index.keys():

                add_set = tuple(inverted_index[minimal_invert_index])

                temp_candidate = temp_candidate.union(add_set)

            distance_dict.pop(minimal_index)
            used_index[minimal_index] = True


            for one in one_list:

                new_index = tuple(one + list(minimal_index))


                if new_index not in used_index.keys() and max(new_index) < 256:

                    distance_dict[new_index] = distance(index_conv(new_index, sorted_matrix), dis_matrix)



        candidates.append(temp_candidate)


    return candidates

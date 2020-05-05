## import modules here
import numpy as np
################# Question 1 #################

def dot_product(a, b):
    res = 0
    for i in range(len(a)):
        res += a[i] * b[i]
    return res

def update_sim(sim, clusters):
    new_sim = np.zeros((len(clusters), len(clusters)))
    for x in range(len(clusters)):
        for y in range(x+1, len(clusters)):
            temp_list = []
            for _x in clusters[x]:
                for _y in clusters[y]:
                    if sim[_x, _y] > 0:
                        temp_list.append(sim[_x, _y])
            new_sim[x, y] = min(temp_list)

    return new_sim



def hc(data, k):# do not change the heading of the function
    sim = np.zeros((data.shape[0], data.shape[0]))
    clusters = []

    for x in range(data.shape[0]):
        clusters.append([x])
        sim[x,x] = 0
        for y in range(x+1 , data.shape[0]):
            sim[x,y] = dot_product(data[x], data[y])
    sim_orginal = sim.copy()

    while len(clusters) > k:
        index = np.argwhere(sim == np.max(sim))
        for i in clusters[index[0][1]]:
            clusters[index[0][0]].append(i)
        del clusters[index[0][1]]
        sim = update_sim(sim_orginal,clusters)


    output_list = [0] * data.shape[0]
    for i in range(len(clusters)):
        for j in clusters[i]:
            output_list[j] = i
    return output_list

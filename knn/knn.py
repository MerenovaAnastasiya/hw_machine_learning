import k_means.kmeans as kmns
import numpy as np
import math

# количество соседей
K = 3
colors = ['red', 'blue', 'green', 'pink']

def generate_data():
    return kmns.create_data()


def generate_new_point():
    x = np.random.randint(kmns.MIN_X_VALUE, kmns.MAX_X_VALUE)
    y = np.random.randint(kmns.MIN_Y_VALUE, kmns.MAX_Y_VALUE)
    return [x, y]


def find_distance_between_points(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


#  на вход подаются данные и номера кластеров, которым они принадлежат
def knn(clusters, data, new_point):
    means_clusters = []
    means_indexes = []
    indexes_count = {}
    # формируем массив из длин от новой точки до всех
    for j in range(K):
        min = math.inf
        min_index = - 1
        for i in range(len(data)):
            distance = find_distance_between_points(new_point, data[i])
            if distance < min and i not in means_indexes:
                min = distance
                min_index = i
        means_clusters.append(clusters[min_index])
        means_indexes.append(min_index)
        if indexes_count.get(clusters[min_index]) is None:
            indexes_count.update({clusters[min_index] : 0})
        else:
            indexes_count.update({clusters[min_index]: indexes_count.get(clusters[min_index]) + 1})
    max = 0
    max_i = 0
    for k, v in indexes_count.items():
        if v > max:
            max = v
            max_i = k
    return max_i


def clustering(data):
    return kmns.k_means(data)


clusters, data = clustering(generate_data())
kmns.draw_with_different_colors(clusters, data)
new_point = generate_new_point()
new_point_cluster = knn(clusters, data, new_point)
print('The color of new point is: ' + colors[new_point_cluster])
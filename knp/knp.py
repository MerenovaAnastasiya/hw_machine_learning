import math
import matplotlib.pyplot as plt
import numpy as np

K = 4
MIN_X_VALUE = MIN_Y_VALUE = 0
MAX_X_VALUE = MAX_Y_VALUE = 100
COUNT_OF_ELEMENTS = 50
# количество цветов должно равняться количеству кластеров
colors = ['red', 'blue', 'green', 'pink']


def create_data():
    points = []
    x = np.random.randint(MIN_X_VALUE, MAX_X_VALUE, COUNT_OF_ELEMENTS)
    y = np.random.randint(MIN_Y_VALUE, MAX_Y_VALUE, COUNT_OF_ELEMENTS)
    for i in range(COUNT_OF_ELEMENTS):
        points.append([x[i], y[i]])
    adjacency_matrix = np.empty((COUNT_OF_ELEMENTS, COUNT_OF_ELEMENTS))
    for i in range(len(points)):
        adjacency_matrix[i][i] = math.inf
        for j in range(0, i):
            adjacency_matrix[j][i] = adjacency_matrix[i][j] = find_distance_between_points(points[i], points[j])
    return points, adjacency_matrix


def find_distance_between_points(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def find_min_distance_points(arr):
    return min(map(lambda distance: min(distance), arr))


# алгоритм прима, поиск минимального остовного дерева
def search_minimum_spanning_tree(adjacency_matrix):
    visited_vertex = [0]
    # храним список длин, которые вошли в минимальный остов
    edges = []
    edges_length = []
    while len(visited_vertex) < COUNT_OF_ELEMENTS:
        min = math.inf
        start = None
        end = None
        # проходимся по всем посещенным вершинам и ищем локальный минимум
        # i индекс вершины, можно по нему достать смежные вершины из adjacency_matrix
        for i in visited_vertex:
            for j in range(len(adjacency_matrix[i])):
                if adjacency_matrix[i][j] < min and j not in visited_vertex:
                    # расстояние от точки до точки
                    min = adjacency_matrix[i][j]
                    start = i
                    end = j
        visited_vertex.append(end)
        edges.append([start, end])
        edges_length.append(min)
    return edges, edges_length


def clustering(edges, edges_length):
    for i in range(K -1):
        max = 0
        max_i = 0
        for j in range(len(edges_length)):
            if edges_length[j] is not None and edges_length[j] > max:
                max = edges_length[j]
                max_i = j
        # убираем ребро
        edges_length[max_i] = None
    clusters = {}
    cluster_index = 0
    for i in range(len(edges)):
        if edges_length[i] is not None:
            if clusters.get(cluster_index) is None:
                clusters.update({cluster_index: edges[i]})
            else:
                for j in edges[i]:
                    if not clusters.get(cluster_index).__contains__(j):
                        new_list = clusters.get(cluster_index)
                        new_list.append(j)
                        clusters.update({cluster_index: new_list})
        else:
            if i != 0:
                cluster_index = cluster_index + 1
            clusters.update({cluster_index: [edges[i][1]]})

    return clusters


def draw(points, clusters):
    for k, v in clusters.items():
        for i in clusters[k]:
            plt.scatter(points[i][0], points[i][1], color=colors[k])
    plt.show()

# матрица смежности
points, adjacency_matrix = create_data()
edges, edges_length = search_minimum_spanning_tree(adjacency_matrix)
clusters = clustering(edges, edges_length)
draw(points, clusters)
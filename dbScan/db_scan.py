import numpy as np
import math
import matplotlib.pyplot as plt

# min количество точек для образования кластера
M = 2
# max возможное расстояние между 2-мя точками, находящимися в одном кластере
E = 15

MIN_X_VALUE = MIN_Y_VALUE = 0
MAX_X_VALUE = MAX_Y_VALUE = 100
COUNT_OF_ELEMENTS = 50

UNCLASSIFIED = False
NOISE = None
NOISE_COLOR = 'black'
colors = dict()


def create_data():
    points = []
    x = np.random.randint(MIN_X_VALUE, MAX_X_VALUE, COUNT_OF_ELEMENTS)
    y = np.random.randint(MIN_Y_VALUE, MAX_Y_VALUE, COUNT_OF_ELEMENTS)
    for i in range(COUNT_OF_ELEMENTS):
        points.append([x[i], y[i]])
    return points


def db_scan(data):
    cluster_id = 0
    n_points = len(data)
    classifications = [UNCLASSIFIED] * n_points
    for i in range(n_points):
        if classifications[i] == UNCLASSIFIED:
            if expand_cluster(data, classifications, i, cluster_id, E, M):
                colors.update({cluster_id: np.random.rand(3,)})
                cluster_id = cluster_id + 1
    return classifications


def expand_cluster(m, classifications, point_id, cluster_id, eps, min_points):
    seeds = region_query(m, point_id, eps)
    if len(seeds) < min_points:
        classifications[point_id] = NOISE
        return False
    else:
        classifications[point_id] = cluster_id
        for seed_id in seeds:
            classifications[seed_id] = cluster_id

        while len(seeds) > 0:
            current_point = seeds[0]
            results = region_query(m, current_point, eps)
            if len(results) >= min_points:
                for i in range(0, len(results)):
                    result_point = results[i]
                    if classifications[result_point] == UNCLASSIFIED or classifications[result_point] == NOISE:
                        classifications[result_point] = cluster_id
            seeds = seeds[1:]
        return True


def find_distance_between_points(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def eps_neighborhood(a, b, eps):
    return find_distance_between_points(a, b) < eps


def region_query(m, point_id, eps):
    n_points = len(m)
    seeds = []
    for i in range(n_points):
        if eps_neighborhood(m[point_id], m[i], eps):
            if not seeds.__contains__(i) and i != point_id:
                seeds.append(i)
    return seeds


def draw_with_different_colors(data, classifications):
    for i in range(len(data)):
        color = 'black'
        if classifications[i] is not None:
            color = colors.get(classifications[i])
        plt.scatter(data[i][0], data[i][1], color=color)
    plt.show()


data = create_data()
classifications = db_scan(data)
draw_with_different_colors(data, classifications)

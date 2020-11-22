import math
from collections import defaultdict
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
    return points


# найти мин и макс для каждой координаты и в промежутке между ними
# выбрать k рандомных точек
def generate_centers(data):
    centers = []
    all_min_max = {}
    min_format = 'min_{}'
    max_format = 'max_{}'
    num_of_coordinates = len(data[0])

    for point in data:
        for coordinate in range(num_of_coordinates):
            min_key = min_format.format(coordinate)
            max_key = max_format.format(coordinate)
            if min_key not in all_min_max or point[coordinate] < all_min_max[min_key]:
                all_min_max[min_key] = point[coordinate]
            if max_key not in all_min_max or point[coordinate] > all_min_max[max_key]:
                all_min_max[max_key] = point[coordinate]

    for i in range(K):
        randoms_centers = []
        for coordinate in range(num_of_coordinates):
            randoms_centers.append(np.random.uniform(all_min_max[min_format.format(coordinate)]))
            randoms_centers.append(np.random.uniform(all_min_max[max_format.format(coordinate)]))
        centers.append(randoms_centers)
    return centers


def update_centers(data, shortest_distance_indexes):
    new_means = defaultdict(list)
    centers = []
    for distance, point in zip(shortest_distance_indexes, data):
        new_means[distance].append(point)

    for points in new_means.values():
        centers.append(create_new_center(points))

    return centers


# среднее значение для набора точек
def create_new_center(points):
    new_center = []

    for coordinate in range(len(points[0])):
        distance_sum = 0  # dimension sum
        for point in points:
            distance_sum += point[coordinate]
        new_center.append(distance_sum / float(len(points)))

    return new_center


def find_shortest_distances(data, centers):
    shortest_intervals = []
    for point in data:
        shortest_interval = find_distance_between_points([MAX_X_VALUE, MAX_Y_VALUE], [MIN_X_VALUE, MIN_Y_VALUE])
        index_of_shortest_interval = 0
        for i in range(len(centers)):
            distance = find_distance_between_points(point, centers[i])
            if distance < shortest_interval:
                shortest_interval = distance
                index_of_shortest_interval = i
        shortest_intervals.append(index_of_shortest_interval)
    return shortest_intervals


def find_distance_between_points(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def k_means(data):
    centers = generate_centers(data)
    draw_with_centers(data, centers)
    shortest_distance_indexes = find_shortest_distances(data, centers)
    old_distances = None
    while shortest_distance_indexes != old_distances:
        draw_with_different_colors(shortest_distance_indexes, data)
        new_centers = update_centers(data, shortest_distance_indexes)
        old_distances = shortest_distance_indexes
        shortest_distance_indexes = find_shortest_distances(data, new_centers)
    return zip(shortest_distance_indexes, data)


def create_array(data, index):
    array = []
    for point in data:
        array.append(point[index])
    return array


def draw(data, title):
    x = create_array(data, 0)
    y = create_array(data, 1)
    plt.title(title)
    plt.scatter(x, y)
    plt.show()


def draw_with_centers(data, centers):
    x = create_array(data, 0)
    y = create_array(data, 1)
    for i in range(len(centers)):
        plt.scatter(centers[i][0], centers[i][1], color=colors[i])
    plt.scatter(x, y)
    plt.show()


def draw_with_different_colors(shortest_distance_indexes, data):
    for i in range(len(data)):
        plt.scatter(data[i][0], data[i][1], color=colors[shortest_distance_indexes[i]])
    plt.show()


data = create_data()
draw(data, 'Исходные значения')
k_means(data)

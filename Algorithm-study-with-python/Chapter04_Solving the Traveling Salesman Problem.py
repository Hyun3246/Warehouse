import random
from itertools import permutations
import matplotlib.pyplot as plt
import time
from collections import Counter


alltours = permutations

def distance_tour(aTour):
    return sum(distance_points(aTour[i - 1], aTour[i]) for i in range(len(aTour)))


aCity = complex

def distance_points(first, second):
    return abs(first - second)

def generate_cities(number_of_cities):
    seed = 111
    width = 500
    height = 300
    random.seed((number_of_cities, seed))
    return frozenset(aCity(random.randint(1, width), random.randint(1, height)) for c in range(number_of_cities))

# 무차별 대입 전략
def brute_forces(cities):
    return shortest_tour(alltours(cities))

# 무차별 대입 전략
def shortest_tour(tours):
    return min(tours, key=distance_tour)

# 탐욕 알고리즘
def greedy_algorithm(cities, start = None):
    C = start or first(cities)
    tour = [C]
    unvisited = set(cities - {C})
    while unvisited:
        C = nearest_neighbor(C, unvisited)
        tour.append(C)
        unvisited.remove(C)
    return tour

# 탐욕 알고리즘
def first(collection):
    return next(iter(collection))

# 탐욕 알고리즘
def nearest_neighbor(A, cities):
    return min(cities, key=lambda C: distance_points(C, A))

def visualize_tour(tour, style = 'bo-'):
    if len(tour) > 1000:
        plt.figure(figsize=(15, 10))
    start = tour[0:1]
    visualize_segment(tour + start, style)
    visualize_segment(start, 'rD')

def visualize_segment(segment, style = 'bo-'):
    plt.plot([X(c) for c in segment], [Y(c) for c in segment], style, clip_on = False)
    plt.axis('scaled')
    plt.axis('off')

def X(city):
    return city.real

def Y(city):
    return city.imag


def tsp(algorithm, cities):
    t0 = time.perf_counter()
    tour = algorithm(cities)
    t1 = time.perf_counter()
    assert Counter(tour) == Counter(cities)
    visualize_tour(tour)
    print("{}:{} cities = tour length {:.0f} (in {:.3f} sec)".format(name(algorithm), len(tour), distance_tour(tour), t1 - t0))

def name(algorithm):
    return algorithm.__name__.replace('_tsp', '')

print(tsp(brute_forces, generate_cities(10)))
print(tsp(greedy_algorithm, generate_cities(2000)))

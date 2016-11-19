'''
Ryan's TSP solver.

Run with:
    ipython ryan_solution.py data/tiny.csv bf
    ipython ryan_solution.py data/tiny.csv greedy
'''

import sys
import numpy as np
from itertools import permutations

from tsp_starter import read_cities, score_solution, \
                        create_figure, visualize_solution, \
                        euclidean


def brute_force_tsp_solver(cities, new_best_callback):
    best_dist = float("inf")
    best_solution = None
    indicies = np.arange(1, len(cities))  # we'll force starting at city 0
    for solution in permutations(indicies):
        solution = [0] + list(solution)   # remember, we start at city 0
        dist = score_solution(cities, solution)
        if dist < best_dist:
            best_dist = dist
            best_solution = solution
            new_best_callback(solution)
    return best_solution


def greedy_tsp_solver(cities, new_piece_callback, start_index=0):
    path = [start_index]
    visited = {start_index}
    new_piece_callback(path)
    num_cities = len(cities)
    while len(visited) < num_cities:
        curr_city = path[-1]
        nearest_city = None
        nearest_city_dist = float('inf')
        for i, city in enumerate(cities):
            if i in visited:
                continue
            dist = euclidean(cities[curr_city], city)
            if dist < nearest_city_dist:
                nearest_city = i
                nearest_city_dist = dist
        path.append(nearest_city)
        visited.add(nearest_city)
        new_piece_callback(path)
    return path


if __name__ == '__main__':

    if len(sys.argv) != 3:
        print 'Usage: ipython {} <data_file_path> <bf|greedy>'.format(sys.argv[0])
        sys.exit(1)

    data_file_path = sys.argv[1]
    algorithm = sys.argv[2]

    cities = read_cities(data_file_path)

    fig, axes = create_figure()

    if algorithm == 'bf':

        # Closure over cities, fig, and axes:
        def visualize_wrapper(solution, is_final=False):
            print ('FINAL SOLUTION:' if is_final else 'Best so far:'), \
                    score_solution(cities, solution), solution
            visualize_solution(cities, solution, fig, axes, block=is_final)

        solution = brute_force_tsp_solver(cities, visualize_wrapper)
        visualize_wrapper(solution, True)

    elif algorithm == 'greedy':

        # Closure over cities, fig, and axes:
        def visualize_wrapper(solution, is_final=False):
            print ('FINAL SOLUTION:' if is_final else 'Best so far:'), solution
            visualize_solution(cities, solution, fig, axes, block=is_final)

        best_score = float('inf')
        best_solution = None
        for start_index in range(len(cities)):
            solution = greedy_tsp_solver(cities, visualize_wrapper, start_index)
            visualize_wrapper(solution, False)
            score = score_solution(cities, solution)
            print 'Score:', score
            if score < best_score:
                best_score = score
                best_solution = solution
        visualize_wrapper(best_solution, True)

    else:
        print 'Unknown algorithm'


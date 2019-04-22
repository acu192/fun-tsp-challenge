'''
TSP starter code. Make this your own!

Run with: ipython tsp_starter.py
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean

plt.ion()   # turn interactive mode on


def read_cities(filepath):
    '''
    Load a TSP dataset.
    This function works for loading CSV files generated
    by the data/make_data.py script.
    '''
    cities = np.loadtxt(filepath, delimiter=',')
    return cities


def score_solution(cities, solution):
    '''
    Calculate the total distance traveled by the given solution.
    This function scores a TSP solution by computing the total
    distance the salesperson would travel. Lower is better!
    The 'solution' array must contain indices into the 'cities'
    array. Also, the 'solution' array must visit each city exactly
    once!
    '''

    if len(solution) != len(cities):
        raise Exception(('Invalid solution: len(solution) is {}, ' + \
                'but it should be {}.').format(len(solution), len(cities)))

    if set(solution) != set(range(len(cities))):
        raise Exception('Invalid solution: The solution does not ' + \
                'visit each city exactly once!')

    dist = 0.0
    for i in range(len(solution)):
        p_prev = cities[solution[i-1]]
        p_here = cities[solution[i]]
        dist += euclidean(p_prev, p_here)
    return dist


def create_figure():
    '''
    Creates a figure which `visualize_solution()` will draw onto.
    '''
    fig, axes = plt.subplots(1, 2, figsize=(15, 7))
    return fig, axes


def visualize_solution(cities, solution, fig=None, axes=None, block=True):
    '''
    Visualize the solution in a 2D plot.
    The 'cities' and 'solution' arguments are the same
    as to the `score_solution()` function.
    '''
    dist = score_solution(cities, solution) if len(solution) == len(cities) else float('NaN')

    if fig is None or axes is None:
        fig, axes = create_figure()
    ax1, ax2 = axes
    fig.suptitle('Total Distance: {}'.format(dist), fontsize=20)

    ax1.clear()
    ax1.scatter(cities[:,0], cities[:,1])

    if len(solution) == len(cities):
        path = np.hstack((solution, solution[0]))  # <-- the salesperson has to return home!
    else:
        path = solution
    ax2.clear()
    ax2.plot(cities[path,0], cities[path,1])
    ax2.scatter(cities[:,0], cities[:,1])

    if block:
        while plt.fignum_exists(fig.number):
            plt.pause(0.001)
    else:
        plt.pause(0.001)


def tsp_solver_silly(cities, new_best_solution_func = None):
    '''
    This TSP solver is super silly.
    This solver simply randomizes several solutions then
    keeps the one which is best.
    '''
    best_dist = float("inf")
    best_solution = None
    for i in range(1000):
        solution = np.arange(len(cities))
        np.random.shuffle(solution)
        dist = score_solution(cities, solution)
        if dist < best_dist:
            best_dist = dist
            best_solution = solution
            if new_best_solution_func:
                new_best_solution_func(solution)
    return best_solution


if __name__ == '__main__':

    cities = read_cities('data/tiny.csv')

    show_progress = False

    if not show_progress:

        solution = tsp_solver_silly(cities)
        visualize_solution(cities, solution)

    else:

        fig, axes = create_figure()

        # Closure over cities, fig, and axes:
        def visualize_wrapper(solution, is_final=False):
            print ('FINAL SOLUTION:' if is_final else 'Best so far:'), \
                    score_solution(cities, solution), solution
            visualize_solution(cities, solution, fig, axes, block=is_final)

        solution = tsp_solver_silly(cities, visualize_wrapper)
        visualize_wrapper(solution, True)


'''
TSP starter code. Make this your own!
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean


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

    if set(solution) != set(xrange(len(cities))):
        raise Exception('Invalid solution: The solution does not ' + \
                'visit each city exactly once!')

    dist = 0.0
    for i in xrange(len(solution)):
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
    dist = score_solution(cities, solution)

    if fig is None or axes is None:
        fig, axes = create_figure()
    ax1, ax2 = axes
    fig.suptitle('Total Distance: {}'.format(dist), fontsize=20)

    ax1.clear()
    ax1.scatter(cities[:,0], cities[:,1])

    path = np.hstack((solution, solution[0]))  # <-- the salesperson has to return home!
    ax2.clear()
    ax2.plot(cities[path,0], cities[path,1])
    ax2.scatter(cities[:,0], cities[:,1])

    if block:
        plt.ioff()
        plt.show()
    else:
        plt.ion()
        plt.pause(0.05)


def tsp_solver_silly(cities):
    '''
    This TSP solver is super silly.
    This solver simply randomizes several solutions then
    keeps the one which is best.
    '''
    best_dist = float("inf")
    best_solution = None
    for i in xrange(100):
        solution = np.arange(len(cities))
        np.random.shuffle(solution)
        dist = score_solution(cities, solution)
        if dist < best_dist:
            best_dist = dist
            best_solution = solution
    return best_solution


if __name__ == '__main__':

    cities = read_cities('data/tiny.csv')
    solution = tsp_solver_silly(cities)
    visualize_solution(cities, solution)


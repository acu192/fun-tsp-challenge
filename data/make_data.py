import numpy as np

np.random.seed(123)

def normal_points(n, x_region, y_region, x_stddev, y_stddev):
    x = np.random.normal(x_region, x_stddev, (n, 1))
    y = np.random.normal(y_region, y_stddev, (n, 1))
    return np.hstack((x, y))

def uniform_points(n, x_low, y_low, x_high, y_high):
    x = np.random.uniform(x_low, x_high, (n, 1))
    y = np.random.uniform(y_low, y_high, (n, 1))
    return np.hstack((x, y))

def make_tiny():
    return normal_points(10, 0, 0, 1, 1)

def make_small():
    p1 = normal_points(10, 0, 0, 1, 1)
    p2 = normal_points(10, 5, 5, 1, 1)
    p3 = normal_points(10, -8, 15, 1, 1)
    data = np.vstack((p1, p2, p3))
    np.random.shuffle(data)
    return data

def make_medium():
    return uniform_points(100, 0, 0, 1, 1)

def make_large():
    return uniform_points(1000, 0, 0, 1, 1)

import matplotlib.pyplot as plt

def visualize(data, ax):
    ax.scatter(data[:,0], data[:,1])

if __name__ == '__main__':
    tiny   = make_tiny()
    small  = make_small()
    medium = make_medium()
    large  = make_large()

    np.savetxt('tiny.csv',   tiny,   delimiter=',')
    np.savetxt('small.csv',  small,  delimiter=',')
    np.savetxt('medium.csv', medium, delimiter=',')
    np.savetxt('large.csv',  large,  delimiter=',')

    fig, axes = plt.subplots(2, 2)
    visualize(tiny,   axes[0,0])
    visualize(small,  axes[0,1])
    visualize(medium, axes[1,0])
    visualize(large,  axes[1,1])
    plt.show()


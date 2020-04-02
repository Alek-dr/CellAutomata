import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation


def rule30():
    return np.array([[True, True, True, False],
                     [True, True, False, False],
                     [True, False, True, False],
                     [True, False, False, True],
                     [False, True, True, True],
                     [False, True, False, True],
                     [False, False, True, True],
                     [False, False, False, False]])


def rule110():
    return np.array([[True, True, True, 0],
                     [True, True, False, 1],
                     [True, False, True, 1],
                     [True, False, False, 0],
                     [False, True, True, 1],
                     [False, True, False, 1],
                     [False, False, True, 1],
                     [False, False, False, 0]])


def rule161():
    return np.array([[True, True, True, 1],
                     [True, True, False, 0],
                     [True, False, True, 1],
                     [True, False, False, 0],
                     [False, True, True, 0],
                     [False, True, False, 0],
                     [False, False, True, 0],
                     [False, False, False, 1]])


color_map = {
    0: np.array([0, 0, 0]),
    1: np.array([255, 255, 255])
}


class CellAutomata(object):

    def __init__(self, rows, columns, rule):
        self.rule = rule
        self.r = self.rule.shape[1] - 1  # радиус
        self.k = (self.rule.shape[1] - 1) // 2  # центр
        self.n = columns
        self.rows = rows
        self.columns = columns + 2 * self.k
        self.grid = np.zeros(shape=(rows, self.columns, 4), dtype=np.uint8)
        self.generations = iter(np.arange(self.rows - 1))
        self.fig = plt.figure()
        self.im = plt.imshow(self.grid[:, :, 1:], animated=True)

    def next_step(self, i: int):
        row = self.grid[i, :, 0]
        left = self.grid[i, self.k:self.k * 2]
        right = self.grid[i, -self.k * 2:-self.k]
        self.grid[i, 0:self.k] = left
        self.grid[i, -self.k:] = right
        for j in range(self.n):
            s = row[j:j + self.r]
            for lr in self.rule:
                if np.equal(s, lr[:-1]).all():
                    self.grid[i + 1, j + self.k, 0] = lr[-1]
                    break
        for k, v in color_map.items():
            m = self.grid[:, :, 0] == k
            self.grid[m, 1:] = v
        return self.grid[:, self.k:-self.k, 1:]

    def updatefig(self, *args):
        try:
            i = next(self.generations)
            self.im.set_array(self.next_step(i))
        except StopIteration:
            pass
        return self.im,


if __name__ == '__main__':
    rt = rule30()
    ca = CellAutomata(150, 300, rt)
    ca.grid[0, 151, 0] = 1
    ca.grid[0, 151, 1:] = color_map[1]
    ani = animation.FuncAnimation(ca.fig, ca.updatefig, interval=1, blit=True)
    plt.show()

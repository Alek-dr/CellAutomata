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


class CellAutomata(object):

    def __init__(self, rows, columns, rule):
        self.grid = np.zeros(shape=(rows, columns, 4), dtype=np.uint8)
        self.rows = rows
        self.columns = columns
        self.rule = rule
        self.r = self.rule.shape[1] - 1  # радиус
        self.k = (self.rule.shape[1] - 1) % 2  # центр
        self.n = self.columns - self.r + 1
        self.generations = iter(np.arange(self.rows-1))
        self.fig = plt.figure()
        self.im = plt.imshow(self.grid[:, :, 1:], animated=True)

    def next_step(self, i: int):
        row = self.grid[i, :, 0]
        for j in range(self.n):
            s = row[j:j + self.r]
            for lr in self.rule:
                if np.equal(s, lr[:-1]).all():
                    self.grid[i + 1, j + self.k, 0] = lr[-1]
                    break
        m = self.grid[:, :, 0] == 1
        self.grid[m, 1:] = 255
        return self.grid[:, :, 1:]

    def updatefig(self, *args):
        try:
            i = next(self.generations)
            self.im.set_array(self.next_step(i))
        except StopIteration:
            pass
        return self.im,


if __name__ == '__main__':
    rt = rule30()
    ca = CellAutomata(27, 50, rt)
    ca.grid[0, 25, 0] = 1
    ca.grid[0, 25, 1:] = 255
    ani = animation.FuncAnimation(ca.fig, ca.updatefig, interval=1, blit=True)
    plt.show()

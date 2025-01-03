import numpy as np
import matplotlib.pyplot as plt

class LangtonsAnt:
    def __init__(self, width=101, height=101):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=int)
        self.x = width // 2
        self.y = height // 2
        self.direction = 0  # 0 - North, 1 - East, 2 - South, 3 - West

    def step(self):
        if self.grid[self.y, self.x] == 0:
            self.direction = (self.direction - 1) % 4
            self.grid[self.y, self.x] = 1
        else:
            self.direction = (self.direction + 1) % 4
            self.grid[self.y, self.x] = 0

        if self.direction == 0:
            self.y = (self.y - 1) % self.height
        elif self.direction == 1:
            self.x = (self.x + 1) % self.width
        elif self.direction == 2:
            self.y = (self.y + 1) % self.height
        elif self.direction == 3:
            self.x = (self.x - 1) % self.width

    def run(self, steps=11000):
        plt.figure(figsize=(8, 8))
        for _ in range(steps):
            self.step()
        plt.imshow(self.grid, cmap='binary')
        plt.title(f'Langton\'s Ant after {steps} steps')
        plt.axis('off')
        plt.show()

if __name__ == "__main__":
    width = int(input("Podaj szerokość planszy (np. 101): "))
    height = int(input("Podaj wysokość planszy (np. 101): "))
    steps = int(input("Podaj liczbę iteracji (np. 11000): "))

    ant_simulation = LangtonsAnt(width, height)
    ant_simulation.run(steps)
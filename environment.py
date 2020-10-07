import objects

GRID_HEIGHT = 15
GRID_WIDTH = 16


class Environment:

    def __init__(self):
        self.grid = []
        for i in range(GRID_HEIGHT):
            self.grid.append([])
            for j in range(GRID_WIDTH):
                if i == 0 or i == GRID_HEIGHT-1 or j == 0 or j == GRID_WIDTH-1:
                    self.grid[i].append(objects.Wall())
                elif i % 2 == 0:
                    if j % 2 == 1:
                        self.grid[i].append(objects.Floor())
                    else:
                        self.grid[i].append(objects.Wall())
                else:
                    self.grid[i].append(objects.Floor())
        for r in self.grid:
            for c in r:
                print(c.sprite, end="")
            print()

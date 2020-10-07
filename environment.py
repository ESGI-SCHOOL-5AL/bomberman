import objects
import arcade

GRID_HEIGHT = 15
GRID_WIDTH = 15


class Environment:

    def __init__(self):
        self.grid = []
        for i in range(GRID_HEIGHT):
            self.grid.append([])
            for j in range(GRID_WIDTH):
                if i == 0 or i == GRID_HEIGHT-1 or j == 0 or j == GRID_WIDTH-1:
                    wall = objects.Wall()
                    wall.setCenterPos(j, i)
                    self.grid[i].append(wall)
                elif i % 2 == 0:
                    if j % 2 == 1:
                        floor = objects.Floor()
                        floor.setCenterPos(j, i)
                        self.grid[i].append(floor)
                    else:
                        wall = objects.Wall()
                        wall.setCenterPos(j, i)
                        self.grid[i].append(wall)
                else:
                    floor = objects.Floor()
                    floor.setCenterPos(j, i)
                    self.grid[i].append(floor)

    def toSpriteList(self):
        l = arcade.SpriteList()
        for r in self.grid:
            for c in r:
                l.append(c)
        return l

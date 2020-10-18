import arcade

from ..game import objects
from ..game.player import Player
from .agent import Agent


GRID_HEIGHT = 15
GRID_WIDTH = 15

CORNERS = [
    (1, 1), (2, 1), (1, 2),
    (GRID_WIDTH-2, GRID_HEIGHT-2), (GRID_WIDTH-3,
                                    GRID_HEIGHT-2), (GRID_WIDTH-2, GRID_HEIGHT-3),
    (1, GRID_HEIGHT-2), (2, GRID_HEIGHT-2), (1, GRID_HEIGHT-3),
    (GRID_WIDTH-2, 1), (GRID_WIDTH-3, 1), (GRID_WIDTH-2, 2)
]


class Environment:

    def __init__(self):
        self.spriteList = []
        self.generateTerrain()
        self.generatePlayers()

    def generateTerrain(self):
        self.grid = []
        self.states = {}
        for i in range(GRID_HEIGHT):
            self.grid.append([])
            for j in range(GRID_WIDTH):
                if i == 0 or i == GRID_HEIGHT-1 or j == 0 or j == GRID_WIDTH-1:
                    wall = objects.Wall()
                    wall.setCenterPos(j, i)
                    self.grid[i].append(wall)
                elif i % 2 == 0:
                    if j % 2 == 1:
                        brick = objects.Brick()
                        brick.setCenterPos(j, i)
                        self.grid[i].append(brick)
                    else:
                        wall = objects.Wall()
                        wall.setCenterPos(j, i)
                        self.grid[i].append(wall)
                else:
                    brick = objects.Brick()
                    brick.setCenterPos(j, i)
                    self.grid[i].append(brick)
                self.states[(i, j)] = self.grid[i][j]

        # Remove bricks at players start position
        for pos in CORNERS:
            floor = objects.Floor()
            floor.setCenterPos(pos[0], pos[1])
            self.grid[pos[1]][pos[0]] = floor

    def reset(self):
        self.generateTerrain()
        pos = [(1, 1), (GRID_WIDTH-2, GRID_HEIGHT-2), (1, GRID_HEIGHT-2), (GRID_WIDTH-2, 1)]
        i = 0
        while i < len(self.players):
            self.players[i].setCenterPos(pos[i][0], pos[i][1])
            self.players[i].reset()
            i += 1

    def draw(self):
        self.spriteList.draw()
        for p in self.players:
            if p.alive:
                p.draw()
        # self.players.draw()

    def update(self, delta_time):
        self.spriteList = self.toSpriteList()
        for s in self.spriteList:
            s.update(delta_time)
        for p in self.players:
            p.update(delta_time)

        ok = False
        for p in self.players:
            if p.alive:
                ok = True
                break
        
        if not ok:
            self.reset()

    def toSpriteList(self):
        l = arcade.SpriteList()
        for r in self.grid:
            for c in r:
                l.append(c)
        return l

    def generatePlayers(self):
        self.players = arcade.SpriteList()
        for pos in [(1, 1), (GRID_WIDTH-2, GRID_HEIGHT-2), (1, GRID_HEIGHT-2), (GRID_WIDTH-2, 1)]:
            p = Agent(self)
            p.setCenterPos(pos[0], pos[1])
            self.players.append(p)
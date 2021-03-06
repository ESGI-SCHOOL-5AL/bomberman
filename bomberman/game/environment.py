import arcade

from ..game import objects
from ..game.player import Player
from ..reinforcement_learning.agent import Agent
from itertools import product


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

        # Remove bricks at players start position
        for pos in CORNERS:
            floor = objects.Floor()
            floor.setCenterPos(pos[0], pos[1])
            self.grid[pos[1]][pos[0]] = floor

    def generateStates(self):
        types = ["Floor", "Wall", "Brick", "Bomb", "Explosion"]
        states = [ele for ele in product(types, repeat=9)]
        result = []
        for s in states:
            result.append((s[0], s[1], s[2], s[3], s[4],
                           s[5], s[6], s[7], s[8], 0))
            result.append((s[0], s[1], s[2], s[3], s[4],
                           s[5], s[6], s[7], s[8], 1))

        return result

    def reset(self):
        self.generateTerrain()
        pos = [(1, 1), (GRID_WIDTH-2, GRID_HEIGHT-2),
               (1, GRID_HEIGHT-2), (GRID_WIDTH-2, 1)]
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
        for p in self.players:
            p.update(delta_time)
        for s in self.spriteList:
            s.update(delta_time)

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
        policy = None
        for pos in [(1, 1), (GRID_WIDTH-2, GRID_HEIGHT-2), (1, GRID_HEIGHT-2), (GRID_WIDTH-2, 1)]:
            p = Agent(self, policy)
            policy = p.policy
            #p = Player(self)
            p.setCenterPos(pos[0], pos[1])
            self.players.append(p)

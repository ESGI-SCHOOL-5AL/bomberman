import arcade

from . import objects
from .bomb import Bomb
from .bomb import Explosion


class Player(objects.Object):

    def __init__(self, environment):
        super().__init__(False, "player_front")
        self.environment = environment
        self.alive = True
        self.max_bombs = 1
        self.current_bombs = 0

    def updateCenterPos(self):
        self.center_x = self.width * self.x + self.width / 2
        self.center_y = self.width * self.y + self.width / 1.25

    def move(self, key, key_modifiers):
        if (key == arcade.key.Z or key == arcade.key.UP) and self.environment.grid[self.y+1][self.x].traversable:
            self.y += 1
        elif (key == arcade.key.Q or key == arcade.key.LEFT) and self.environment.grid[self.y][self.x-1].traversable:
            self.x -= 1
        elif (key == arcade.key.S or key == arcade.key.DOWN) and self.environment.grid[self.y-1][self.x].traversable:
            self.y -= 1
        elif (key == arcade.key.D or key == arcade.key.RIGHT) and self.environment.grid[self.y][self.x+1].traversable:
            self.x += 1
        elif key == arcade.key.SPACE and not isinstance(self.environment.grid[self.y][self.x], Bomb) and self.current_bombs < self.max_bombs:
            self.current_bombs += 1
            b = Bomb(self.environment, self)
            b.setCenterPos(self.x, self.y)
            self.environment.grid[self.y][self.x] = b

        if isinstance(self.environment.grid[self.y][self.x], Explosion):
            self.onDeath()
            self.environment.grid[self.y][self.x].owner.onKill(self)
        self.updateCenterPos()

    def reset(self):
        self.alive = True
        self.current_bombs = 0

    def onDeath(self):
        self.alive = False

    def onKill(self, player):
        pass

    def onDestroyBrick(self, brick):
        pass

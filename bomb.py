import objects

import arcade


class Bomb(objects.Object):

    def __init__(self, environment):
        super().__init__(False, "bomb_2")
        self.append_texture(arcade.load_texture("sprites/bomb_1.png"))
        self.append_texture(arcade.load_texture("sprites/bomb_0.png"))
        self.remaining = 3
        self.power = 3
        self.environment = environment

    def update(self, delta_time):
        self.remaining -= delta_time
        if self.remaining <= 0:
            self.destroyNear()
        else:
            self.set_texture(int(self.remaining))

    def destroyNear(self):
        self.destroyTowards(1)
        self.destroyTowards(-1)

    def destroyTowards(self, direction):
        for i in range(self.power):
            offset = i*direction
            if isinstance(self.environment.grid[self.y+offset][self.x], objects.Wall):
                break
            f = Explosion(self.environment)
            f.setCenterPos(self.x, self.y+offset)
            self.environment.grid[self.y+offset][self.x] = f
        for i in range(self.power):
            offset = i*direction
            if isinstance(self.environment.grid[self.y][self.x+offset], objects.Wall):
                break
            f = Explosion(self.environment)
            f.setCenterPos(self.x+offset, self.y)
            self.environment.grid[self.y][self.x+offset] = f


class Explosion(objects.Object):

    def __init__(self, environment):
        super().__init__(True, "explosion")
        self.remaining = 1
        self.environment = environment

    def setCenterPos(self, x, y):
        super().setCenterPos(x, y)
        newList = arcade.SpriteList()
        for p in self.environment.players:
            if not self.checkPlayerInside(p):
                newList.append(p)
        self.environment.players = newList

    def checkPlayerInside(self, player):
        if player.x == self.x and player.y == self.y:
            player.onDeath()
            return True
        return False

    def update(self, delta_time):
        self.remaining -= delta_time
        if self.remaining <= 0:
            f = objects.Floor()
            f.setCenterPos(self.x, self.y)
            self.environment.grid[self.y][self.x] = f

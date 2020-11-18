import arcade

from . import objects


class Bomb(objects.Object):

    def __init__(self, environment, owner):
        super().__init__(False, "bomb_2")
        self.append_texture(arcade.load_texture("sprites/bomb_1.png"))
        self.append_texture(arcade.load_texture("sprites/bomb_0.png"))
        self.remaining = 1  # TODO set back to 3
        self.power = 3
        self.environment = environment
        self.owner = owner

    def update(self, delta_time):
        self.remaining -= delta_time
        if self.remaining <= 0:
            self.owner.current_bombs -= 1
            self.destroyNear()
        else:
            self.set_texture(int(self.remaining))

    def destroyNear(self):
        self.destroyTowards(1)
        self.destroyTowards(-1)

    def destroyTowards(self, direction):
        for i in range(self.power):
            offset = i*direction
            obj = self.environment.grid[self.y+offset][self.x]
            if isinstance(obj, objects.Wall):
                break
            elif isinstance(obj, Bomb) and (obj.x != self.x or obj.y != self.y):
                obj.remaining = 0
                obj.destroyNear()
                break
            f = Explosion(self.environment, self.owner)
            f.setCenterPos(self.x, self.y+offset)

            if isinstance(obj, objects.Brick):
                self.owner.onDestroyBrick(obj)
            self.environment.grid[self.y+offset][self.x] = f
        for i in range(self.power):
            offset = i*direction
            obj = self.environment.grid[self.y][self.x+offset]
            if isinstance(obj, objects.Wall):
                break
            elif isinstance(obj, Bomb) and (obj.x != self.x or obj.y != self.y):
                obj.remaining = 0
                obj.destroyNear()
                break

            if isinstance(obj, objects.Brick):
                self.owner.onDestroyBrick(obj)
            f = Explosion(self.environment, self.owner)
            f.setCenterPos(self.x+offset, self.y)
            self.environment.grid[self.y][self.x+offset] = f


class Explosion(objects.Object):

    def __init__(self, environment, owner):
        super().__init__(True, "explosion")
        self.remaining = 1/3
        self.environment = environment
        self.owner = owner

    def setCenterPos(self, x, y):
        super().setCenterPos(x, y)
        # newList = arcade.SpriteList()
        for p in self.environment.players:
            self.checkPlayerInside(p)
            # if not self.checkPlayerInside(p):
            #     newList.append(p)
        # self.environment.players = newList

    def checkPlayerInside(self, player):
        if player.alive and player.x == self.x and player.y == self.y:
            player.onDeath()
            self.owner.onKill(player)
            return True
        return False

    def update(self, delta_time):
        self.remaining -= delta_time
        if self.remaining <= 0:
            f = objects.Floor()
            f.setCenterPos(self.x, self.y)
            self.environment.grid[self.y][self.x] = f

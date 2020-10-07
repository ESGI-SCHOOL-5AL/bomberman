import objects


class Bomb(objects.Object):

    def __init__(self, environment):
        super().__init__(False, "bomb_1")
        self.remaining = 3
        self.power = 3
        self.environment = environment

    def update(self, delta_time):
        self.remaining -= delta_time
        if self.remaining <= 0:
            self.destroyNear()

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

    def update(self, delta_time):
        self.remaining -= delta_time
        if self.remaining <= 0:
            f = objects.Floor()
            f.setCenterPos(self.x, self.y)
            self.environment.grid[self.y][self.x] = f

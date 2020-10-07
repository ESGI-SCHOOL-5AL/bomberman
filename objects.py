import arcade


class Object(arcade.Sprite):

    def __init__(self, traversable, sprite):
        super().__init__("sprites/" + sprite + ".png", 2)
        self.traversable = traversable
        self.sprite = sprite
        self.x = 0
        self.y = 0

    def setCenterPos(self, x, y):
        self.x = x
        self.y = y
        self.updateCenterPos()

    def updateCenterPos(self):
        self.center_x = self.width * self.x + self.width / 2
        self.center_y = self.height * self.y + self.height / 2

    def update(self, delta_time):
        pass


class Floor(Object):

    def __init__(self):
        super().__init__(True, "floor")


class Wall(Object):

    def __init__(self):
        super().__init__(False, "wall")


class Brick(Object):

    def __init__(self):
        super().__init__(False, "bricks")

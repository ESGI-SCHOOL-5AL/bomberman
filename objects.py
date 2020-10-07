import arcade


class Object(arcade.Sprite):

    def __init__(self, traversable, sprite):
        super().__init__("sprites/" + sprite + ".png")
        self.traversable = traversable
        self.sprite = sprite

    def setCenterPos(self, x, y):
        self.center_x = self.width * x + self.width / 2
        self.center_y = self.height * y + self.height / 2


class Floor(Object):

    def __init__(self):
        super().__init__(True, "floor")


class Wall(Object):

    def __init__(self):
        super().__init__(False, "wall")


class Brick(Object):

    def __init__(self):
        super().__init__(False, "brick")

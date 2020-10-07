class Object:

    def __init__(self, traversable, sprite):
        self.traversable = traversable
        self.sprite = sprite


class Floor(Object):

    def __init__(self):
        super().__init__(True, "F")


class Wall(Object):

    def __init__(self):
        super().__init__(False, "W")

    pass

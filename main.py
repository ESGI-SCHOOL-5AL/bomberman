import arcade
import environment

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Bomberman"


class BombermanGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.WHITE_SMOKE)

        # If you have sprite lists, you should create them here,
        # and set them to None

    def setup(self):
        self.env = environment.Environment()
        self.spriteList = self.env.toSpriteList()
        # Create your sprites and sprite lists here
        pass

    def on_draw(self):
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()
        self.spriteList.draw()

        # Call draw() on all your sprite lists below

    def on_update(self, delta_time):
        pass

    def on_key_press(self, key, key_modifiers):
        pass

    def on_key_release(self, key, key_modifiers):
        pass


def main():
    game = BombermanGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()

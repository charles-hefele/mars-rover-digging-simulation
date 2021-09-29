# Written by Charles Hefele
# April 2021

import arcade

# grid properties
ROWS = 4
COLS = 4
CELL_SIZE = 50
WIDTH = CELL_SIZE
HEIGHT = CELL_SIZE
MARGIN = 1

# screen properties
SCREEN_WIDTH = (CELL_SIZE + MARGIN) * COLS + MARGIN
SCREEN_HEIGHT = (CELL_SIZE + MARGIN) * ROWS + MARGIN
SCREEN_TITLE = 'Mars Rover Digging Simulation'


class GameView(arcade.View):

    def __init__(self, xray):
        super().__init__()

        # setup xray vision
        self.xray = xray

        # init grid
        self.grid = [[0 for i in range(4)] for j in range(4)]

        # init minerals
        self.minerals = [
            [0, 2, 3, 0],
            [0, 1, 1, 0],
            [1, 3, 0, 2],
            [0, 2, 0, 4],
        ]

        # init reward
        self.reward = 0

        # init vision
        self.vision = [[0 for i in range(4)] for j in range(4)]

        # game variables
        self.battery = 50
        self.mineral_count = 0

        # init player loc
        self.x = 3
        self.y = 0
        self.grid[self.x][self.y] = 1

        # sprites
        self.grid_sprite_list = arcade.SpriteList()
        for row in range(ROWS):
            for col in range(COLS):
                x = col * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
                sprite_square = arcade.SpriteSolidColor(WIDTH, HEIGHT, arcade.color.WHITE)
                sprite_square.center_x = x
                sprite_square.center_y = y
                self.grid_sprite_list.append(sprite_square)

    def update_sprites(self):
        for row in range(ROWS):
            for col in range(COLS):
                pos = row * COLS + col
                if self.grid[row][col] == 0:
                    self.grid_sprite_list[pos].color = arcade.color.WINE
                else:
                    self.grid_sprite_list[pos].color = arcade.color.GRAY

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.update_sprites()

    def on_update(self, delta_time):
        if self.battery == 0:
            game_over_view = GameOverView(self.mineral_count)
            self.window.show_view(game_over_view)

    def on_draw(self):
        arcade.start_render()

        # draw sprites
        self.grid_sprite_list.draw()

        # draw static text
        font_size = 10
        output_battery = f'Battery: {self.battery}'
        arcade.draw_text(output_battery, 0, 30, arcade.color.WHITE, font_size)

        output_minerals = f'Minerals: {self.mineral_count}'
        arcade.draw_text(output_minerals, 0, 15, arcade.color.WHITE, font_size)

        output_reward = f'Reward: {self.reward}'
        arcade.draw_text(output_reward, 0, 0, arcade.color.WHITE, font_size)

        # draw grid numbers
        for row in range(ROWS):
            for col in range(COLS):
                x = col * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
                # xray vision mode
                if self.xray:
                    val = self.minerals[row][col]
                    if val != 0:
                        arcade.draw_text(str(val), x, y, arcade.color.WHITE, font_size=30, anchor_x='center', anchor_y='center')
                # blind mode
                else:
                    if self.vision[row][col] == 1:
                        arcade.draw_text(str(self.minerals[row][col]), x, y, arcade.color.WHITE, font_size=30, anchor_x='center', anchor_y='center')

    def on_key_press(self, key, key_modifiers):

        if key == arcade.key.UP:
            self.battery -= 1
            self.reward += -1
            if self.x < ROWS - 1:
                self.grid[self.x][self.y] = 0
                self.x += 1
                self.grid[self.x][self.y] = 1
            print('action: up', '\t\tloc: ', self.x, self.y, '\tbattery: ', self.battery, '\tminerals: ', self.mineral_count)

        if key == arcade.key.DOWN:
            self.battery -= 1
            self.reward += -1
            if self.x > 0:
                self.grid[self.x][self.y] = 0
                self.x -= 1
                self.grid[self.x][self.y] = 1
            print('action: down', '\tloc: ', self.x, self.y, '\tbattery: ', self.battery,  '\tminerals: ', self.mineral_count)

        if key == arcade.key.LEFT:
            self.battery -= 1
            self.reward += -1
            if self.y > 0:
                self.grid[self.x][self.y] = 0
                self.y -= 1
                self.grid[self.x][self.y] = 1
            print('action: left', '\tloc: ', self.x, self.y, '\tbattery: ', self.battery,  '\tminerals: ', self.mineral_count)

        if key == arcade.key.RIGHT:
            self.battery -= 1
            self.reward += -1
            if self.y < COLS - 1:
                self.grid[self.x][self.y] = 0
                self.y += 1
                self.grid[self.x][self.y] = 1
            print('action: right', '\tloc: ', self.x, self.y, '\tbattery: ', self.battery,  '\tminerals: ', self.mineral_count)

        if key == arcade.key.D:
            self.battery -= 1
            if self.minerals[self.x][self.y] > 0:
                self.minerals[self.x][self.y] -= 1
                self.mineral_count += 1
                self.reward += 1
            else:
                self.reward += -1
            print('action: dig', '\tloc: ', self.x, self.y, '\tbattery: ', self.battery,  '\tminerals: ', self.mineral_count, '\t\tminerals in current loc: ', self.minerals[self.x][self.y])

        if key == arcade.key.S:
            self.battery -= 1
            self.vision[self.x][self.y] = 1
            # up
            if self.x + 1 < ROWS:
                self.vision[self.x + 1][self.y] = 1
            # down
            if self.x - 1 >= 0:
                self.vision[self.x - 1][self.y] = 1
            # right
            if self.y + 1 < COLS:
                self.vision[self.x][self.y + 1] = 1
            # left
            if self.y - 1 >= 0:
                self.vision[self.x][self.y - 1] = 1
            print('action: scan', '\tloc: ', self.x, self.y, '\tbattery: ', self.battery,  '\tminerals: ', self.mineral_count, '\t\tminerals left: ', self.mineral_count[self.x][self.y])

        if key == arcade.key.H:
            self.xray = not self.xray

        # update the sprite list
        self.update_sprites()


class GameOverView(arcade.View):
    def __init__(self, mineral_count):
        super().__init__()
        self.mineral_count = mineral_count

    def on_show(self):
        arcade.set_background_color(arcade.color.WINE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text('Battery empty!', SCREEN_WIDTH/2, SCREEN_HEIGHT-200, arcade.color.WHITE, font_size=40, anchor_x='center')
        arcade.draw_text('Press "enter" to recharge', SCREEN_WIDTH/2, SCREEN_HEIGHT-250, arcade.color.WHITE, font_size=24, anchor_x='center')
        arcade.draw_text(f'Minerals found: {self.mineral_count}', SCREEN_WIDTH / 2, SCREEN_HEIGHT - 300, arcade.color.WHITE, font_size=24, anchor_x='center')

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.ENTER:
            game_view = GameView(xray=True)
            self.window.show_view(game_view)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game_view = GameView(xray=True)
    window.show_view(game_view)
    arcade.run()


if __name__ == '__main__':
    main()
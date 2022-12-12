import arcade
import random
import os

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 450
GAME_INTRO = 1
GAME_RUNNING = 2
GAME_OVER = 3
MOVEMENT_SPEED = 5


class Puck(arcade.Sprite):

    # def __init__(self, image, scale):
    #     super().__init__(image, scale)
    # self.image = image
    # self.scale = scale

    def update(self):
        if self.left <= 0 or self.right >= SCREEN_WIDTH:
            self.change_x *= -1
        elif self.bottom <= 0 or self.top >= SCREEN_HEIGHT:
            self.change_y *= -1

    def puck_boundary(self):
        if self.left <= 16 or self.right >= 686:
            self.center_x *= -1
        elif self.bottom <= 20 or self.top >= 400:
            self.center_y *= -1

        self.center_x += self.change_x
        super(Puck, self).update()


class PlayerStriker(arcade.Sprite):

    def player_striker_boundary(self):
        if self.bottom <= 30:
            self.center_y += 10
        elif self.top >= 400:
            self.center_y -= 10


class ComputerStriker(arcade.Sprite):

    def computer_striker_boundary(self):
        if self.bottom <= 30:
            # self.center_y += 10
            self.change_y *= -1
        elif self.top >= 400:
            # self.center_y -= 10
            self.change_y *= -1

        print(self.change_y)


class InstructionView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Welcome to Air Hockey", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 75,
                         arcade.color.RED_DEVIL, font_size=50, anchor_x="center")
        arcade.draw_text("Score seven times to win", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.RED_DEVIL, font_size=30, anchor_x="center")
        arcade.draw_text("Click to start the game", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 75,
                         arcade.color.RED_DEVIL, font_size=30, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = Game()
        game_view.setup()
        self.window.show_view(game_view)
        self.window.set_mouse_visible(False)


class Game(arcade.View):

    def __init__(self):
        super().__init__()
        self.background = None
        self.current_state = None

        self.MOVEMENT_SPEED = 4

        self.all_sprites_list = []
        self.all_striker_list = []
        self.puck = None
        self.player_striker = None
        self.computer_striker = None
        self.goal_line = None
        self.goal_line_2 = None

        self.score = 0
        self.enemy_score = 0
        self.score_text = None

    def setup(self):

        self.background = arcade.load_texture("air_hockey_arena.jpg")
        self.all_sprites_list = arcade.SpriteList()
        self.all_striker_list = arcade.SpriteList()
        self.puck_list = arcade.SpriteList()
        self.current_state = GAME_RUNNING

        self.score = 0
        self.enemy_score = 0
        self.current_state = GAME_INTRO

        self.player_striker = arcade.Sprite("green_striker.jpg", .07)
        self.all_striker_list.append(self.player_striker)

        self.computer_striker = arcade.Sprite("red_striker.jpg", .07)
        self.computer_striker.change_y = 1
        self.all_striker_list.append(self.computer_striker)

        self.puck = Puck("puck.jpg", .15)
        self.bounce_frame = 35

        self.goal_line = arcade.Sprite("goal_line.jpg", .3)
        self.all_sprites_list.append(self.goal_line)
        self.goal_line_2 = arcade.Sprite("goal_line_2.jpg", .3)
        self.all_sprites_list.append(self.goal_line_2)

        self.puck.center_x = SCREEN_WIDTH // 2
        self.puck.center_y = 210
        self.all_sprites_list.append(self.puck)
        self.puck_list.append(self.puck)
        self.puck.change_x = -1
        # self.puck.change_y = 1

        self.player_striker.center_x = 170
        self.player_striker.center_y = 208
        self.computer_striker.center_x = 530
        self.computer_striker.center_y = 208
        self.computer_striker.change_y = 1

        self.goal_line.center_x = 16
        self.goal_line.center_y = 208
        self.goal_line_2.center_x = 686
        self.goal_line_2.center_y = 208

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        # if self.current_state == GAME_INTRO:
        #     arcade.draw_text("Welcome to air hockey", SCREEN_WIDTH // 4.8, SCREEN_HEIGHT // 2 + 30, arcade.color.BLACK
        #                      ,25)
        #     arcade.draw_text("Score seven times to win", SCREEN_WIDTH // 4.8, SCREEN_HEIGHT // 2, arcade.color.BLACK,
        #                      25)
        #     arcade.draw_text("Press the space bar to continue.", SCREEN_WIDTH // 4.8, (SCREEN_HEIGHT // 2 - 30),
        #                      arcade.color.BLACK, 25)

        # elif self.current_state == GAME_RUNNING:
        #     self.draw_game()

        # else:
        #     self.draw_game_over()

        self.draw_game()

    def draw_game(self):
        self.player_striker.draw()
        self.computer_striker.draw()
        self.puck.draw()
        self.goal_line.draw()
        self.goal_line_2.draw()

        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 425, arcade.color.BLACK, 15)
        output = f"Score: {self.enemy_score}"
        arcade.draw_text(output, 610, 425, arcade.color.BLACK, 15)

    def draw_game_over(self):
        output = "Game Over"
        arcade.draw_text(output, 240, 225, arcade.color.BLACK, 50)

    def update(self, delta_time):
        self.puck_list.update()
        self.computer_striker.update()
        self.player_striker.update()

        hit_list = arcade.check_for_collision_with_list(self.player_striker, self.puck_list)
        for puck in hit_list:
            if self.bounce_frame == 35:
                puck.change_x *= -1 * random.uniform(0.8, 1.2)
                puck.change_y *= -1 * random.uniform(0.8, 1.2)
                self.bounce_frame -= 1
            elif self.bounce_frame == 0:
                self.bounce_frame = 35
            else:
                self.bounce_frame -= 1
            # print("hello")

        hit_list = arcade.check_for_collision_with_list(self.computer_striker, self.puck_list)
        for puck in hit_list:
            puck.change_x *= -1
            puck.change_y *= -1

        hit_list = arcade.check_for_collision_with_list(self.goal_line, self.puck_list)
        for puck in hit_list:
            puck.center_x = SCREEN_WIDTH // 2
            puck.center_y = 210
            puck.change_x = -1

            self.player_striker.center_x = 170
            self.player_striker.center_y = 208
            self.computer_striker.center_x = 530
            self.computer_striker.center_y = 208

            self.enemy_score += 1

            if self.enemy_score == 4:
                self.MOVEMENT_SPEED += .06
                self.computer_striker.change_y *= 2
                print("hi", self.computer_striker.change_y)


        hit_list = arcade.check_for_collision_with_list(self.goal_line_2, self.puck_list)
        for puck in hit_list:
            puck.center_x = SCREEN_WIDTH // 2
            puck.center_y = 210
            puck.change_x = -1

            self.player_striker.center_x = 170
            self.player_striker.center_y = 208
            self.computer_striker.center_x = 530
            self.computer_striker.center_y = 208

            self.score += 1

            if self.score == 4:
                self.MOVEMENT_SPEED += .06
                self.computer_striker.change_y *= 2
                print("hi")

        PlayerStriker.player_striker_boundary(self.player_striker)
        ComputerStriker.computer_striker_boundary(self.computer_striker)
        Puck.puck_boundary(self.puck)
        super().update(delta_time)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.player_striker.change_y = self.MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_striker.change_y = -self.MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_striker.change_y = 0


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Different Views Example")
    menu_view = InstructionView()
    window.show_view(menu_view)
    arcade.run()


main()

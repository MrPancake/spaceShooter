import arcade
from random import randrange
import tkinter

root = tkinter.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
screen_title = "shooter"

player_scale = 0.8
enemy_chance = 10000


class Player(arcade.Sprite):

    def __init__(self):
        super().__init__()

        self.textures = []
        texture_up = arcade.load_texture("playerShip1_green.png")
        self.textures.append(texture_up)

        self.set_texture(0)

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > screen_height - 1:
            self.top = screen_height - 1

        if self.left < 0:
            self.left = 0
        elif self.right > screen_width - 1:
            self.right = screen_width - 1

        if self.change_x > 0 and self.change_y > 0:
            self.angle = 315
        elif self.change_x > 0 and self.change_y < 0:
            self.angle = 225
        elif self.change_x < 0 and self.change_y < 0:
            self.angle = 135
        elif self.change_x < 0 and self.change_y > 0:
            self.angle = 45
        elif self.change_x == 0 and self.change_y < 0:
            self.angle = 180
        elif self.change_x > 0 and self.change_y == 0:
            self.angle = 270
        elif self.change_x < 0 and self.change_y == 0:
            self.angle = 90
        else:
            self.angle = 0


class MyShooter(arcade.Window):
    def __init__(self):
        super().__init__(screen_width, screen_height, screen_title, True)

        arcade.set_background_color(arcade.color.NAVY_BLUE)

        self.movement_speed_player = 5

        self.sprite_list_player = arcade.SpriteList()

        self.sprite_player = Player()
        self.sprite_player.center_y = screen_height // 2
        self.sprite_player.center_x = screen_width // 2
        self.sprite_list_player.append(self.sprite_player)

        self.sprite_list_enemy = arcade.SpriteList()

        self.sprite_list_bullets = arcade.SpriteList()
        self.enemy_chance = enemy_chance

        self.player_position_shooting_list = [(screen_width // 2, screen_height // 2)]

        self.set_mouse_visible(False)

        self.score = 0
        self.time = 0
        self.time_2 = 0
        self.game_over = False

        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False

        self.w_pressed = False
        self.s_pressed = False
        self.d_pressed = False
        self.a_pressed = False

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            exit()

        if symbol == arcade.key.W:
            self.w_pressed = True
        if symbol == arcade.key.S:
            self.s_pressed = True
        if symbol == arcade.key.D:
            self.d_pressed = True
        if symbol == arcade.key.A:
            self.a_pressed = True

        if symbol == arcade.key.UP:
            self.up_pressed = True
        if symbol == arcade.key.DOWN:
            self.down_pressed = True
        if symbol == arcade.key.RIGHT:
            self.right_pressed = True
        if symbol == arcade.key.LEFT:
            self.left_pressed = True

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.W:
            self.w_pressed = False
        if symbol == arcade.key.S:
            self.s_pressed = False
        if symbol == arcade.key.D:
            self.d_pressed = False
        if symbol == arcade.key.A:
            self.a_pressed = False

        if symbol == arcade.key.UP:
            self.up_pressed = False
        if symbol == arcade.key.DOWN:
            self.down_pressed = False
        if symbol == arcade.key.RIGHT:
            self.right_pressed = False
        if symbol == arcade.key.LEFT:
            self.left_pressed = False

    def on_draw(self):
        arcade.start_render()
        self.sprite_list_player.draw()
        self.sprite_list_enemy.draw()
        self.sprite_list_bullets.draw()
        arcade.draw_text(f"Your Score: {self.score}", 50, 50, arcade.color.YELLOW, 15,
                         align="center")
        arcade.draw_text(f"Your Time: {round(self.time, 3)}", 50, 30, arcade.color.YELLOW, 15,
                         align="center")

        if self.game_over:
            arcade.draw_text(f"Your Score: {self.score}.\n"
                             f"Your Time: {round(self.time, 3)}\n"
                             f"Press ESC to close.",
                             660, 540, arcade.color.YELLOW, 40, 600, "center")
            return

    def on_update(self, delta_time: float):
        if self.game_over:
            return

        self.time += 1 / 60
        self.time_2 += 1

        self.sprite_list_player.update()
        self.sprite_list_enemy.update()
        self.sprite_list_bullets.update()

        self.sprite_player.change_x = 0
        self.sprite_player.change_y = 0

        if self.a_pressed and not self.d_pressed and self.sprite_player.center_x >= 0 + 50 * player_scale:
            self.sprite_player.change_x = - self.movement_speed_player
        elif not self.a_pressed and self.d_pressed and self.sprite_player.center_x <= screen_width - 50 * player_scale:
            self.sprite_player.change_x = self.movement_speed_player

        if self.w_pressed and not self.s_pressed and self.sprite_player.center_y <= screen_height - 30 * player_scale:
            self.sprite_player.change_y = self.movement_speed_player
        elif not self.w_pressed and self.s_pressed and self.sprite_player.center_y >= 0 + 70 * player_scale:
            self.sprite_player.change_y = - self.movement_speed_player

        if self.time_2 >= 10:

            bullet_sprite = arcade.Sprite("laserRed01.png")
            bullet_sprite.center_x = self.player_position_shooting_list[-1][0]
            bullet_sprite.center_y = self.player_position_shooting_list[-1][1]
            self.player_position_shooting_list.append((self.sprite_player.center_x + self.sprite_player.change_x*10,
                                                       self.sprite_player.center_y + self.sprite_player.change_y*10))

            if self.up_pressed and not self.down_pressed and not self.left_pressed and not self.right_pressed:
                bullet_sprite.change_y = 20
                bullet_sprite.angle = 0
                self.sprite_list_bullets.append(bullet_sprite)

            elif self.down_pressed and not self.up_pressed and not self.left_pressed and not self.right_pressed:
                bullet_sprite.change_y = -20
                bullet_sprite.angle = 180
                self.sprite_list_bullets.append(bullet_sprite)

            elif self.right_pressed and not self.left_pressed and not self.up_pressed and not self.down_pressed:
                bullet_sprite.change_x = 20
                bullet_sprite.angle = 270
                self.sprite_list_bullets.append(bullet_sprite)

            elif self.left_pressed and not self.right_pressed and not self.up_pressed and not self.down_pressed:
                bullet_sprite.change_x = -20
                bullet_sprite.angle = 90
                self.sprite_list_bullets.append(bullet_sprite)

            elif self.left_pressed and not self.right_pressed and self.up_pressed and not self.down_pressed:
                bullet_sprite.change_x = -20
                bullet_sprite.change_y = 20
                bullet_sprite.angle = 45
                self.sprite_list_bullets.append(bullet_sprite)

            elif self.left_pressed and not self.right_pressed and not self.up_pressed and self.down_pressed:
                bullet_sprite.change_x = -20
                bullet_sprite.change_y = -20
                bullet_sprite.angle = 135
                self.sprite_list_bullets.append(bullet_sprite)

            elif not self.left_pressed and self.right_pressed and self.up_pressed and not self.down_pressed:
                bullet_sprite.change_x = 20
                bullet_sprite.change_y = 20
                bullet_sprite.angle = 315
                self.sprite_list_bullets.append(bullet_sprite)

            elif not self.left_pressed and self.right_pressed and not self.up_pressed and self.down_pressed:
                bullet_sprite.change_x = 20
                bullet_sprite.change_y = -20
                bullet_sprite.angle = 225
                self.sprite_list_bullets.append(bullet_sprite)

            self.time_2 -= 10

        self.enemy_chance += (self.time/60)
        x = randrange(round(self.enemy_chance))
        if x > 9900:
            k = 1
            while k == 1:
                enemy = arcade.Sprite("saw.png", scale=0.5,
                                      center_x=randrange(screen_width),
                                      center_y=randrange(screen_height))
                if abs(enemy.center_x - self.sprite_player.center_x) > 175\
                        or abs(enemy.center_y - self.sprite_player.center_y) > 175:
                    self.sprite_list_enemy.append(enemy)
                    k -= 1

        for i in self.sprite_list_enemy:
            if i.center_x > self.sprite_player.center_x:
                i.change_x = -1
            elif i.center_x < self.sprite_player.center_x:
                i.change_x = 1
            else:
                i.change_x = 0

            if i.center_y > self.sprite_player.center_y:
                i.change_y = -1
            elif i.center_y < self.sprite_player.center_y:
                i.change_y = 1
            else:
                i.change_y = 0

        for i in self.sprite_list_bullets:
            if (i.center_y > screen_height + 50 or i.center_y < -50 or i.center_x > screen_width + 50
                    or i.center_x < -50):
                i.remove_from_sprite_lists()

            bullet_hit_list = arcade.check_for_collision_with_list(i, self.sprite_list_enemy)
            if bullet_hit_list:
                i.remove_from_sprite_lists()
                for k in bullet_hit_list:
                    self.score += 1
                    k.remove_from_sprite_lists()

        player_hit_list = arcade.check_for_collision_with_list(self.sprite_player, self.sprite_list_enemy)
        if player_hit_list != []:
            self.game_over = True


def main():
    MyShooter()
    arcade.run()


if __name__ == "__main__":
    main()

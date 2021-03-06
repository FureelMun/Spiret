# Импортирование библиотек
from pygame import *
from random import randint
from time import sleep


# Класс спрайтов
class GameSprite(sprite.Sprite):
    def __init__(self, player_x, player_y, player_image, player_speed, player_size_x, player_size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_size_x, player_size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# Класс игрока
class Player(GameSprite):

    def update(self):
        global maze_playing, coins_you_have, coins_counter, maze_2_playing, \
            flag_playing, bullets
        pressed_key = key.get_pressed()
        if flag_playing:
            if (pressed_key[K_UP] or pressed_key[K_w]) and self.rect.y > 5:  # движение вверх
                self.rect.y -= self.speed
            elif (pressed_key[K_DOWN] or pressed_key[K_s]) and self.rect.y < 420:  # движение вниз
                self.rect.y += self.speed
            if (pressed_key[K_RIGHT] or pressed_key[K_d]) and self.rect.x < 450:  # движение вправо
                self.rect.x += self.speed
            elif (pressed_key[K_LEFT] or pressed_key[K_a]) and self.rect.x > 10:  # движение влево
                self.rect.x -= self.speed

        elif maze_playing:
            if (pressed_key[K_RIGHT] or pressed_key[K_d]) and not (sprite.collide_rect(hero, wall_1)
                                                                   or sprite.collide_rect(hero, wall_2)
                                                                   or sprite.collide_rect(hero, wall_3)
                                                                   or sprite.collide_rect(hero, wall_4)
                                                                   or sprite.collide_rect(hero, wall_5)) \
                    and self.rect.x < 630:
                self.rect.x += self.speed
            if (pressed_key[K_LEFT] or pressed_key[K_a]) and self.rect.x > 10 \
                    and not (sprite.collide_rect(hero, wall_1) or sprite.collide_rect(hero, wall_2)
                             or sprite.collide_rect(hero, wall_3)):  # движение влево
                self.rect.x -= self.speed
            elif (pressed_key[K_UP] or pressed_key[K_w]) and self.rect.y > 5 \
                    and not (sprite.collide_rect(hero, wall_1) or sprite.collide_rect(hero, wall_2)
                             or sprite.collide_rect(hero, wall_3)):  # движение вверх
                self.rect.y -= self.speed
            elif (pressed_key[K_DOWN] or pressed_key[K_s]) and self.rect.y < 420 \
                    and not (sprite.collide_rect(hero, wall_1) or sprite.collide_rect(hero, wall_2)
                             or sprite.collide_rect(hero, wall_3)):  # движение вниз
                self.rect.y += self.speed
            if sprite.collide_rect(hero, wall_1) or sprite.collide_rect(hero, wall_2) \
                    or sprite.collide_rect(hero, wall_3) or \
                    sprite.collide_rect(hero, wall_4) or \
                    sprite.collide_rect(hero, wall_5):
                self.rect.y = 400
                self.rect.x = 20
                coins_you_have -= 5
                update_coin()
            if sprite.collide_rect(self, coin_maze):
                win()
        elif maze_2_playing:
            if (pressed_key[K_RIGHT] or pressed_key[K_d]) and not (sprite.collide_rect(hero, wall_2_1)
                                                                   or sprite.collide_rect(hero, wall_2_2)
                                                                   or sprite.collide_rect(hero, wall_2_3)
                                                                   or sprite.collide_rect(hero, wall_2_4)
                                                                   or sprite.collide_rect(hero, wall_2_5)) \
                    and self.rect.x < 630:
                self.rect.x += self.speed
            elif (pressed_key[K_LEFT] or pressed_key[K_a]) and self.rect.x > 10 \
                    and not (sprite.collide_rect(hero, wall_2_1) or sprite.collide_rect(hero, wall_2_2)
                             or sprite.collide_rect(hero, wall_2_3)):  # движение влево
                self.rect.x -= self.speed
            elif (pressed_key[K_UP] or pressed_key[K_w]) and self.rect.y > 5 \
                    and not (sprite.collide_rect(hero, wall_2_1) or sprite.collide_rect(hero, wall_2_2)
                             or sprite.collide_rect(hero, wall_2_3)):  # движение вверх
                self.rect.y -= self.speed
            elif (pressed_key[K_DOWN] or pressed_key[K_s]) and self.rect.y < 420 \
                    and not (sprite.collide_rect(hero, wall_2_1) or sprite.collide_rect(hero, wall_2)
                             or sprite.collide_rect(hero, wall_2_3)):  # движение вниз
                self.rect.y += self.speed
            if sprite.collide_rect(hero, wall_2_1) or sprite.collide_rect(hero, wall_2_2) \
                    or sprite.collide_rect(hero, wall_2_3) or \
                    sprite.collide_rect(hero, wall_2_4) or \
                    sprite.collide_rect(hero, wall_2_5):
                self.rect.y = 400
                self.rect.x = 20
                coins_you_have -= 5
                update_coin()
            if sprite.collide_rect(self, coin_maze):
                win()
        elif brick_game_playing:
            if (pressed_key[K_LEFT] or pressed_key[K_a]) and self.rect.x > 10:  # движение влево
                self.rect.x -= self.speed
            elif (pressed_key[K_RIGHT] or pressed_key[K_d]) and self.rect.x < 550:  # движение вправо
                self.rect.x += self.speed
            if pressed_key[K_SPACE]:
                bullet = Bullet(self.rect.centerx, self.rect.top, "bullet.png", 5, 10, 10)
                bullets.add(bullet)
                fire_effect.play()

        elif banana_playing:
            if (pressed_key[K_LEFT] or pressed_key[K_a]) and self.rect.x > 10:  # движение влево
                self.rect.x -= self.speed
            elif (pressed_key[K_RIGHT] or pressed_key[K_d]) and self.rect.x < 550:  # движение вправо
                self.rect.x += self.speed

    def physics(self):
        global flag_playing, brick_game_playing
        if flag_playing:
            if not (sprite.collide_rect(hero, island_1)
                    or sprite.collide_rect(hero, island_2)
                    or sprite.collide_rect(hero, island_3)):
                self.rect.y += 2
        elif brick_game_playing:
            self.rect.y += 2

    def lose_flore(self):
        global lose
        if self.rect.y > 440:
            lose = True
            loosing()


# Класс остравов в 1-ой игре
class Islands(GameSprite):
    def update(self):
        pressed_key = key.get_pressed()
        if pressed_key[K_LEFT] or pressed_key[K_a]:  # движение влево
            self.rect.x += (self.speed / 2)
        if pressed_key[K_RIGHT] or pressed_key[K_d]:  # движение вправо
            self.rect.x -= self.speed

    def shift(self):
        if self.rect.x < 0:
            self.rect.y = randint(70, 430)
            self.rect.x = wind_size[0]


# Класс монстров в 1-ой игре
class Monsters(GameSprite):
    def update(self):
        pressed_key = key.get_pressed()
        if pressed_key[K_LEFT] or pressed_key[K_a]:  # движение влево
            self.rect.x += self.speed / 2
        self.rect.x -= self.speed / 4
        if (pressed_key[K_UP] or pressed_key[K_w]) and self.rect.y > 5:  # движение вверх
            self.rect.y -= self.speed / 4
        elif pressed_key[K_DOWN] or pressed_key[K_s]:  # движение вниз
            self.rect.y += self.speed / 2

    def shift(self):
        if self.rect.x < 10 or self.rect.y < 10 or self.rect.y > 490:
            self.rect.y = randint(70, 430)
            self.rect.x = wind_size[0]


# Класс койнов
class Coins(GameSprite):

    def update(self):
        pressed_key = key.get_pressed()
        if pressed_key[K_LEFT] or pressed_key[K_a]:  # движение влево
            self.rect.x += self.speed
        self.rect.x -= self.speed / 2

    def shift(self):
        if self.rect.x < 0:
            self.rect.y = randint(70, 430)
            self.rect.x = wind_size[0]

    def touching(self):
        global coins_state
        if sprite.collide_rect(hero, self):
            self.rect.y = randint(70, 430)
            self.rect.x = wind_size[0]
            award_sound.play()
            coins_state = True


# Класс стен в лаберинтах
class Wall(sprite.Sprite):
    def __init__(self, color_red, color_green, color_blue, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_red = color_red
        self.color_green = color_green
        self.color_blue = color_blue

        self.wall_x = wall_x
        self.wall_y = wall_y

        self.width = wall_width
        self.height = wall_height

        self.image = Surface((self.width, self.height))
        self.image.fill((color_red, color_green, color_blue))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def update(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# Класс ложныхбананов в "Летит банан"
class Bananas(GameSprite):
    def update(self):
        global coins_you_have, coins_counter, background_state, flag_start_sprite, lose, banana, banana_playing
        self.rect.y += self.speed
        coins_counter_sprite.reset()
        if sprite.collide_rect(basket, self):
            coins_you_have += 5
            award_sound.play()
            update_coin()
            self.rect.y = 0
            self.rect.x = randint(100, 600)
        elif self.rect.y >= 490:
            coins_you_have -= 10
            update_coin()
            lose = True
            background_state = "start"
            self.rect.y = 0
            loosing()
            if lose:
                self.rect.y = 0
                flag_start_sprite = True
                touch_a_monster.play()
                lose = False
                banana = 0
                banana_playing = False


# Класс бананов в "Летит банан"
class False_banana(GameSprite):
    def update(self):
        global coins_you_have, coins_counter, background_state, flag_start_sprite, lose, banana, banana_playing
        self.rect.y += self.speed
        if self.rect.y >= 490:
            coins_you_have += 5
            award_sound.play()
            update_coin()
            self.rect.y = 0
            self.rect.x = randint(100, 600)
        elif sprite.collide_rect(basket, self):
            coins_you_have -= 10
            update_coin()
            lose = True
            background_state = "start"
            self.rect.y = 0
            if lose:
                self.rect.y = 0
                banana_1.rect.y = 0
                banana_2.rect.y = 0
                banana_3.rect.y = 0
                flag_start_sprite = True
                touch_a_monster.play()
                lose = False
                banana = 0
                banana_playing = False
            background_state = "start"


# Класс кнопок в лобби
class Buttons(GameSprite):
    def update(self):
        global button_status, button_brick_game_y, button_maze_y_2, buttons_banana_y, buttons_maze_y
        if button_status == 5 and not button_flight.rect.y == 20:
            self.rect.y += 5
            maze_1_look.rect.y = button_maze.rect.y
            banana_look.rect.y = button_banana.rect.y
            maze_2_look.rect.y = button_maze_2.rect.y
            bricks_look.rect.y = button_brick_game.rect.y
        elif button_status == 4 and not button_brick_game.rect.y == 20:
            self.rect.y -= 5
            maze_1_look.rect.y = button_maze.rect.y
            banana_look.rect.y = button_banana.rect.y
            maze_2_look.rect.y = button_maze_2.rect.y
            bricks_look.rect.y = button_brick_game.rect.y
        if button_flight.rect.y == 20:
            button_maze.rect.y = 180
            button_banana.rect.y = 340
            button_maze_2.rect.y = 500
            button_brick_game.rect.y = 660
            maze_1_look.rect.y = 180
            maze_2_look.rect.y = 340
            banana_look.rect.y = 500
            bricks_look.rect.y = 600


# Класс пуль в "Разбей керпич"
class Bullet(GameSprite):
    def update(self):
        global lose, num_bricks
        self.rect.y -= self.speed
        if self.rect.y == 0:
            self.kill()
            lose = True
        if sprite.spritecollide(self, bricks, True):
            self.kill()
            num_bricks -= 1
            print(num_bricks)


# FPS
clock = time.Clock()
FPS = 60

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# size
wind_size = (700, 500)
half_wind_size = (wind_size[0] / 2, wind_size[1] / 2)
wall_2_size_1 = (20, 400)
island_size = (170, 30)
monsters_size = (100, 50)
buttons_size = (300, 150)
brick_size = (140, 50)
basket_size = (140, 70)
bananas_size = (70, 50)

coin_size = 50
info_button_size = 50
start_sprite_size = 128
hero_size = 70

# x
coins_counter_sprite_x = 555
buttons_x = 200
info_button_x = 20
banana_1_x = 20
banana_2_x = 250
banana_3_x = 400
brick_x_list = [50, 325, 550]
brick_x = 0

# location
start_sprite_place = (wind_size[0] / 2.5, wind_size[1] / 2.5)
coin_1_place = (580, 90)
coin_2_place = (640, 400)
coin_3_place = (500, 225)
monster_1_place = (140, 50)
monster_2_place = (240, 250)
monster_3_place = (440, 150)
island_1_place = (490, 50)
island_2_place = (0, half_wind_size[1])
island_3_place = (400, 200)
wall_place_1 = (100, 100)
wall_size_1 = (20, 400)
wall_place_2 = (220, 0)
wall_place_3 = (340, 100)
wall_place_4 = (460, 0)
wall_place_5 = (580, 100)
font_place = (610, 10)
basket_place = (half_wind_size[0], 400)
hero_place = (10, half_wind_size[1] - 40)
wall_2_place_1 = (100, 0)
wall_2_place_2 = (220, 100)
wall_2_place_3 = (340, 0)
wall_2_place_4 = (460, 100)
wall_2_place_5 = (580, 0)

# y
coins_counter_sprite_y = 10
buttons_flight_y = 20
buttons_maze_y = 180
info_button_y = 20
buttons_banana_y = 340
bananas_y = 0
button_maze_y_2 = 500
button_brick_game_y = 660
brick_y = 0

# speed
island_1_speed = 4
island_2_speed = 6
island_3_speed = 8
hero_speed = 10
monster_1_speed = 8
monster_2_speed = 10
monster_3_speed = 6
coin_1_speed = 10
coin_2_speed = 6
coin_3_speed = 8
start_sprite_speed = 1
coins_counter_speed = 0
buttons_speed = 0
basket_speed = 10
bananas_speed = 2

# Счетчик
font_size = 50
coins_you_have = 0
maze = 0
button_status = 0
banana = 0
maze_2 = 0
brick_game = 0
num_bricks = 25

font.init()
font = font.SysFont("Arial", font_size)

# image
hero_image = "hero.png"
monsters_image = "monster.png"
coins_image = "coins.png"
start_sprite_image = "Button.png"
basket_image = "basket.png"
button_flight_image = "flight_button.png"
button_maze_image = "maze_game.png"
info_button_image = "info.png"
mouse_image = "mouse.png"
instruction_image = "instruction.png"
button_banana_image = "banana_button.png"
bananas_image = "banana.png"
false_bananas_image = "monster.png"
button_maze_image_2 = "maze_2_button.png"
button_brick_game_image = "brick_game_button.png"
brick_image = "brick.png"
looks_image = "look.png"

islands_image = "island.jpg"
icon = image.load('background.jpg')
background_image = "background.jpg"
start_lobe_image = "choose_game.jpg"
choose_lobe_image = "start_lobe.jpg"
maze_background = "maze_image.jpg"
banana_image = "banana.jpg"
brick_game_image = "brick_game_background.jpg"

# музыка
mixer.init()
gaming_music_1 = 'jungles.ogg'
gaming_music_2 = 'start_music.ogg'
gaming_music = gaming_music_2
mixer.music.load(gaming_music)
mixer.music.play()
# звуки/эффекты
transition = mixer.Sound('transition.ogg')
touch_a_monster = mixer.Sound('failure.ogg')
award_sound = mixer.Sound('award.ogg')
win_sound = mixer.Sound('win.ogg')
fire_effect = mixer.Sound("shot.ogg")
# Громкость
volume_sounds = 0.5
mixer.music.set_volume(volume_sounds)
transition.set_volume(volume_sounds)
touch_a_monster.set_volume(volume_sounds)
award_sound.set_volume(volume_sounds)

# Названия
game_name = "Призрачек"

# Цвет
font_color = (255, 140, 0)
walls_color = (25, 25, 112)

# Экран
display.set_caption(game_name)
display.set_icon(icon)
window = display.set_mode((wind_size[0], wind_size[1]))
background_effective = start_lobe_image
background = transform.scale(image.load(background_effective), (wind_size[0], wind_size[1]))
background_state = "start"

# flag
flag_start_sprite = True
game = True
flag_new_m = True

maze_2_playing = False
banana_playing = False
instruction_flag = False
maze_playing = False
finish = False
lose = False
coins_state = False
flag_playing = False
brick_game_playing = False
flag_brick_create = False

# Замки (флаги)
maze_1_look_flag = True
maze_2_look_flag = True
banana_look_flag = True
bricks_look_flag = True

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Спрайты
start_sprite = GameSprite(start_sprite_place[0], start_sprite_place[1],
                          start_sprite_image, start_sprite_speed,
                          start_sprite_size, start_sprite_size)
coin_maze = GameSprite(600, 400, coins_image, 0, coin_size * 2, coin_size * 2)
coins_counter_sprite = GameSprite(coins_counter_sprite_x, coins_counter_sprite_y,
                                  coins_image, coins_counter_speed, coin_size, coin_size)
info_button = GameSprite(info_button_x, info_button_y,
                         info_button_image, buttons_speed, info_button_size, info_button_size)
maze_1_look = GameSprite(buttons_x + (buttons_size[0] // 4), buttons_maze_y, looks_image,
                         buttons_speed, buttons_size[0] // 2, buttons_size[1])
maze_2_look = GameSprite(buttons_x + (buttons_size[0] // 4), button_maze_y_2, looks_image,
                         buttons_speed, buttons_size[0] // 2, buttons_size[1])
banana_look = GameSprite(buttons_x + (buttons_size[0] // 4), buttons_banana_y, looks_image,
                         buttons_speed, buttons_size[0] // 2, buttons_size[1])
bricks_look = GameSprite(buttons_x + (buttons_size[0] // 4), button_brick_game_y, looks_image,
                         buttons_speed, buttons_size[0] // 2, buttons_size[1])

island_1 = Islands(island_1_place[0], island_1_place[1], islands_image, island_1_speed,
                   island_size[0], island_size[1])
island_2 = Islands(island_2_place[0], island_2_place[1], islands_image, island_2_speed,
                   island_size[0], island_size[1])
island_3 = Islands(island_3_place[0], island_3_place[1], islands_image, island_3_speed,
                   island_size[0], island_size[1])

hero = Player(hero_place[0], hero_place[1], hero_image, hero_speed, hero_size, hero_size)
basket = Player(basket_place[0], basket_place[1], basket_image, basket_speed, basket_size[0], basket_size[1])

monster_1 = Monsters(monster_1_place[0], monster_1_place[1], monsters_image, monster_1_speed, monsters_size[0],
                     monsters_size[1])
monster_2 = Monsters(monster_2_place[0], monster_2_place[1], monsters_image, monster_2_speed, monsters_size[0],
                     monsters_size[1])
monster_3 = Monsters(monster_3_place[0], monster_3_place[1], monsters_image, monster_3_speed, monsters_size[0],
                     monsters_size[1])

coin_1 = Coins(coin_1_place[0], coin_1_place[1], coins_image, coin_1_speed, coin_size, coin_size)
coin_2 = Coins(coin_2_place[0], coin_2_place[1], coins_image, coin_2_speed, coin_size, coin_size)
coin_3 = Coins(coin_3_place[0], coin_3_place[1], coins_image, coin_3_speed, coin_size, coin_size)

button_flight = Buttons(buttons_x, buttons_flight_y,
                        button_flight_image, buttons_speed, buttons_size[0], buttons_size[1])
button_maze = Buttons(buttons_x, buttons_maze_y, button_maze_image, buttons_speed, buttons_size[0], buttons_size[1])
button_banana = Buttons(buttons_x, buttons_banana_y,
                        button_banana_image, buttons_speed, buttons_size[0], buttons_size[1])
button_maze_2 = Buttons(buttons_x, button_maze_y_2, button_maze_image_2,
                        buttons_speed, buttons_size[0], buttons_size[1])
button_brick_game = Buttons(buttons_x, button_brick_game_y, button_brick_game_image,
                            buttons_speed, buttons_size[0], buttons_size[1])

wall_1 = Wall(walls_color[0], walls_color[1], walls_color[2],
              wall_place_1[0], wall_place_1[1], wall_size_1[0], wall_size_1[1])
wall_2 = Wall(walls_color[0], walls_color[1], walls_color[2],
              wall_place_2[0], wall_place_2[1], wall_size_1[0], wall_size_1[1])
wall_3 = Wall(walls_color[0], walls_color[1], walls_color[2],
              wall_place_3[0], wall_place_3[1], wall_size_1[0], wall_size_1[1])
wall_4 = Wall(walls_color[0], walls_color[1], walls_color[2],
              wall_place_4[0], wall_place_4[1], wall_size_1[0], wall_size_1[1])
wall_5 = Wall(walls_color[0], walls_color[1], walls_color[2],
              wall_place_5[0], wall_place_5[1], wall_size_1[0], wall_size_1[1])
wall_2_1 = Wall(walls_color[0], walls_color[1], walls_color[2],
                wall_2_place_1[0], wall_2_place_1[1], wall_2_size_1[0], wall_2_size_1[1])
wall_2_2 = Wall(walls_color[0], walls_color[1], walls_color[2],
                wall_2_place_2[0], wall_2_place_2[1], wall_2_size_1[0], wall_2_size_1[1])
wall_2_3 = Wall(walls_color[0], walls_color[1], walls_color[2],
                wall_2_place_3[0], wall_2_place_3[1], wall_2_size_1[0], wall_2_size_1[1])
wall_2_4 = Wall(walls_color[0], walls_color[1], walls_color[2],
                wall_2_place_4[0], wall_2_place_4[1], wall_2_size_1[0], wall_2_size_1[1])
wall_2_5 = Wall(walls_color[0], walls_color[1], walls_color[2],
                wall_2_place_5[0], wall_2_place_5[1], wall_2_size_1[0], wall_2_size_1[1])

banana_1 = Bananas(banana_1_x, bananas_y, bananas_image, bananas_speed, bananas_size[0], bananas_size[1])
banana_2 = Bananas(banana_2_x, bananas_y, bananas_image, bananas_speed + 1, bananas_size[0], bananas_size[1])
banana_3 = Bananas(banana_3_x, bananas_y, bananas_image, bananas_speed + 2, bananas_size[0], bananas_size[1])

# Группы спрайтов
walls_2 = sprite.Group(wall_2_1, wall_2_2, wall_2_3, wall_2_4, wall_2_5)
bananas = sprite.Group(banana_1, banana_2, banana_3)
bricks = sprite.Group()
bullets = sprite.Group()
walls = sprite.Group(wall_1, wall_2, wall_3, wall_4, wall_5)
buttons = sprite.Group(button_brick_game, button_maze, button_flight, button_banana, button_maze_2,
                       maze_1_look, maze_2_look, banana_look, bricks_look)

# Октрытие/создание текстового файла с кол-вом койнов
try:
    with open('count_coins.txt', 'r', encoding='utf-8') as file:
        what_in_file = file.read()
        if what_in_file == "" or what_in_file == " ":
            coins_you_have = 0
        else:
            coins_you_have = int(what_in_file)
except IOError:
    with open('count_coins.txt', 'w', encoding='utf-8') as file:
        coins_you_have = 0
        file.write("0")

coins_counter = font.render(str(coins_you_have), True, font_color)


def update_coin():
    global coins_counter, coins_you_have
    coins_counter = font.render(str(coins_you_have), True, font_color)
    with open('count_coins.txt', 'w', encoding='utf-8') as file:
        file.write(str(coins_you_have))


def increase_volume_sounds():
    global volume_sounds
    if (pressed_keys[K_EQUALS] or pressed_keys[K_KP_PLUS] or pressed_keys[K_PLUS]) and volume_sounds <= 2:
        volume_sounds = float(volume_sounds + 0.01)
        mixer.music.set_volume(volume_sounds)
        transition.set_volume(volume_sounds)
        fire_effect.set_volume(volume_sounds)
        win_sound.set_volume(volume_sounds)
        touch_a_monster.set_volume(volume_sounds)
        award_sound.set_volume(volume_sounds)
        print(volume_sounds)
    elif (pressed_keys[K_UNDERSCORE] or pressed_keys[K_KP_MINUS] or pressed_keys[K_MINUS]) and volume_sounds >= 0:
        volume_sounds = float(volume_sounds - 0.01)
        mixer.music.set_volume(volume_sounds)
        transition.set_volume(volume_sounds)
        win_sound.set_volume(volume_sounds)
        touch_a_monster.set_volume(volume_sounds - 1)
        award_sound.set_volume(volume_sounds)
        print(volume_sounds)
    else:
        pass


def coin():
    global coins_state, coins_you_have, coins_counter

    coin_1.shift()
    coin_2.shift()
    coin_3.reset()
    coin_3.shift()
    coin_2.reset()
    coin_1.touching()
    coin_2.touching()
    coin_3.touching()
    coin_1.reset()
    coin_1.update()
    coin_2.update()
    coin_3.update()
    coins_counter_sprite.reset()

    if coins_state:
        coins_you_have += 1
        update_coin()
        coins_state = False
    if pressed_keys[K_q]:
        coins_you_have = 0
        coins_counter = font.render(str(coins_you_have), True, font_color)
    window.blit(coins_counter, (font_place[0], font_place[1]))


def look():
    global maze_1_look_flag, maze_2_look_flag, banana_look_flag, bricks_look_flag, coins_you_have
    pressed = mouse.get_pressed()
    mouse_pos = mouse.get_pos()
    mouse_sensor = GameSprite(mouse_pos[0], mouse_pos[1], mouse_image, 0, 1, 1)
    if (pressed_keys[K_b] or (pressed[0] and sprite.collide_rect(button_maze, mouse_sensor))) \
            and maze_1_look_flag and coins_you_have >= 100:
        maze_1_look_flag = False
        coins_you_have -= 100
        win_sound.play()
        maze_1_look.kill()

        update_coin()
    elif (pressed[0] and sprite.collide_rect(button_maze, mouse_sensor)) \
            and maze_1_look_flag and coins_you_have < 100:
        touch_a_monster.play()
    elif (pressed_keys[K_b] or (pressed[0] and sprite.collide_rect(button_banana, mouse_sensor))) \
            and banana_look_flag and coins_you_have >= 500:
        banana_look_flag = False
        coins_you_have -= 500
        win_sound.play()
        banana_look.kill()
        update_coin()
    elif (pressed[0] and sprite.collide_rect(button_banana, mouse_sensor)) \
            and banana_look_flag and coins_you_have < 500:
        touch_a_monster.play()
    elif (pressed_keys[K_b] or (pressed[0] and sprite.collide_rect(button_maze_2, mouse_sensor))) \
            and maze_2_look_flag and coins_you_have >= 1000:
        maze_2_look_flag = False
        coins_you_have -= 1000
        win_sound.play()
        maze_2_look.kill()
        update_coin()
    elif (pressed[0] and sprite.collide_rect(button_maze_2, mouse_sensor)) \
            and maze_2_look_flag and coins_you_have < 1000:
        touch_a_monster.play()
    elif (pressed_keys[K_b] or (pressed[0] and sprite.collide_rect(button_brick_game, mouse_sensor))) \
            and bricks_look_flag and coins_you_have >= 1500:
        bricks_look_flag = False
        coins_you_have -= 1500
        win_sound.play()
        bricks_look.kill()
        update_coin()
    elif (pressed[0] and sprite.collide_rect(button_brick_game, mouse_sensor)) \
            and bricks_look_flag and coins_you_have < 1500:
        touch_a_monster.play()

    if maze_1_look_flag:
        maze_2_look_flag = True
        banana_look_flag = True
        bricks_look_flag = True
    elif banana_look_flag:
        maze_2_look_flag = True
        bricks_look_flag = True
    elif maze_2_look_flag:
        bricks_look_flag = True
    elif bricks_look_flag:
        maze_1_look_flag = False
        maze_2_look_flag = False
        banana_look_flag = False

    coins_counter_sprite.reset()
    window.blit(coins_counter, (font_place[0], font_place[1]))


def islands():
    island_1.update()
    island_2.update()
    island_3.update()
    island_1.reset()
    island_2.reset()
    island_3.reset()
    island_1.shift()
    island_2.shift()
    island_3.shift()


def hero_interaction():
    hero.reset()
    hero.update()
    hero.physics()
    hero.lose_flore()


def monsters():
    monster_1.update()
    monster_2.update()
    monster_3.update()
    monster_1.reset()
    monster_1.shift()
    monster_2.reset()
    monster_2.shift()
    monster_3.reset()
    monster_3.shift()


def start_sprite_interaction():
    start_sprite.update()
    start_sprite.reset()


def swoop_m():
    global gaming_music, gaming_music_2, gaming_music_1
    if gaming_music == gaming_music_1:
        gaming_music = gaming_music_2
        mixer.music.stop()
        mixer.music.load(gaming_music)
        mixer.music.play()
    else:
        gaming_music = gaming_music_1
        mixer.music.stop()
        mixer.music.load(gaming_music)
        mixer.music.play()


def loosing():
    global lose, island_1, island_2, \
        island_3, hero, monster_1, monster_2, \
        monster_3, coin_1, coin_2, coin_3, background_state, \
        flag_start_sprite, flag_playing, maze, maze_playing, banana, banana_playing

    if (sprite.collide_rect(hero, monster_1) or
            sprite.collide_rect(hero, monster_2) or
            sprite.collide_rect(hero, monster_3)):
        lose = True
        background_state = "start"
    if lose:
        flag_start_sprite = True
        island_1 = Islands(island_1_place[0], island_1_place[1],
                           islands_image, island_1_speed, island_size[0], island_size[1])
        island_2 = Islands(island_2_place[0], island_2_place[1],
                           islands_image, island_2_speed, island_size[0], island_size[1])
        island_3 = Islands(island_3_place[0], island_3_place[1],
                           islands_image, island_3_speed, island_size[0], island_size[1])

        hero = Player(hero_place[0], hero_place[1], hero_image, hero_speed, hero_size, hero_size)

        monster_1 = Monsters(monster_1_place[0], monster_1_place[1],
                             monsters_image, monster_1_speed, monsters_size[0], monsters_size[1])
        monster_2 = Monsters(monster_2_place[0], monster_2_place[1],
                             monsters_image, monster_2_speed, monsters_size[0], monsters_size[1])
        monster_3 = Monsters(monster_3_place[0], monster_3_place[1],
                             monsters_image, monster_3_speed, monsters_size[0], monsters_size[1])

        coin_1 = Coins(coin_1_place[0], coin_1_place[1], coins_image, coin_1_speed, coin_size, coin_size)
        coin_2 = Coins(coin_2_place[0], coin_2_place[1], coins_image, coin_2_speed, coin_size, coin_size)
        coin_3 = Coins(coin_3_place[0], coin_3_place[1], coins_image, coin_3_speed, coin_size, coin_size)

        touch_a_monster.play()
        lose = False
        maze = 0
        maze_playing = False
        banana = 0
        banana_playing = False
    background_state = "start"


def play_fly_boll():
    global background_state
    islands()
    hero_interaction()
    monsters()
    coin()
    loosing()
    background_state = "fly"


def maze_game():
    global coins_state, coins_you_have, coins_counter
    hero.update()
    hero.reset()
    walls.update()
    if coins_state:
        coins_you_have += 1
        update_coin()
        coins_state = False
    if pressed_keys[K_q]:
        coins_you_have = 0
        coins_counter = font.render(str(coins_you_have), True, font_color)
    window.blit(coins_counter, (font_place[0], font_place[1]))
    coin_maze.reset()


def win():
    global background_state, maze_playing, hero, flag_start_sprite, coins_you_have, \
        coins_counter, maze_2_playing, flag_playing, maze, maze_2, banana, banana_playing, brick_game, \
        brick_game_playing, num_bricks
    maze_playing = False
    flag_start_sprite = True
    flag_playing = False
    maze = 0
    banana = 0
    banana_playing = False
    maze_2 = 0
    maze_2_playing = False
    hero = Player(hero_place[0], hero_place[1], hero_image, hero_speed, hero_size, hero_size)
    coins_you_have += 100
    brick_game = 0
    num_bricks = 25
    brick_game_playing = False
    win_sound.play()
    update_coin()


def banana_game():
    global coins_state, coins_you_have, coins_counter
    basket.reset()
    basket.update()
    banana_1.reset()
    banana_2.reset()
    banana_3.reset()
    bananas.update()
    if coins_state:
        coins_you_have += 1
        update_coin()
        coins_state = False
    if pressed_keys[K_q]:
        coins_you_have = 0
        coins_counter = font.render(str(coins_you_have), True, font_color)
    window.blit(coins_counter, (font_place[0], font_place[1]))


def maze_2_game():
    global coins_state, coins_you_have, coins_counter
    hero.update()
    hero.reset()
    walls_2.update()
    if coins_state:
        coins_you_have += 1
        update_coin()
        coins_state = False
    if pressed_keys[K_q]:
        coins_you_have = 0
        coins_counter = font.render(str(coins_you_have), True, font_color)
    window.blit(coins_counter, (font_place[0], font_place[1]))
    coin_maze.reset()


def brick_game_game():
    global coins_state, coins_you_have, coins_counter, num_bricks, flag_brick_create, brick_y, brick_x
    hero.update()
    hero.reset()
    if flag_brick_create:
        flag_brick_create = False
        brick_y = 0
        brick_x = 0
        flag_sprite_while = 0
        start_wall_flag = 0
        while flag_sprite_while != 5:
            brick_x = 0
            for i in range(6):
                brick = GameSprite(brick_x, brick_y, brick_image, 0, brick_size[0], brick_size[1])
                bricks.add(brick)
                brick_x += 140
            if start_wall_flag != 2:
                brick = GameSprite(brick_x, brick_y, brick_image, 0, brick_size[0], brick_size[1])
                bricks.add(brick)
                brick_x += 140
                start_wall_flag += 1
            brick_y += 50
            flag_sprite_while += 1

    if coins_state:
        coins_you_have += 1
        update_coin()
        coins_state = False
    if pressed_keys[K_q]:
        coins_you_have = 0
        coins_counter = font.render(str(coins_you_have), True, font_color)
    if num_bricks == 0:
        win()
    window.blit(coins_counter, (font_place[0], font_place[1]))
    coins_counter_sprite.reset()
    bullets.update()
    bullets.draw(window)
    bricks.update()
    bricks.draw(window)


def definition_lobe():
    global background_image, background_state, background_effective, background, \
        coin_1, coin_2, coin_3, coin_size, coins_image, coin_1_speed, coin_2_speed, coin_3_speed
    if background_state == "fly" and background_effective != background_image:
        background_effective = background_image
        background = transform.scale(image.load(background_effective), (wind_size[0], wind_size[1]))
    elif background_state == "fly" and background_effective == background_image:
        pass

    if background_state == "start" and background_effective != start_lobe_image:
        background_effective = start_lobe_image
        background = transform.scale(image.load(background_effective), (wind_size[0], wind_size[1]))
    elif background_state == "start" and background_effective == start_lobe_image:
        pass

    if background_state == "choose" and background_effective != choose_lobe_image:
        background_effective = choose_lobe_image
        background = transform.scale(image.load(background_effective), (wind_size[0], wind_size[1]))
    elif background_state == "choose" and background_effective == choose_lobe_image:
        buttons.update()
        buttons.draw(window)
        look()
    if background_state == "maze" and background_effective != maze_background:
        background_effective = maze_background
        background = transform.scale(image.load(background_effective), (wind_size[0], wind_size[1]))

        coin_1 = Coins(500, 0, coins_image, coin_1_speed, coin_size, coin_size)
        coin_2 = Coins(500, 250, coins_image, coin_2_speed, coin_size, coin_size)
        coin_3 = Coins(500, 400, coins_image, coin_3_speed, coin_size, coin_size)
    elif background_state == "maze" and background_effective == maze_background:
        pass

    if background_state == "instruction" and background_effective != background_image:
        background_effective = instruction_image
        background = transform.scale(image.load(background_effective), (wind_size[0], wind_size[1]))
    elif background_state == "instruction" and background_effective == background_image:
        pass

    if background_state == "banana" and background_effective != banana_image:
        background_effective = banana_image
        background = transform.scale(image.load(background_effective), (wind_size[0], wind_size[1]))
    elif background_state == "banana" and background_effective == banana_image:
        pass

    if background_state == "brick_game" and background_effective != brick_game_image:
        background_effective = brick_game_image
        background = transform.scale(image.load(background_effective), (wind_size[0], wind_size[1]))
    elif background_state == "brick_game" and background_effective == brick_game_image:
        pass


def button_start():
    global flag_start_sprite, background_state, flag_playing, flag_new_m, gaming_music, \
        gaming_music_1, instruction_flag, maze, maze_playing, banana, banana_playing, maze_2_playing, \
        maze_2, brick_game, brick_game_playing, coins_counter_sprite, flag_brick_create, maze_1_look_flag, \
        maze_2_look_flag, banana_look_flag, bricks_look_flag
    choose = False
    pressed = mouse.get_pressed()
    mouse_pos = mouse.get_pos()
    mouse_sensor = GameSprite(mouse_pos[0], mouse_pos[1], mouse_image, 0, 1, 1)

    if pressed[0] and sprite.collide_rect(info_button, mouse_sensor) and not instruction_flag:
        instruction_flag = True
        sleep(0.5)
    elif pressed[0] and sprite.collide_rect(info_button, mouse_sensor) and instruction_flag:
        instruction_flag = False
        sleep(0.5)
    if instruction_flag:
        background_state = "instruction"
        info_button.reset()
    if not instruction_flag:
        if flag_start_sprite:
            start_sprite_interaction()
            background_state = "start"
            info_button.reset()

            if (pressed_keys[K_SPACE] or (pressed[0] and sprite.collide_rect(start_sprite, mouse_sensor))) \
                    and not choose:
                flag_start_sprite = False
                transition.play()
                choose = True
            if choose:
                background_state = "choose"

            flag_playing = False
        if not flag_start_sprite:
            if (pressed[0] and sprite.collide_rect(button_flight, mouse_sensor)) \
                    and not flag_playing:
                flag_playing = True
                flag_new_m = True
                transition.play()
            elif (pressed[0] and sprite.collide_rect(button_maze, mouse_sensor)) \
                    and not maze_playing and not maze_1_look_flag:
                maze += 1
                sleep(0.25)
            elif (pressed[0] and sprite.collide_rect(button_banana, mouse_sensor)) \
                    and not banana_playing and not banana_look_flag:
                banana += 1
                sleep(0.25)
            elif (pressed[0] and sprite.collide_rect(button_maze_2, mouse_sensor)) \
                    and not maze_2_playing and not maze_2_look_flag:
                maze_2 += 1
                sleep(0.25)
            elif (pressed[0] and sprite.collide_rect(button_brick_game, mouse_sensor)) \
                    and not brick_game_playing and not bricks_look_flag:
                brick_game += 1
                sleep(0.25)
            if flag_new_m:
                gaming_music = gaming_music_1
                mixer.music.stop()
                mixer.music.load(gaming_music)
                mixer.music.play()
                flag_new_m = False
            else:
                pass
            if flag_playing:
                play_fly_boll()
            if maze == 2 and not maze_playing:
                maze_playing = True
                transition.play()
            if maze_playing:
                maze_game()
                background_state = "maze"
            else:
                coins_counter_sprite = GameSprite(coins_counter_sprite_x, coins_counter_sprite_y,
                                                  coins_image, coins_counter_speed, coin_size, coin_size)
            if maze_2 == 2 and not maze_2_playing:
                maze_2_playing = True
                transition.play()
            if maze_2_playing:
                maze_2_game()
                background_state = "maze"
            else:
                coins_counter_sprite = GameSprite(coins_counter_sprite_x, coins_counter_sprite_y,
                                                  coins_image, coins_counter_speed, coin_size, coin_size)
            if banana == 2 and not banana_playing:
                banana_playing = True
                transition.play()
            if banana_playing:
                banana_game()
                background_state = "banana"
            if brick_game == 2 and not brick_game_playing:
                transition.play()
                hero.rect.y = 400
                flag_brick_create = True
                brick_game_playing = True
            if brick_game_playing:
                brick_game_game()
                background_state = "brick_game"

    else:
        pass


while game:
    window.blit(background, (0, 0))

    pressed_keys = key.get_pressed()
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == MOUSEBUTTONDOWN:
            button_status = e.button
    update_coin()
    button_start()
    definition_lobe()
    increase_volume_sounds()
    display.update()
    clock.tick(FPS)

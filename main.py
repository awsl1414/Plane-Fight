from random import randint
import pygame
from pygame.locals import *

# 初始化pygame
pygame.init()
pygame.mixer.init()

# 图片资源加载
BACKGROUND_IMAGE_PATH = pygame.image.load("./resource/bg.png")
PLAYER_IMAGE_PATH = pygame.image.load("./resource/player.png")
BULLET_IMAGE_PATH = pygame.image.load("./resource/bullet.png")
ENEMY1_IMAGE_PATH = pygame.image.load("./resource/enemy.png")
ENEMY2_IMAGE_PATH = pygame.image.load("./resource/enemy2.png")
UFO_IMAGE_PATH = pygame.image.load("./resource/ufo.png")
BOMB_IMAGE_PATH = pygame.image.load("./resource/bomb.png")

# 音频资源加载
pygame.mixer_music.load("./resource/bg_music.mp3")

# 音量设置
# pygame.mixer.music.set_volume(0.5)  # 设置音量范围为 0.0 到 1.0

# 播放背景音乐（-1表示循环播放，0表示播放一次）
pygame.mixer.music.play(-1)


class PlayerPlane(object):
    def __init__(self, screen_temp, PLAYER_IMAGE_PATH):
        self.x = 350
        self.y = 420
        self.screen = screen_temp
        self.image = PLAYER_IMAGE_PATH
        self.bullets = []
        self.speed = 5
        self.last_shot_time = pygame.time.get_ticks()  # 记录上一次发射子弹的时间

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))

    def update(self):
        self.display()
        self.press_move()
        for bullet in self.bullets[:]:
            bullet.display()
            bullet.move()
            if bullet.judge():
                self.bullets.remove(bullet)

    def press_move(self):
        key_pressed = pygame.key.get_pressed()
        min_x = 0
        max_x = self.screen.get_width() - self.image.get_width()
        min_y = 0
        max_y = self.screen.get_height() - self.image.get_height()

        if (key_pressed[K_a] or key_pressed[K_LEFT]) and self.x > min_x:
            self.x -= self.speed
        if (key_pressed[K_d] or key_pressed[K_RIGHT]) and self.x < max_x:
            self.x += self.speed
        if (key_pressed[K_w] or key_pressed[K_UP]) and self.y > min_y:
            self.y -= self.speed
        if (key_pressed[K_s] or key_pressed[K_DOWN]) and self.y < max_y:
            self.y += self.speed

    # 发射子弹
    def fire(self):
        # 控制子弹发射频率
        shot_interval = 1000  # 1000ms

        current_time = pygame.time.get_ticks()  # 获取当前时间

        if current_time - self.last_shot_time > shot_interval:
            self.bullets.append(Bullet(self.screen, self.x, self.y))
            self.last_shot_time = current_time


class Bullet(object):
    def __init__(self, screen_temp, x, y):
        self.x = x + 16
        self.y = y - 24
        self.screen = screen_temp
        self.image = BULLET_IMAGE_PATH

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.y -= 8

    def judge(self):
        if self.y < 0:
            return True
        else:
            return False


class EnemyPlane(object):
    def __init__(self, screen_temp, enemy_image):
        self.image = enemy_image
        self.screen = screen_temp
        self.x = randint(0, self.screen.get_width() - self.image.get_width() + 1)
        self.y = 0 - self.image.get_height()
        # self.y = 0

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))

    def move(self):
        if self.y < self.screen.get_height():
            self.y += 2
        else:
            self.y = 0
            self.x = randint(0, self.screen.get_width() - self.image.get_width() + 1)


def main():

    screen_size = (800, 600)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("飞机大战")

    player = PlayerPlane(screen_temp=screen, PLAYER_IMAGE_PATH=PLAYER_IMAGE_PATH)
    enemy1 = EnemyPlane(screen_temp=screen, enemy_image=ENEMY1_IMAGE_PATH)

    clock = pygame.time.Clock()

    while True:
        screen.blit(BACKGROUND_IMAGE_PATH, (0, 0))
        player.update()
        player.fire()
        enemy1.display()
        enemy1.move()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()  # 卸载所有的模块
                exit()  # 退出程序
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit()

        pygame.display.update()
        clock.tick(60)  # 控制游戏最大帧率为60


if __name__ == "__main__":
    main()

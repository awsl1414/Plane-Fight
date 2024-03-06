import pygame
from pygame.locals import *

# 资源加载
background = pygame.image.load("./resource/bg.png")
play_image = pygame.image.load("./resource/player.png")
bullet_image = pygame.image.load("./resource/bullet.png")


class PlayerPlane(object):
    def __init__(self, screen_temp):
        self.x = 350
        self.y = 420
        self.screen = screen_temp
        self.image = play_image
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
        self.image = bullet_image

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.y -= 8

    def judge(self):
        if self.y < 0:
            return True
        else:
            return False


def main():
    # 初始化pygame
    pygame.init()

    screen_size = 800, 600
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("飞机大战")

    player = PlayerPlane(screen_temp=screen)

    clock = pygame.time.Clock()

    while True:
        screen.blit(background, (0, 0))
        player.update()
        player.fire()

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

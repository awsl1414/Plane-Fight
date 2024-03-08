import random
import pygame

# 屏幕大小的常量
SCREEN_RECT = pygame.Rect(0, 0, 800, 600)
# 刷新的帧率
FRAME_PER_SEC = 60
# 创建敌机的定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 英雄发射子弹事件
HERO_FIRE_EVENT = pygame.USEREVENT + 1

BULLET_SPEED_TIME = 300


class GameSprite(pygame.sprite.Sprite):
    """飞机大战游戏精灵"""

    def __init__(self, image_name, speed=1):

        # 调用父类的初始化方法
        super().__init__()

        # 定义对象属性
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):

        # 在屏幕垂直方向上移动
        self.rect.y += self.speed


class Background(GameSprite):
    """游戏背景精灵"""

    def __init__(self, is_alt=False):

        # 调用父类方法实现精灵的创建（image/rect/speed）
        super().__init__("./resource/bg.png")

        # 判断是否是交替图像，如果是，需要设置初始位置
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):

        # 调用父类的方法实现：垂直移动
        super().update()

        # 判断是否移出屏幕，若移出屏幕，应该将图像设置到图像上方
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Hero(GameSprite):
    """英雄精灵"""

    def __init__(self):

        # 调用父类方法，设置image speed
        super().__init__("./resource/hero.png", 0)

        # 设置英雄初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120

        # 创建子弹的精灵组
        self.bullets = pygame.sprite.Group()
        self.last_shot_time = pygame.time.get_ticks()  # 记录上一次发射子弹的时间

    def update(self):
        # 使用键盘提供的方法获取键盘按键 --按键元组
        keys_pressed = pygame.key.get_pressed()
        # 判断元组中对应的按键索引值 1
        if keys_pressed[pygame.K_d]:
            self.rect.x += 2
        if keys_pressed[pygame.K_a]:
            self.rect.x -= 2
        if keys_pressed[pygame.K_s]:
            self.rect.y += 2
        if keys_pressed[pygame.K_w]:
            self.rect.y -= 2
        if keys_pressed[pygame.K_SPACE]:
            self.fire()

        # 控制英雄不能离开屏幕
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.y < 0:
            self.rect.y = 0

        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

        self.bullets.update()
        self.bullets.draw(screen)

    def fire(self):
        print("发射子弹")
        current_time = pygame.time.get_ticks()  # 获取当前时间

        if current_time - self.last_shot_time > BULLET_SPEED_TIME:
            # 创建子弹精灵
            bullet = Bullet()
            self.bullets.add(bullet)
            self.last_shot_time = current_time

            # 设置精灵的位置
            bullet.rect.bottom = self.rect.y
            bullet.rect.centerx = self.rect.centerx


class Enemy(GameSprite):
    """敌机精灵"""

    def __init__(self, image_name):
        # 调用父类方法，创建敌机精灵，同时指定敌机图片
        super().__init__(image_name)
        # 指定敌机的初始随机速度
        self.speed = random.randint(1, 3)

        # 指定敌机的初始随机位置
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x + 1)

    def update(self):

        # 调用父类方法，保持垂直方向上的飞行
        super().update()
        # 判断是否飞出屏幕，如果是，需要从精灵组删除敌机
        # if self.rect.y >= 300:
        if self.rect.y >= SCREEN_RECT.height:
            # print("飞出屏幕，需要从精灵组删除")
            # kill 方法可以将精灵从所有精灵组中移出，精灵就会被自动销毁
            self.kill()

    def __del__(self):
        # print("敌机挂了 %s" %self.rect)
        pass


class Bullet(GameSprite):
    """子弹精灵"""

    def __init__(self):

        # 调用父类方法设施子弹图片 初始速度
        super().__init__("./resource/bullet.png", -2)

    def update(self):

        # 调用父类方法，让子弹沿垂直方向飞行
        super().update()

        # 判断子弹是否飞出屏幕
        if self.rect.bottom < 0:
            self.kill()

    def __del__(self):
        print("子弹被销毁")


# 创建英雄精灵
hero = Hero()
# 创建敌机精灵
enemy1 = Enemy("./resource/enemy.png")
enemy2 = Enemy("./resource/enemy2.png")


# 创建背景精灵组
bg_group = pygame.sprite.Group(Background(), Background(is_alt=True))
# 创建英雄精灵组

hero_group = pygame.sprite.Group(hero)

# 创建敌机精灵组
enemy_group = pygame.sprite.Group(enemy1, enemy2)


clock = pygame.time.Clock()
if __name__ == "__main__":
    # 初始化 Pygame
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_RECT.size)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():

            # 判断是否退出游戏
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        bg_group.update()
        bg_group.draw(screen)
        hero_group.update()
        hero_group.draw(screen)
        enemy_group.update()
        enemy_group.draw(screen)

        # 刷新屏幕
        pygame.display.update()
        # 设置刷新帧率
        clock.tick(FRAME_PER_SEC)

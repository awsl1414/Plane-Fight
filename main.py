import random
import pygame

from sprites import *

# 创建英雄精灵
hero = Hero()


# 创建背景精灵组
bg_group = pygame.sprite.Group(Background(), Background(is_alt=True))
# 创建英雄精灵组

hero_group = pygame.sprite.Group(hero)


enemy_group = pygame.sprite.Group()


clock = pygame.time.Clock()
explosion_sound = pygame.mixer.Sound("./resource/bomb_music.mp3")
bullet_sound = pygame.mixer.Sound("./resource/bullet_music.wav")
if __name__ == "__main__":
    # 初始化 Pygame
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode(SCREEN_RECT.size)
    clock = pygame.time.Clock()
    pygame.time.set_timer(CREATE_ENEMY1_EVENT, 1000)  # 每1秒创建敌机1
    pygame.time.set_timer(CREATE_ENEMY2_EVENT, 3000)  # 每3秒创建敌机2
    while True:
        for event in pygame.event.get():

            # 判断是否退出游戏
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == CREATE_ENEMY1_EVENT:
                # 创建敌机1
                enemy1 = Enemy("./resource/enemy.png")

                enemy_group.add(enemy1)
            elif event.type == CREATE_ENEMY2_EVENT:
                # 创建敌机2
                enemy2 = Enemy("./resource/enemy2.png")

                enemy_group.add(enemy2)

        bg_group.update()
        bg_group.draw(screen)
        hero_group.update()
        hero_group.draw(screen)
        enemy_group.update()
        enemy_group.draw(screen)
        # 子弹摧毁敌机
        # pygame.sprite.groupcollide(hero.bullets, enemy_group, True, True)

        # 敌机撞英雄
        enemies = pygame.sprite.spritecollide(hero, enemy_group, True)
        # 判断是否有内容
        if len(enemies) > 0:
            for enemy in enemies:
                explosion_sound.play()
                explosion_group = pygame.sprite.Group()
                explosion = Explosion(enemy.rect.center)
                explosion_group.add(explosion)
                explosion_group.update()
                explosion_group.draw(screen)

            # 牺牲英雄飞机
            hero.kill()
            # print("你输了")
            # exit()
        for bullet in hero.bullets:
            hits = pygame.sprite.spritecollide(bullet, enemy_group, True)
            for hit in hits:
                explosion_sound.play()
                explosion_group = pygame.sprite.Group()
                explosion = Explosion(hit.rect.center)
                explosion_group.add(explosion)
                bullet.kill()
                explosion_group.update()
                explosion_group.draw(screen)

        # 刷新屏幕
        pygame.display.update()
        # 设置刷新帧率
        clock.tick(FRAME_PER_SEC)


class PlaneGame(object):
    def __init__(self) -> None:
        # 创建游戏窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 设置游戏标题
        pygame.display.set_caption("飞机大战 - awsl1414")
        # 创建游戏时钟
        self.clock = pygame.time.Clock()

        # 调用私有方法，精灵和精灵组的创建
        self.__create_sprites()

        # 设定定时器事件 - 创建敌机
        pygame.time.set_timer(CREATE_ENEMY1_EVENT, 1000)
        pygame.time.set_timer(CREATE_ENEMY2_EVENT, 3000)

    def __game_start(self):
        # 设置刷新率
        self.clock.tick(FRAME_PER_SEC)
        # TODO 事件监听

    def __game_over(self):
        print("游戏结束")
        pygame.quit()
        exit()

    def __event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            elif event.type == CREATE_ENEMY1_EVENT:
                enemy1 = Enemy("./resource/enemy.png")
                self.enemy_group.add(enemy1)
            e

    def __create_sprites(self):

        # 创建背景精灵和精灵组
        bg1 = Background()
        bg2 = Background(is_alt=True)
        self.back_group = pygame.sprite.Group(bg1, bg2)

        # 创建英雄精灵和精灵组

        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

        # 创建敌机精灵组
        self.enemy_group = pygame.sprite.Group()

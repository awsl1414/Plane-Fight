from sprites import *


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

    def game_start(self):
        print("游戏开始...")

        while True:
            # 设置刷新率
            self.clock.tick(FRAME_PER_SEC)
            # 事件监听
            self.__event_handler()
            # 碰撞检测
            self.__check_collide()
            # 更新绘制精灵
            self.__update_sprites()
            # 更新显示
            pygame.display.update()

    @staticmethod  # 静态方法
    def __game_over():
        print("游戏结束")

        # 卸载所有模块
        pygame.quit()
        # 退出程序
        exit()

    def __event_handler(self):
        # 事件监听
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__game_over()

            # 定时器事件创建敌机
            elif event.type == CREATE_ENEMY1_EVENT:
                enemy1 = Enemy("./resource/enemy.png")
                self.enemy_group.add(enemy1)
            elif event.type == CREATE_ENEMY2_EVENT:
                enemy2 = Enemy("./resource/enemy2.png")
                self.enemy_group.add(enemy2)

        # 使用键盘提供的方法获取键盘按键 --按键元组
        keys_pressed = pygame.key.get_pressed()
        # 判断元组中对应的按键索引值
        if keys_pressed[pygame.K_d]:
            self.hero.rect.x += 2
        if keys_pressed[pygame.K_a]:
            self.hero.rect.x -= 2
        if keys_pressed[pygame.K_s]:
            self.hero.rect.y += 2
        if keys_pressed[pygame.K_w]:
            self.hero.rect.y -= 2

        # 按空格键发射子弹
        if keys_pressed[pygame.K_SPACE]:
            self.hero.fire()

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

        # 创建爆炸精灵组
        self.explosion_group = pygame.sprite.Group()

    def __check_collide(self):
        # 子弹摧毁敌机并生成爆炸效果
        for bullet in self.hero.bullets:
            hits = pygame.sprite.spritecollide(bullet, self.enemy_group, True)
            for hit in hits:
                explosion = Explosion(hit.rect.center)
                self.explosion_group.add(explosion)
                bullet.kill()

        # 敌机撞英雄
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        # 判断是否有内容
        if len(enemies) > 0:
            # 牺牲英雄飞机
            self.hero.kill()
            for enemy in enemies:
                # 获取碰撞点
                explosion_center = enemy.rect.center
                # 生成爆炸对象
                explosion = Explosion(explosion_center)
                # 将爆炸对象添加到显示组或更新组等（取决于您如何处理这些对象）
                self.explosion_group.add(explosion)
                self.explosion_group.update()
                self.explosion_group.draw(self.screen)
                pygame.display.update()
            # 游戏结束
            PlaneGame.__game_over()

    def __update_sprites(self):

        self.back_group.update()
        self.back_group.draw(self.screen)

        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        self.hero_group.update()
        self.hero_group.draw(self.screen)

        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

        self.explosion_group.update()
        self.explosion_group.draw(self.screen)


if __name__ == "__main__":
    # 初始化pygame
    pygame.init()
    pygame.mixer.init()
    # 创建游戏对象
    game = PlaneGame()

    # 启动游戏
    game.game_start()

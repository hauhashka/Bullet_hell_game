import os
import random
import sqlite3
import sys

import pygame
"""Задание границ экрана и инициализация самого экрана"""
size = width, height = 1200, 900
screen = pygame.display.set_mode(size)
"""Инициализация pygame и все необходимые переменные"""
pygame.init()
level1_available = True
level2_available = False
level3_available = False
SKELETON_SPAWN = pygame.USEREVENT + 1
girl_frame_change = pygame.USEREVENT + 2
girl_hit = pygame.USEREVENT + 3
girl_dance = pygame.USEREVENT + 4
skeleton_shoot = pygame.USEREVENT + 5
skeleton_change_frame = pygame.USEREVENT + 6

bad_guys = pygame.sprite.Group()

con = sqlite3.connect('data/WinsAndLooses')


def load_image(name, colorkey=None):
    '''Функция необходимая для загрузки картинки'''
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class ButtonLevel1(pygame.sprite.Sprite):
    """Класс необходимый для создания кнопки первого уровня на главном экране"""
    cur = con.cursor()

    if level1_available:
        image = load_image('lv1_en.png')
    else:
        image = load_image('lv1_dis.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = ButtonLevel1.image
        self.rect = self.image.get_rect()
        self.rect.x = 90
        self.rect.y = 350
        self.pos = (200, 100)

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos) and level1_available:
            load_level(1)


class ButtonLevel2(pygame.sprite.Sprite):
    """Класс для создания кнопки второго уровня на главном экране"""
    def __init__(self, *group):
        super().__init__(*group)
        cur = con.cursor()
        self.level2_available = cur.execute('SELECT passed FROM WL '
                                            'WHERE level like "1"').fetchall()
        level2_images = (load_image('lv2_en.png'), load_image('lv2_dis.png'))
        if self.level2_available[0][0]:
            self.image = level2_images[0]
        else:
            self.image = level2_images[1]
        self.rect = self.image.get_rect()
        self.rect.x = 90
        self.rect.y = 450
        self.pos = (200, 100)

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos) and self.level2_available[0][0]:
            load_level(2)


class ButtonLevel3(pygame.sprite.Sprite):
    """"Клосс для создания кнопки третьего уровня на главном экране"""
    def __init__(self, *group):
        super().__init__(*group)
        cur = con.cursor()
        self.level3_available = cur.execute('SELECT passed FROM WL '
                                            'WHERE level like "2"').fetchall()
        level3_images = (load_image('lv3_en.png'), load_image('lv3_dis.png'))
        if self.level3_available[0][0]:
            self.image = level3_images[0]
        else:
            self.image = level3_images[1]
        self.rect = self.image.get_rect()
        self.rect.x = 90
        self.rect.y = 550
        self.pos = (200, 100)

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos) and self.level3_available[0][0]:
            load_level(3)


class Background(pygame.sprite.Sprite):
    """Класс для отрисовки фона на главном экране"""
    girl = load_image('girl_1.1.jpg')
    girl = pygame.transform.scale(girl, (600, 900))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Background.girl
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 0
        self.pos = (0, 0)


class Logo(pygame.sprite.Sprite):
    """Класс для отрисовки логотипа на главном экране"""
    logo = load_image('logo.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Logo.logo
        self.rect = self.image.get_rect()
        self.rect.x = 250
        self.rect.y = -50


class Girl(pygame.sprite.Sprite):
    """Класс для создания и проработки логики движения девочки на экране игры"""
    girl_stands = load_image('girl_idle.png')
    girl_hurt = load_image('girl_hurt.png')
    girl_walk = [load_image('girl_walk_1.png'), load_image('girl_walk_2.png')]
    girl_dance = [load_image('girl_dance_1.png'), load_image('girl_dance_2.png')]
    girl_cry = [load_image('girl_cry_1.png'), load_image('girl_cry_2.png')]

    def __init__(self, *group):
        """Инициализация спрайта девочки"""
        super().__init__(*group)
        self.image = Girl.girl_stands
        self.speed = 6
        self.rect = self.image.get_rect().move(570, 700)
        self.movex = 0
        self.movey = 0
        self.hp = 3
        self.frame = 0
        self.cooldown = 400
        self.last = pygame.time.get_ticks()
        self.last_hurt = pygame.time.get_ticks()
        self.cooldown_hurt = 700

    def hit(self):
        """Метод для проработки снимания хп"""
        now = pygame.time.get_ticks()
        if pygame.sprite.spritecollideany(self, bad_guys) or pygame.sprite.spritecollideany(self, bullets_skel):
            if now - self.last_hurt >= self.cooldown_hurt:
                if pygame.sprite.spritecollideany(self, bad_guys):
                    pygame.sprite.spritecollideany(self, bad_guys).kill()
                while pygame.sprite.spritecollideany(self, bullets_skel):
                    pygame.sprite.spritecollideany(self, bullets_skel).rect.x += pygame.sprite.spritecollideany(self,
                                                                                                                bullets_skel).vel
                    pygame.sprite.spritecollideany(self, bullets_skel).kill()
                self.last_hurt = now
                self.hp -= 1
                self.image = Girl.girl_hurt
                if self.hp == 0:
                    lost()

    def shoot(self):
        """Метод для стрельбы"""
        now = pygame.time.get_ticks()
        if now - self.last >= self.cooldown:
            self.last = now
            bullet = BulletGirl(all_sprites)

    def move(self, x, y):
        self.movex += x
        self.movey += y

    def update(self, *args):
        """Метод для прорисовки всех изменений спрайта девочки на файле"""
        if self.hp > 0:
            pygame.draw.rect(screen, (255, 0, 0), (50, 20, 30, 30), 0)
        if self.hp > 1:
            pygame.draw.rect(screen, (255, 0, 0), (85, 20, 30, 30), 0)
        if self.hp > 2:
            pygame.draw.rect(screen, (255, 0, 0), (120, 20, 30, 30), 0)
        if 200 < self.rect.x + self.movex < 910:
            self.rect.x += self.movex
        if 150 < self.rect.y + self.movey < 850:
            self.rect.y += self.movey
        if pygame.sprite.spritecollideany(self, bullets_skel):
            self.hp -= 1

    def change_frame(self):
        """Метод для изменения спрайта девочки во время ходьбы"""
        self.frame += 1
        self.image = Girl.girl_walk[self.frame % 2]

    def dance(self):
        """Метод для изменения спрайта девочки во время танца"""
        self.frame += 1
        self.image = Girl.girl_dance[self.frame % 2]

    def cry(self):
        """Метод для изменения спрайта девочки во время плача"""
        self.frame += 1
        self.image = Girl.girl_cry[self.frame % 2]


class BulletGirl(pygame.sprite.Sprite):
    """Класс пуль-сигарет девочки"""
    tile = load_image('tile_girl.png')

    def __init__(self, *group):
        """Инициализация спрайта пуль-сигарет девочки"""
        super().__init__(*group)
        self.image = BulletGirl.tile
        self.add(bullets_girl)
        self.rect = self.image.get_rect()
        self.rect.x = girl.rect.x + 40
        self.rect.y = girl.rect.y
        self.vel = 5

    def update(self, *args):
        """Прописано движение пуль и удаления их при пересечении границ экрана"""
        self.rect.y -= self.vel
        if self.rect.y < -50:
            self.kill()


class BasedSkeleton(pygame.sprite.Sprite):
    """Обычный скелет - класс"""
    sk_image = load_image('skeleton.png')

    def __init__(self, *group):
        """Иницаилизация обычного скелета"""
        super().__init__(*group)
        self.image = BasedSkeleton.sk_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(200, 800)
        while pygame.sprite.spritecollide(self, bad_guys, False):
            self.rect.x = random.randrange(200, 950)
        self.vel = 1
        bad_guys.add(self)

    def update(self, *event):
        """Движение скелета и удаление его если был контакт с пулей"""
        global CNT
        self.rect.y += self.vel
        if pygame.sprite.spritecollideany(self, bullets_girl):
            pygame.sprite.spritecollideany(self, bullets_girl).kill()
            self.kill()
            CNT += 10
        if self.rect.y > screen.get_height():
            CNT -= 20
            if CNT - 20 < 0:
                CNT = 0
            girl.hp -= 1
            self.kill()


class AdvancedSkeleton(pygame.sprite.Sprite):
    """Класс для продвинутого скелета"""
    sk_image_1 = load_image('skeleton_angry_1.png')
    sk_image_2 = load_image('skeleton_angry_2.png')

    def __init__(self, *group):
        """Инициализация продвинутого скелета"""
        super().__init__(*group)
        self.image = AdvancedSkeleton.sk_image_1
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(200, 800)
        while pygame.sprite.spritecollide(self, bad_guys, False):
            self.rect.x = random.randrange(200, 950)
            print(self.rect.x)
        ask_group.add(self)
        bad_guys.add(self)
        self.frame = 0
        self.hp = 2
        self.vel = 1

    def update(self, *args):
        """Движение скелета, изменение его при контакте с пулей и удаление его при втором контакте"""
        global CNT
        self.rect.y += self.vel
        if pygame.sprite.spritecollideany(self, bullets_girl):
            self.hp -= 1
            if self.hp == 0:
                CNT += 20
                self.kill()
            elif self.hp == 1:
                self.image = AdvancedSkeleton.sk_image_2
                pygame.sprite.spritecollideany(self, bullets_girl).kill()

        if self.rect.y > screen.get_height():
            CNT -= 20
            if CNT - 20 < 0:
                CNT = 0
            girl.hp -= 1
            self.kill()

    # def change_frame(self):
    #     self.frame += 1
    #     self.image = AdvancedSkeleton.sk_images[self.frame % 2]


class MusicButton(pygame.sprite.Sprite):
    """Кнопка музыки на главном экране"""
    img_on = load_image('mbutton_on.png')
    img_off = load_image('mbutton_off.png')

    def __init__(self, *group):
        """Инициализация кнопки"""
        super().__init__(*group)
        self.image = MusicButton.img_on
        self.rect = self.image.get_rect().move(1100, 800)
        self.is_playing = True

    def update(self, *args):
        """Изменение ее, если игрок не хочет ее слушать"""
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos) and self.is_playing:
            pygame.mixer.music.pause()
            self.image = MusicButton.img_off
            self.is_playing = False
        elif args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos) and not self.is_playing:
            pygame.mixer.music.unpause()
            self.image = MusicButton.img_on
            self.is_playing = True


class Border(pygame.sprite.Sprite):
    """Границы игровой области"""
    def __init__(self, x1):
        """Отрисовка границ"""
        super().__init__(all_sprites)
        self.add(borders)
        self.image = pygame.Surface([10, 900])
        self.image.fill((255, 255, 255))
        self.rect = pygame.Rect(x1, 0, 1, 900)


class Count(pygame.sprite.Sprite):
    """Счетчик смертей скелетов"""
    def __init__(self):
        """Отрисовка счетчика"""
        super().__init__(all_sprites)
        self.image = pygame.Surface([100, 300])
        self.font = pygame.font.Font(None, 50)
        text = self.font.render('0', True, (0, 255, 0))
        self.image.fill((28, 28, 28))
        self.image.blit(text, (0, 0))
        self.rect = pygame.Rect(1100, 15, 100, 300)

    def update(self, *args):
        """Изменение счета"""
        self.image.fill((28, 28, 28))
        text = self.font.render(str(CNT), True, (0, 255, 0))
        self.image.blit(text, (0, 0))


class EndGameLabelWin(pygame.sprite.Sprite):
    """Конечная надпись если игрок победил и прошел уровень до конца"""
    def __init__(self):
        """Инициализация надписи"""
        super().__init__(all_sprites)
        self.image = pygame.Surface([600, 150])
        self.font = pygame.font.Font(None, 72)
        self.rect = pygame.Rect(300, 0, 600, 200)

    def update(self, *args):
        """Появление текста ты умничка и вывод на экран"""
        text = self.font.render('Ты умничка <3', True, (0, 0, 0))
        self.image.fill((139, 0, 255))
        self.image.blit(text, (130, 50))


class EndGameLabelLoose(pygame.sprite.Sprite):
    """Надпись если игрок проиграл"""
    def __init__(self):
        """Инициализация надписи"""
        super().__init__(all_sprites)
        self.image = pygame.Surface([600, 150])
        self.font = pygame.font.Font(None, 72)
        self.rect = pygame.Rect(300, 0, 600, 200)

    def update(self, *args):
        """Появление текста плоха и вывод на экран"""
        text = self.font.render('Плоха', True, (0, 0, 0))
        self.image.fill((240, 0, 10))
        self.image.blit(text, (230, 50))


def read_skeleton(line):
    """Функция для чтения файла с уровня, появления скелетов и конца уровня"""
    global ask
    for elem in line:
        if elem == '.':
            sk = BasedSkeleton(all_sprites)
        elif elem == '1':
            win(1)
        elif elem == '2':
            win(2)
        elif elem == '3':
            win(3)
        elif elem == '#':
            ask = AdvancedSkeleton(all_sprites)


def win(level_passed):
    """Функция для вывода надписи победы на экран"""
    global ON_VICTORY_SCREEN
    global IN_GAME
    EndGameLabelWin()
    IN_GAME = False
    ON_VICTORY_SCREEN = True
    cur = con.cursor()
    print(level_passed)
    print(f'WHERE level = {level_passed}')
    cur.execute(f'''UPDATE WL
                SET passed = 1
                WHERE level = {level_passed}''')
    con.commit()
    print(cur.execute("""SELECT passed from WL""").fetchall())
    pygame.time.set_timer(girl_dance, 500)


def lost():
    """Функция для вывода надписи проигрыша на экран"""
    global ON_LOST_SCREEN
    global IN_GAME
    EndGameLabelLoose()
    for elem in bad_guys:
        elem.vel = 0
    IN_GAME = False
    ON_LOST_SCREEN = True
    pygame.time.set_timer(girl_dance, 500)


def load_level(level_number):
    """Функция для начала игры"""
    global ON_VICTORY_SCREEN
    global level_map
    global girl
    global IN_GAME
    global bad_guys
    global borders
    global CNT
    global bullets_girl
    global bullets_skel
    global spawnlane_index
    global ln
    global ask_group
    ln = level_number
    spawnlane_index = 0
    ON_VICTORY_SCREEN = False
    IN_GAME = True
    for sprite in all_sprites:
        sprite.kill()
    pygame.time.set_timer(SKELETON_SPAWN, 2000)
    pygame.mixer.music.stop()
    level_map = []
    girl = Girl(all_sprites)
    borders = pygame.sprite.Group()
    Border(200)
    Border(1000)
    Count()
    CNT = 0
    bullets_girl = pygame.sprite.Group()
    bullets_skel = pygame.sprite.Group()
    bad_guys = pygame.sprite.Group()
    pygame.time.set_timer(girl_frame_change, 500)
    pygame.time.set_timer(girl_hit, 200)
    ask_group = pygame.sprite.Group()
    if level_number > 1:
        pygame.time.set_timer(skeleton_shoot, 1500)
        pygame.time.set_timer(skeleton_change_frame, 750)
    with open(f'data/level{level_number}.txt', 'r') as level:
        level_map = [line.strip() for line in level]
        print(level_map)
    print('ye')


def main_menu():
    """Функция для отображения главного меню"""
    for elem in all_sprites:
        elem.kill()
    global ON_LOST_SCREEN
    global ON_VICTORY_SCREEN
    global background
    global logo
    global btn1
    global btn2
    global btn3
    global btnm
    ON_LOST_SCREEN = False
    ON_VICTORY_SCREEN = False
    screen.fill((28, 28, 28))
    pygame.mixer.stop()
    pygame.mixer.music.load("data/main_menu_theme.mp3")
    pygame.mixer.music.play(-1, 0.0)
    background = Background(all_sprites)
    logo = Logo(all_sprites)
    btn1 = ButtonLevel1(all_sprites)
    btn2 = ButtonLevel2(all_sprites)
    btn3 = ButtonLevel3(all_sprites)
    btnm = MusicButton(all_sprites)

"""создание главной группы спрайтов и вывод главного меню"""
all_sprites = pygame.sprite.Group()
main_menu()

if __name__ == '__main__':
    """Главный игровой цикл"""
    global level_map
    pygame.init()
    pygame.display.set_caption('BulletHell')
    fps = 60  # количество кадров в секунду
    clock = pygame.time.Clock()
    running = True
    ticks = 0
    speed = 7
    spawnlane_index = 0
    IN_GAME = False
    dance_limit = 0
    ON_VICTORY_SCREEN = False
    ON_LOST_SCREEN = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == SKELETON_SPAWN and IN_GAME:
                read_skeleton(level_map[spawnlane_index])
                if spawnlane_index + 1 >= len(level_map):
                    spawnlane_index = 0
                    IN_GAME = False
                else:
                    print(level_map[spawnlane_index])
                    spawnlane_index += 1

            if event.type == pygame.KEYDOWN and IN_GAME:
                if event.key == pygame.K_LEFT:
                    girl.move(-speed, 0)
                if event.key == pygame.K_RIGHT:
                    girl.move(speed, 0)
                if event.key == pygame.K_UP:
                    girl.move(0, -speed)
                if event.key == pygame.K_DOWN:
                    girl.move(0, speed)
                if event.key == pygame.K_SPACE:
                    girl.shoot()
            if event.type == pygame.KEYUP and IN_GAME:
                if event.key == pygame.K_LEFT:
                    girl.move(speed, 0)
                if event.key == pygame.K_RIGHT:
                    girl.move(-speed, 0)
                if event.key == pygame.K_UP:
                    girl.move(0, speed)
                if event.key == pygame.K_DOWN:
                    girl.move(0, -speed)
            if event.type == girl_frame_change and IN_GAME:
                girl.change_frame()
            # if event.type == skeleton_shoot and IN_GAME and ln > 1:
            #     for elem in ask_group:
            #         elem.shoot()
            # if event.type == skeleton_change_frame and IN_GAME and ln > 1:
            #     for elem in ask_group:
            #         elem.change_frame()
            if event.type == girl_hit and IN_GAME:
                girl.hit()
            if event.type == girl_dance and ON_VICTORY_SCREEN and dance_limit <= 10:
                girl.dance()
                dance_limit += 1
            elif event.type == girl_dance and ON_LOST_SCREEN and dance_limit <= 10:
                girl.cry()
                dance_limit += 1
            elif dance_limit > 10:
                girl.kill()
                main_menu()
                dance_limit = 0
            all_sprites.update(event)
        screen.fill((28, 28, 28))
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(fps)
        ticks += 1

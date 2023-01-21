import os
import random
import sqlite3
import sys

import pygame

size = width, height = 1200, 900
screen = pygame.display.set_mode(size)

pygame.init()
level1_available = True
level2_available = False
level3_available = False
SKELETON_SPAWN = pygame.USEREVENT + 1
girl_frame_change = pygame.USEREVENT + 2
girl_hit = pygame.USEREVENT + 3

bad_guys = pygame.sprite.Group()

con = sqlite3.connect('WinsAndLoses')


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class ButtonLevel1(pygame.sprite.Sprite):
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
    cur = con.cursor()
    level2_available = cur.execute('SELECT passed FROM WL '
                                   'WHERE level like "1"')
    if level2_available:
        image = load_image('lv2_en.png')
    else:
        image = load_image('lv2_dis.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = ButtonLevel2.image
        self.rect = self.image.get_rect()
        self.rect.x = 90
        self.rect.y = 450
        self.pos = (200, 100)

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos) and level2_available:
            load_level(2)


class ButtonLevel3(pygame.sprite.Sprite):
    cur = con.cursor()
    level3_available = cur.execute('SELECT passed FROM WL '
                                   'WHERE level like "2"')
    if level2_available:
        image = load_image('lv3_en.png')
    else:
        image = load_image('lv3_dis.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = ButtonLevel3.image
        self.rect = self.image.get_rect()
        self.rect.x = 90
        self.rect.y = 550
        self.pos = (200, 100)

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos) and level3_available:
            load_level(3)


class Background(pygame.sprite.Sprite):
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
    logo = load_image('logo.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Logo.logo
        self.rect = self.image.get_rect()
        self.rect.x = 250
        self.rect.y = -50


class Girl(pygame.sprite.Sprite):
    girl_stands = load_image('girl_idle.png')
    girl_hurt = load_image('girl_hurt.png')
    girl_walk = [load_image('girl_walk_1.png'), load_image('girl_walk_2.png')]

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Girl.girl_stands
        self.speed = 10
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
        now = pygame.time.get_ticks()
        if pygame.sprite.spritecollideany(self, bad_guys):
            if now - self.last_hurt >= self.cooldown_hurt:
                self.last_hurt = now
                self.hp -= 1
                self.image = Girl.girl_hurt

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last >= self.cooldown:
            self.last = now
            bullet = BulletGirl(all_sprites)
        print(1)

    def move(self, x, y):
        self.movex += x
        self.movey += y

    def update(self, *args):
        if self.hp > 0:
            pygame.draw.rect(screen, (255, 0, 0), (50, 20, 30, 30), 0)
        if self.hp > 1:
            pygame.draw.rect(screen, (255, 0, 0), (85, 20, 30, 30), 0)
        if self.hp > 2:
            pygame.draw.rect(screen, (255, 0, 0), (120, 20, 30, 30), 0)
        if 200 < self.rect.x + self.movex < 910:
            self.rect.x += self.movex
        if -50 < self.rect.y + self.movey < 850:
            self.rect.y += self.movey

    def change_frame(self):
        self.frame += 1
        if self.frame > 1:
            self.frame = 0
        self.image = Girl.girl_walk[self.frame]


class BulletGirl(pygame.sprite.Sprite):
    tile = load_image('tile_girl.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = BulletGirl.tile
        self.add(bullets_girl)
        self.rect = self.image.get_rect()
        self.rect.x = girl.rect.x + 40
        self.rect.y = girl.rect.y
        self.vel = 5

    def update(self, *args):
        self.rect.y -= self.vel
        if self.rect.y < -50:
            self.kill()
        # if pygame.sprite.spritecollideany(self, bad_guys):
        #     self.kill()


class Skeleton(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)

    def hurt(self):
        self.kill()


class BasedSkeleton(Skeleton):
    sk_image = load_image('skeleton.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = BasedSkeleton.sk_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(200, 800)
        while pygame.sprite.spritecollide(self, bad_guys, False):
            self.rect.x = random.randrange(200, 970)
        bad_guys.add(self)

    def update(self, *event):
        global CNT
        self.rect.y += 1
        if pygame.sprite.spritecollideany(self, bullets_girl):
            self.kill()
            CNT += 1
        if self.rect.y > screen.get_height():
            self.kill()


class MusicButton(pygame.sprite.Sprite):
    img_on = load_image('mbutton_on.png')
    img_off = load_image('mbutton_off.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = MusicButton.img_on
        self.rect = self.image.get_rect().move(1100, 800)
        self.is_playing = True

    def update(self, *args):
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
    def __init__(self, x1):
        super().__init__(all_sprites)
        self.add(borders)
        self.image = pygame.Surface([10, 900])
        self.image.fill((255, 255, 255))
        self.rect = pygame.Rect(x1, 0, 1, 900)


class Count(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.Surface([100, 300])
        self.font = pygame.font.Font(None, 50)
        text = self.font.render('0', True, (0, 255, 0))
        self.image.fill((28, 28, 28))
        self.image.blit(text, (0, 0))
        self.rect = pygame.Rect(1100, 15, 100, 300)

    def update(self, *args):
        self.image.fill((28, 28, 28))
        text = self.font.render(str(CNT), True, (0, 255, 0))
        self.image.blit(text, (0, 0))


# class EndGameLabel(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__(all_sprites)
#


def read_skeleton(line):
    print(line)
    for elem in line:
        print(elem)
        if elem == '.':
            sk = BasedSkeleton(all_sprites)
        elif elem == '*1':
            end_game(1)
        elif elem == '#':
            pass


def end_game(level_passed):
    cur = con.cursor()
    cur.execute('UPDATE WL'
                'SET passed True'
                f'WHERE level = {level_passed}')


def lost():
    pass


def load_level(level_number):
    global level_map
    global girl
    global IN_GAME
    global bad_guys
    global borders
    global CNT
    global bullets_girl
    global bullets_skel
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
    with open(f'data/level{level_number}.txt', 'r') as level:
        level_map = [line.strip() for line in level]
        print(level_map)


def main_menu():
    global background
    global logo
    global btn1
    global btn2
    global btn3
    global btnm
    pygame.mixer.stop()
    pygame.mixer.music.load("data/main_menu_theme.mp3")
    pygame.mixer.music.play(-1, 0.0)
    background = Background(all_sprites)
    logo = Logo(all_sprites)
    btn1 = ButtonLevel1(all_sprites)
    btn2 = ButtonLevel2(all_sprites)
    btn3 = ButtonLevel3(all_sprites)
    btnm = MusicButton(all_sprites)


all_sprites = pygame.sprite.Group()
main_menu()

if __name__ == '__main__':
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
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == SKELETON_SPAWN and IN_GAME:
                read_skeleton(level_map[spawnlane_index])
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
            if event.type == girl_hit and IN_GAME:
                girl.hit()
            all_sprites.update(event)
        screen.fill((28, 28, 28))
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(fps)
        ticks += 1

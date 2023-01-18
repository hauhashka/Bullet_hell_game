import os
import random
import sys

import pygame

size = width, height = 1200, 900
screen = pygame.display.set_mode(size)

pygame.init()
level1_available = True
level2_available = False
level3_available = False

level_map = []

SKELETON_SPAWN = pygame.USEREVENT + 1
girl_frame_change = pygame.USEREVENT + 2


bad_guys = pygame.sprite.Group


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class ButtonLevel1(pygame.sprite.Sprite):
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


def load_level(level_number):
    global level_map
    global girl
    level_map = []
    for sprite in all_sprites:
        sprite.kill()
    girl = Girl(all_sprites)
    pygame.time.set_timer(girl_frame_change, 500)
    with open(f'data/level{level_number}.txt', 'r') as level:
        level_map = [line.strip() for line in level]
        print(level_map)


class Girl(pygame.sprite.Sprite):
    girl_stands = load_image('girl_idle.png')
    girl_hurt = load_image('girl_hurt.png')
    girl_walk = [load_image('girl_walk_1.png'), load_image('girl_walk_2.png')]

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Girl.girl_stands
        self.speed = 10
        self.rect = self.image.get_rect().move(400, 500)
        self.movex = 0
        self.movey = 0
        self.hp = 3
        self.frame = 0

    def hurt(self):
        self.image = Girl.girl_hurt

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
        self.rect.x += self.movex
        self.rect.y += self.movey

    def change_frame(self):
        self.frame += 1
        if self.frame > 1:
            self.frame = 0
        self.image = Girl.girl_walk[self.frame]


class Skeleton(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.pos = (random.randint(320, 880), 20)

    def hurt(self):
        self.kill()


class BasedSkeleton(Skeleton):
    sk_image = load_image('skeleton.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = BasedSkeleton.sk_image
        self.rect = self.image.get_rect().move((random.randint(0, 680), -200))
        bad_guys.add(self)


    def update(self, *event):
        self.rect.y += 1


def read_skeleton(line):
    print(line)
    for elem in line:
        print(elem)
        if elem == '.':
            sk = BasedSkeleton(all_sprites)
        elif elem == '#':
            pass


all_sprites = pygame.sprite.Group()
background = Background(all_sprites)
logo = Logo(all_sprites)
btn1 = ButtonLevel1(all_sprites)
btn2 = ButtonLevel2(all_sprites)
btn3 = ButtonLevel3(all_sprites)
pygame.time.set_timer(SKELETON_SPAWN, random.randint(1000, 4000))
if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('BulletHell')

    fps = 60  # количество кадров в секунду
    clock = pygame.time.Clock()
    running = True
    ticks = 0
    speed = 10
    spawnlane_index = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == SKELETON_SPAWN:
                read_skeleton(level_map[spawnlane_index])
                spawnlane_index += 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    girl.move(-speed, 0)
                if event.key == pygame.K_RIGHT:
                    girl.move(speed, 0)
                if event.key == pygame.K_UP:
                    girl.move(0, -speed)
                if event.key == pygame.K_DOWN:
                    girl.move(0, speed)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    girl.move(speed, 0)
                if event.key == pygame.K_RIGHT:
                    girl.move(-speed, 0)
                if event.key == pygame.K_UP:
                    girl.move(0, speed)
                if event.key == pygame.K_DOWN:
                    girl.move(0, -speed)
            if event.type == girl_frame_change:
                girl.change_frame()
            all_sprites.update(event)
        screen.fill((28, 28, 28))
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(fps)
        ticks += 1

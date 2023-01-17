import os
import sys

import pygame

size = width, height = 1200, 900
screen = pygame.display.set_mode(size)

pygame.init()
MainMenuSprites = pygame.sprite.Group()
level1_available = True
level2_available = False
level3_available = False


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


'''def draw_button(y_shift, text, enabled=False):
    if enabled:
        color = pygame.Color(50, 150, 50)
        # рисуем "тень"
        pygame.draw.rect(screen, color,
                         (90, 400 + y_shift, 200, 70), 0)
        hsv = color.hsva
        # увеличиваем параметр Value, который влияет на яркость
        color.hsva = (hsv[0], hsv[1], hsv[2] + 30, hsv[3])
        # рисуем сам объект
        pygame.draw.rect(screen, color, (80, 390 + y_shift, 200, 70), 0)
        font = pygame.font.Font(None, 50)
        label = font.render(text, True, (28, 28, 28))
        label_x = 90
        label_y = 400 + y_shift
        screen.blit(label, (label_x, label_y))
    else:
        color = pygame.Color(50, 150, 50)
        # рисуем "тень"
        pygame.draw.rect(screen, color,
                         (90, 400 + y_shift, 200, 70), 0)
        font = pygame.font.Font(None, 50)
        label = font.render(text, True, (30, 30, 30))
        label_x = 100
        label_y = 410 + y_shift
        screen.blit(label, (label_x, label_y))'''


def start_screen():
    btn1 = ButtonLevel1(all_sprites)
    btn2 = ButtonLevel2(all_sprites)
    btn3 = ButtonLevel3(all_sprites)


def load_level():
    for sprite in MainMenuSprites:
        sprite.kill()
        screen.fill((0, 0, 0))


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
        MainMenuSprites.add(self)

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos) and level1_available:
            load_level()


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
        MainMenuSprites.add(self)

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos) and level2_available:
            load_level()


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
        MainMenuSprites.add(self)

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos) and level3_available:
            load_level()


class Background(pygame.sprite.Sprite):
    girl = load_image('girl_1.1.jpg')
    girl = pygame.transform.scale(girl, (600, 900))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Background.girl
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 0
        MainMenuSprites.add(self)


class Logo(pygame.sprite.Sprite):
    logo = load_image('logo.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Logo.logo
        self.rect = self.image.get_rect()
        self.rect.x = 250
        self.rect.y = -50
        MainMenuSprites.add(self)


all_sprites = pygame.sprite.Group()
boackground = Background(all_sprites)
logo = Logo(all_sprites)
start_screen()
if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('BulletHell')

    fps = 50  # количество кадров в секунду
    clock = pygame.time.Clock()
    running = True
    ticks = 0
    speed = 10
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            all_sprites.update(event)
        pygame.display.flip()
        all_sprites.draw(screen)
        clock.tick(fps)
        ticks += 1

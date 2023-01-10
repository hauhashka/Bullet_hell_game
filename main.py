import os
import sys

import pygame

size = width, height = 1200, 900
screen = pygame.display.set_mode(size)

pygame.init()
MainMenuSprites = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def draw_button(y_shift, text, enabled=False):
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
        screen.blit(label, (label_x, label_y))


def start_screen():
    draw_button(0, 'Уровень 1', enabled=True)
    draw_button(100, 'Уровень 2')
    draw_button(200, 'Уровень 3')


def load_level():
    for sprite in MainMenuSprites:
        sprite.kill()
        screen.fill((0, 0, 0))


'''class Button(pygame.sprite.Sprite):
    def __init__(self, *group, y_shift, text, enabled=False):
        super().__init__(*group)
        color = pygame.Color(50, 150, 50)
        if enabled:
            pygame.draw.rect(screen, color,
                             (90, 400 + y_shift, 200, 70), 0)
            hsv = color.hsva
            # увеличиваем параметр Value, который влияет на яркость
            color.hsva = (hsv[0], hsv[1], hsv[2] + 30, hsv[3])
            self.image = pygame.Surface(80, 390 + y_shift, 200, 70)
            font = pygame.font.Font(None, 50)
            label = font.render(text, True, (28, 28, 28))
            label_x = 90
            label_y = 400 + y_shift
            screen.blit(label, (label_x, label_y))
        else:
            self.image = pygame.Surface(90, 400 + y_shift, 200, 70)
            pygame.draw.rect(screen, color,
                             (90, 400 + y_shift, 200, 70), 0)
            font = pygame.font.Font(None, 50)
            label = font.render(text, True, (30, 30, 30))
            label_x = 100
            label_y = 410 + y_shift
            screen.blit(label, (label_x, label_y))
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 0
        MainMenuSprites.add(self)'''


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
        pygame.display.flip()
        all_sprites.draw(screen)
        clock.tick(fps)
        ticks += 1

import pygame
import os


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Background(pygame.sprite.Sprite):
    girl = load_image('girl_2.jpg')
    girl = pygame.transform.scale(girl, (600, 900))


    def __init__(self, *group):
        super().__init__(*group)
        self.image = Background.girl
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


all_sprites = pygame.sprite.Group()
boackground = Background(all_sprites)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('BulletHell')
    size = width, height = 600, 900
    screen = pygame.display.set_mode(size)
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


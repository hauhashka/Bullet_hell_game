import pygame

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

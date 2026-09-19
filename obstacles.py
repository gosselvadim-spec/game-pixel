import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, IMG_STONE, IMG_FIRE, IMG_SWORD


class ObstacleSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Obstacle(ObstacleSprite):
    def __init__(self, x, y, width, height, speed, filename):
        super().__init__(x, y, filename)
        self.width = width
        self.height = height
        self.speed = speed
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
        self.original_speed = speed

    def move(self, slow_motion=False):
        if slow_motion:
            self.rect.y += self.speed * 0.5
        else:
            self.rect.y += self.speed

        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = random.randint(-200, -50)
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.width)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Stone(Obstacle):
    def __init__(self, x, y, speed):
        super().__init__(x, y, 60, 65, speed, IMG_STONE)


class Fire(Obstacle):
    def __init__(self, x, y, speed):
        super().__init__(x, y, 100, 100, speed, IMG_FIRE)


class Sword(Obstacle):
    def __init__(self, x, y, speed):
        super().__init__(x, y, 40, 110, speed, IMG_SWORD)

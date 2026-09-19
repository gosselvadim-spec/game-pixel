import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.speed = 3

    def update(self):
        self.y += self.speed
        self.rect.y = self.y
        if self.y > SCREEN_HEIGHT:
            return True
        return False

    def draw(self, screen):
        center_x = int(self.x + self.width // 2)
        center_y = int(self.y + self.height // 2)
        pygame.draw.circle(screen, (255, 215, 0), (center_x, center_y), 15)
        pygame.draw.circle(screen, (255, 165, 0), (center_x, center_y), 12, 2)
        font = pygame.font.Font(None, 20)
        text = font.render("$", True, (255, 255, 255))
        screen.blit(text, (center_x - 5, center_y - 8))


class SlowBonus:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.animation_frame = 0

    def update(self):
        self.y += 2
        self.rect.y = self.y
        self.animation_frame += 0.1
        if self.y > SCREEN_HEIGHT:
            return True
        return False

    def draw(self, screen):
        center_x = int(self.x + self.width // 2)
        center_y = int(self.y + self.height // 2)
        pygame.draw.circle(screen, (0, 150, 255), (center_x, center_y), 20)
        pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), 18, 2)
        font = pygame.font.Font(None, 25)
        text = font.render("B", True, (255, 255, 255))
        screen.blit(text, (center_x - 8, center_y - 12))

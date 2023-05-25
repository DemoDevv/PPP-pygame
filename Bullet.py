import pygame
import math

from utils.Vec2d import Vec2d


class Bullet(pygame.sprite.Sprite):

    def __init__(self, game, speed: int, damage: int, init_pos: tuple, angle: float, taille_ratio: int = 1):
        pygame.sprite.Sprite.__init__(self)

        self.game = game
        self.speed = speed
        self.damage = damage

        self.angle = angle
        self.angle_rad = angle * (math.pi / 180)

        self.pos = Vec2d(init_pos)

        self.rect_height = 10 * taille_ratio
        self.rect_width = 3 * taille_ratio
        self.image = pygame.Surface((self.rect_width, self.rect_height), pygame.SRCALPHA)
        self.image.fill((255, 0, 0))

        self.image = pygame.transform.rotate(self.image, self.angle)

        self.rect = self.image.get_rect()
        self.rect.center = self.pos.to_tuple()

    def update(self, dt):
        deplacement = Vec2d((-self.speed * dt, -self.speed * dt))
        magnitude = deplacement.magnitude()
        verticale_offset = magnitude * math.sin(self.angle_rad)
        horizontal_offset = magnitude * math.cos(self.angle_rad)
        self.pos.y += horizontal_offset
        self.pos.x += verticale_offset
        self.rect.center = self.pos.to_tuple()

        if not pygame.Rect.colliderect(self.rect, self.game.screen.get_rect()):
            self.kill()

import pygame

from utils.Vec2d import Vec2d


class Bullet(pygame.sprite.Sprite):

    def __init__(self, game, speed: int, damage: int, init_pos: tuple):
        pygame.sprite.Sprite.__init__(self)

        self.game = game
        self.speed = speed
        self.damage = damage

        self.pos = Vec2d(init_pos)

        self.rect_height = 10
        self.rect_width = 3
        self.image = pygame.Surface((self.rect_width, self.rect_height))
        self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.center = self.pos.to_tuple()

    def update(self, dt):
        self.pos.y -= self.speed * dt
        self.rect.center = self.pos.to_tuple()

        if self.pos.y < 0:
            self.kill()

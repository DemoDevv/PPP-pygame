import pygame
import math

from utils.Vec2d import Vec2d


class Competence(pygame.sprite.Sprite):

    def __init__(self, game, name, init_pos: tuple):
        pygame.sprite.Sprite.__init__(self)

        self.game = game

        self.name = name

        self.pos = Vec2d(init_pos)

        self.rect_height = 7
        self.rect_width = 7
        self.image = pygame.Surface((self.rect_width, self.rect_height), pygame.SRCALPHA)
        self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.center = self.pos.to_tuple()

    def update(self, dt):
        deplacement = Vec2d((0, 100 * dt))
        self.pos.y += deplacement.y
        self.pos.x += deplacement.x
        self.rect.center = self.pos.to_tuple()

        if not pygame.Rect.colliderect(self.rect, self.game.screen.get_rect()):
            self.kill()
        elif self.game.main_player.rect.colliderect(self.rect):
            self.game.main_player.add_competence(self)
            self.kill()

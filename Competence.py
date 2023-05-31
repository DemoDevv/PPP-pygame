import pygame
import math

from utils.Vec2d import Vec2d


class Competence(pygame.sprite.Sprite):

    def __init__(self, game, name, init_pos: tuple):
        pygame.sprite.Sprite.__init__(self)

        self.game = game

        self.name = name

        self.pos = Vec2d(init_pos)

        self.rect_height = 30
        self.rect_width = 30
        self.image = pygame.image.load("assets/exp_boost.png")
        self.image = pygame.transform.scale(self.image, (self.rect_width, self.rect_height))

        self.rect = self.image.get_rect()
        self.rect.center = self.pos.to_tuple()

    def update(self, dt):
        deplacement = Vec2d((0, 80 * dt))
        self.pos.y += deplacement.y
        self.pos.x += deplacement.x
        self.rect.center = self.pos.to_tuple()

        if not pygame.Rect.colliderect(self.rect, self.game.screen.get_rect()):
            self.kill()
        elif self.game.main_player.rect.colliderect(self.rect):
            self.game.main_player.add_competence(self)
            self.kill()

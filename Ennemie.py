import pygame

from utils.Vec2d import Vec2d
from Bullet import Bullet
from Competence import Competence

import random


class Ennemie(pygame.sprite.Sprite):

    def __init__(self, game, path_image: str, speed: int, init_pos: tuple, competence, init_life: int = 100):
        pygame.sprite.Sprite.__init__(self)

        self.game = game

        self.speed = speed
        self.life = init_life

        self.interval_shoot = 2.0
        self.offset_shoot = random.uniform(0.0, self.interval_shoot / 2)
        self.shoot_time = self.offset_shoot

        self.life_bar_height = 6
        self.surface_life = pygame.Surface((self.life, self.life_bar_height))
        self.rect_life = self.surface_life.get_rect()
        self.rect_life.center = (init_pos[0], init_pos[1] + 55)
        self.surface_life.fill((255, 0, 0))
        self.surface_life.fill((0, 255, 0), (0, 0, self.life, self.life_bar_height))

        self.pos = Vec2d(init_pos)
        self.velocity = Vec2d((0, self.speed))

        self.image = pygame.image.load(path_image)
        self.rect_height = 85
        self.rect_width = 85
        self.image = pygame.transform.scale(self.image, (self.rect_width, self.rect_height))
        self.image = pygame.transform.rotate(self.image, 180)

        self.rect = self.image.get_rect()
        self.rect.center = (self.pos.x, self.pos.y)
        
        self.competence = competence

    def update(self, dt):
        self.idle_movement(dt)

    def draw_health_bar(self):
        self.rect_life.center = (self.pos.x, self.pos.y + 55)
        self.surface_life.fill((255, 0, 0))
        self.surface_life.fill((0, 255, 0), (0, 0, self.life, self.life_bar_height))
        self.game.screen.blit(self.surface_life, self.rect_life)

    def idle_movement(self, dt):
        self.pos.y += self.velocity.y

        if self.pos.y + self.rect_width / 2 >= self.game.SCREEN_HEIGHT: # TODO si on touche le bas de l'écran c'est game over
            self.velocity.y = 0.0

        self.rect.center = (self.pos.x, self.pos.y)
        self.draw_health_bar()

        self.shoot_time += dt
        if self.shoot_time >= self.interval_shoot:
            self.shoot()
            self.shoot_time = self.offset_shoot

    def shoot(self):
        """ tire un projectile """
        self.game.bullet_group_ennemy.add(Bullet(self.game, 0.4 * self.game.SCREEN_WIDTH, 10, (self.pos.to_tuple()[0], self.rect.y + self.rect_height), 0))

    def take_damage(self, damage: int):
        self.life -= damage
        if self.life <= 0:
            if self.competence is not None:
                self.game.competence_group.add(Competence(self.game, self.competence, self.pos.to_tuple()))
            self.kill()


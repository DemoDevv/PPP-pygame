import pygame

from utils.Vec2d import Vec2d
from utils.animation import animate_position_2d, ease_out_back, easeInOutExpo

from enum import Enum


class AnimationState(Enum):
    Idle = 0
    FromBack = 1
    ToBack = 2
    ToTop = 3


class Vaisseau(pygame.sprite.Sprite):

    def __init__(self, game, path_image: str, speed: int, init_pos: tuple, init_life: int = 100):
        pygame.sprite.Sprite.__init__(self)

        self.game = game

        self.speed = speed
        self.life = init_life

        self.life_bar_height = 6
        self.surface_life = pygame.Surface((self.life, self.life_bar_height))
        self.rect_life = self.surface_life.get_rect()
        self.rect_life.center = (init_pos[0], init_pos[1] + 55)
        self.surface_life.fill((255, 0, 0))
        self.surface_life.fill((0, 255, 0), (0, 0, self.life, self.life_bar_height))

        self.pos = Vec2d(init_pos)
        self.pos_start_animation = Vec2d((self.game.SCREEN_WIDTH / 2, self.game.SCREEN_HEIGHT + 60))
        self.pos_during_animation = self.pos_start_animation

        self.velocity = Vec2d((0, 0))

        self.image = pygame.image.load(path_image)
        self.rect_height = 100
        self.rect_width = 100
        self.image = pygame.transform.scale(self.image, (self.rect_width, self.rect_height))

        self.rect = self.image.get_rect()
        self.rect.center = (self.pos_during_animation.x, self.pos_during_animation.y)

        self.dx = 0.0

        self.current_animation_state = AnimationState.FromBack
        self.animation_time = 0.0
        self.animation = {
            AnimationState.Idle: self.idle_movement,
            AnimationState.FromBack: self.from_back_movement, 
            AnimationState.ToBack: self.to_back_movement, 
            AnimationState.ToTop: self.to_top_movement
        }

    def _finish_animation(self):
        if self.animation_time >= 1.:
            self.current_animation_state = AnimationState.Idle
            self.dx = 0.0
            self.animation_time = 0.0

    def _perform_animation(self, dt, animation_type):

        if animation_type == AnimationState.FromBack:
            self.animation_time += dt

            self.pos_during_animation = Vec2d(animate_position_2d(ease_out_back, self.pos_start_animation.to_tuple(), self.pos.to_tuple(), self.animation_time))
            self.rect.center = self.pos_during_animation.to_tuple()

            print(self.animation_time)
            self._finish_animation()

        elif animation_type == AnimationState.ToBack:
            pass # utiliser cette animation lors du changement de joueur

        elif animation_type == AnimationState.ToTop:
            self.animation_time += dt

            self.pos_during_animation = Vec2d(animate_position_2d(easeInOutExpo, self.pos.to_tuple(), (self.pos.x, -150), self.animation_time))
            self.rect.center = self.pos_during_animation.to_tuple()

            self._finish_animation()


    def update(self, dt):
        self.animation[self.current_animation_state](dt)

    def draw_health_bar(self):
        self.rect_life.center = (self.pos.x, self.pos.y + 55)
        self.surface_life.fill((0, 255, 0), (0, 0, self.life, self.life_bar_height))
        self.game.screen.blit(self.surface_life, self.rect_life)

    def idle_movement(self, dt):
        if pygame.key.get_pressed()[self.game.actions['left']]:
            self.dx = -self.speed
        if pygame.key.get_pressed()[self.game.actions['right']]:
            self.dx = self.speed

        self.velocity.x += self.dx * dt
        self.velocity.x *= 0.9

        self.pos.x += self.velocity.x

        if self.pos.x - self.rect_width / 2 <= 0:
            self.pos.x = self.rect_width / 2
            self.velocity.x = 0.0

        if self.pos.x + self.rect_width / 2 >= self.game.SCREEN_WIDTH:
            self.pos.x = self.game.SCREEN_WIDTH - self.rect_width / 2
            self.velocity.y = 0.0

        self.rect.center = (self.pos.x, self.pos.y)
        self.draw_health_bar()

    def from_back_movement(self, dt):
        self._perform_animation(dt, AnimationState.FromBack)

    def to_back_movement(self, dt):
        self._perform_animation(dt, AnimationState.ToBack)

    def to_top_movement(self, dt):
        self._perform_animation(dt, AnimationState.ToTop)

    def shoot(self):
        """ tire un projectile """
        print("piouuu")
        self.current_animation_state = AnimationState.ToTop


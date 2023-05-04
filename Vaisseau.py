import pygame

from utils.Vec2d import Vec2d
from utils.animation import lerp_position_2d, animate_position_2d, ease_out_back


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

    def perform_animation(self, dt, animation_type):
        current_ingame_state = self.game.get_current_main_state().get_current_ingame_state()

        if animation_type == current_ingame_state.AnimationState.FromBack:
            current_ingame_state.animation_time += dt

            self.pos_during_animation = Vec2d(animate_position_2d(ease_out_back, self.pos_start_animation.to_tuple(), self.pos.to_tuple(), current_ingame_state.animation_time))
            self.rect.center = self.pos_during_animation.to_tuple()

            if self.pos_during_animation.y <= self.pos.y:
                current_ingame_state.animation_state = current_ingame_state.AnimationState.Idle
                current_ingame_state.animation_time = 0.0

        elif animation_type == current_ingame_state.AnimationState.ToBack:
            pass # utiliser cette animation lors du changement de joueur

    def update(self, dt):
        if pygame.key.get_pressed()[self.game.actions['left']]:
            self.dx = -self.speed
        elif pygame.key.get_pressed()[self.game.actions['right']]:
            self.dx = self.speed

        self.velocity.x += self.dx * dt
        self.velocity.x *= 0.9

        self.pos.x += self.velocity.x

        self.rect_life.center = (self.pos.x, self.pos.y + 55)
        self.surface_life.fill((0, 255, 0), (0, 0, self.life, self.life_bar_height))

        if self.pos.x - self.rect_width / 2 <= 0:
            self.pos.x = self.rect_width / 2
            self.velocity.x = 0.0

        if self.pos.x + self.rect_width / 2 >= self.game.SCREEN_WIDTH:
            self.pos.x = self.game.SCREEN_WIDTH - self.rect_width / 2
            self.velocity.y = 0.0

        self.rect.center = (self.pos.x, self.pos.y)
        self.game.screen.blit(self.surface_life, self.rect_life)

    def shoot(self):
        """ tire un projectile """
        print("piouuu")

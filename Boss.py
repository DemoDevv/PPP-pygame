import pygame
import math
import random

from utils.Font import get_font
from utils.Vec2d import Vec2d
from utils.animation import animate_position_2d, ease_out_back, linear
from Bullet import Bullet

from enum import Enum


class AnimationState(Enum):
    Idle = 0
    FromTop = 1
    Custom = 2


class BossState(Enum):
    """ Etat du boss """
    Idle = 0
    Attack = 1


class BossAttack(Enum):
    """ Attaque du boss """
    def __init__(self, duration, is_invicible, shoot_interval, start_pos: tuple, end_pos: tuple, movement_functions, *args) -> None:
        super().__init__()
        self.time = 0.0
        self.shoot_interval_base = shoot_interval
        self.shoot_interval = shoot_interval
        self.is_invicible = is_invicible
        self.duration = duration
        anchors = list(map(Vec2d, args)) if args else []
        self.anchor_index = 0
        self.anchors = [Vec2d(start_pos)] + anchors + [Vec2d(end_pos)] if args else [Vec2d(start_pos), Vec2d(end_pos)]
        self.movement_functions = movement_functions

    Laser = (6.0, True, 0.0, (0, 0), (0, 0), [ease_out_back, linear, ease_out_back], (200, 70), (-200, 70))
    Raining = (5.0, False, 0.5, (0, 0), (0, 0), [])
    Rocket = (1.0, False, 0.3, (0, 0), (0, 0), [])


class Boss(pygame.sprite.Sprite):

    def __init__(self, game, path_image: str, speed: int, name: str, init_pos: tuple, init_life: int = 600):
        pygame.sprite.Sprite.__init__(self)

        self.game = game

        self.name = name
        self.speed = speed
        self.life = init_life

        self.interval_attack = 5.0

        self.is_invincible = True

        self.life_bar_height = 22
        self.surface_life = pygame.Surface((self.life, self.life_bar_height))
        self.rect_life = self.surface_life.get_rect()
        self.rect_life.center = (game.SCREEN_WIDTH / 2, 50)
        self.surface_life.fill((23, 23, 23))
        self.surface_life.fill((255, 0, 0), (0, 0, self.life, self.life_bar_height))

        self.rect_height = 300
        self.rect_width = 500

        self.pos = Vec2d(init_pos)
        self.pos_start_animation = Vec2d((self.game.SCREEN_WIDTH / 2, -self.rect_height - 60))
        self.pos_during_animation = self.pos_start_animation

        self.velocity = Vec2d((0, 0))

        # self.image = pygame.image.load(path_image)
        # self.image = pygame.transform.scale(self.image, (self.rect_width, self.rect_height))

        self.image = pygame.Surface((self.rect_width, self.rect_height), pygame.SRCALPHA) # TODO faut remplacer par l'image
        self.image.fill((255, 255, 255))

        self.rect = self.image.get_rect()
        self.rect.center = (self.pos_during_animation.x, self.pos_during_animation.y)

        self.current_animation_state = AnimationState.FromTop
        self.animation_time = 0.0
        self.animation = {
            AnimationState.Idle: self.idle_movement,
            AnimationState.FromTop: self.from_top_movement,
            AnimationState.Custom: self.custom_movement
        }

        self.name_text = get_font(20).render(self.name, True, (255, 255, 255))
        self.name_text_rect = self.name_text.get_rect(center=(game.SCREEN_WIDTH / 2, 20))

        self.boss_state = BossState.Idle
        self.boss_attack = BossAttack.Raining

    def _finish_animation(self, animation_time, limit: float = 1.):
        if animation_time >= limit:
            self.current_animation_state = AnimationState.Idle
            self.animation_time = 0.0
            self.boss_attack.time = 0.0
            self.boss_state = BossState.Idle

    def _perform_animation(self, dt, animation_type):

        if animation_type == AnimationState.FromTop:
            self.animation_time += dt

            self.pos_during_animation = Vec2d(animate_position_2d(ease_out_back, self.pos_start_animation.to_tuple(), self.pos.to_tuple(), self.animation_time))
            self.rect.center = self.pos_during_animation.to_tuple()

            self._finish_animation(self.animation_time)

        elif animation_type == AnimationState.Custom:
            self.is_invincible = self.boss_attack.is_invicible

            self.game.screen.blit(self.name_text, self.name_text_rect)
            self.draw_health_bar()

            self.animation_time += dt
            self.boss_attack.time += dt

            self.boss_attack.shoot_interval -= dt

            if self.boss_attack.shoot_interval <= 0.0 and self.boss_attack.shoot_interval_base != 0.0:
                self.boss_attack.shoot_interval = self.boss_attack.shoot_interval_base
                self.shoot()

            anchor_index = int(self.boss_attack.time / self.boss_attack.duration * (len(self.boss_attack.anchors) - 1))

            if self.boss_attack.movement_functions != [] and anchor_index < len(self.boss_attack.anchors) - 1:
                if anchor_index != self.boss_attack.anchor_index:
                    self.boss_attack.anchor_index = anchor_index
                    self.animation_time = 0.0

                if not self.animation_time >= 1.0:
                    self.pos_during_animation = Vec2d(animate_position_2d(self.boss_attack.movement_functions[anchor_index], (self.pos + self.boss_attack.anchors[anchor_index]).to_tuple(), (self.pos + self.boss_attack.anchors[anchor_index + 1]).to_tuple(), self.animation_time))
                    self.rect.center = self.pos_during_animation.to_tuple()
            
            self._finish_animation(self.boss_attack.time, self.boss_attack.duration)

    def update(self, dt):
        self.animation[self.current_animation_state](dt)

    def draw_health_bar(self):
        self.surface_life.fill((23, 23, 23))
        self.surface_life.fill((255, 0, 0), (0, 0, self.life, self.life_bar_height))
        self.game.screen.blit(self.surface_life, self.rect_life)

    def idle_movement(self, dt):

        self.is_invincible = False

        self.game.screen.blit(self.name_text, self.name_text_rect)

        self.interval_attack -= dt

        if self.interval_attack <= 0.0:
            self.interval_attack = 5.0
            self.current_animation_state = AnimationState.Custom
            self.animation_time = 0.0
            self.boss_state = BossState.Attack
            self.boss_attack = random.choice(list(BossAttack))

        # donner un effet de vague au vaisseau lorsqu'il stagne
        self.animation_time += dt * 10 * 0.9
        self.pos.y = math.sin(self.animation_time) * 4 + 240

        self.rect.center = (self.pos.x, self.pos.y)
        self.draw_health_bar()

    def from_top_movement(self, dt):
        self._perform_animation(dt, AnimationState.FromTop)

    def custom_movement(self, dt):
        self._perform_animation(dt, AnimationState.Custom)

    def shoot(self):
        """ tire un projectile suivant le type d'attaque du boss """
        if self.boss_attack == BossAttack.Raining:
            pass
        elif self.boss_attack == BossAttack.Rocket:
            # tire un projectile en direction du joueur
            # on calcule la direction du projectile
            magnitudeA = self.pos.magnitude()
            magintudeB = self.game.main_player.pos.magnitude()

            scalar_product = self.pos.dot(self.game.main_player.pos)
            # on calcule l'angle du projectile via la direction
            angle = math.acos(scalar_product / (magnitudeA * magintudeB))
            angle = math.degrees(angle)

            product = self.pos.product(self.game.main_player.pos)
            if product > 0:
                angle = -angle
                
            # on crée le projectile
            self.game.bullet_group_ennemy.add(Bullet(self.game, 0.4 * self.game.SCREEN_WIDTH, 30, self.pos.to_tuple(), angle))
        elif self.boss_attack == BossAttack.Laser:
            pass

    def take_damage(self, damage: int):
        """ inflige des dégats au boss """
        if not self.is_invincible:
            self.life -= damage
            if self.life <= 0:
                self.kill()


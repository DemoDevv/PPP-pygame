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

    Laser = (6.0, True, 0.0, (0, 0), (0, 0), [ease_out_back, linear, ease_out_back], (300, 70), (-300, 70))
    Raining = (5.0, False, 0.5, (0, 0), (0, 0), [])
    Rocket = (1.0, False, 0.3, (0, 0), (0, 0), [])


class Boss(pygame.sprite.Sprite):

    def __init__(self, game, path_image: str, path_image_laser: str, name: str, init_pos: tuple, init_life: int = 600):
        pygame.sprite.Sprite.__init__(self)

        self.game = game

        self.name = name
        self.life_max = init_life
        self.life = init_life

        self.interval_attack = 5.0
        self.enraged = False

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

        self.path_image = path_image
        self.image = pygame.image.load(path_image)
        if not path_image.startswith("maximilien"):
            self.image = pygame.transform.rotate(self.image, -90)
        self.image = pygame.transform.scale(self.image, (self.rect_width, self.rect_height))

        self.path_image_laser = path_image_laser
        self.is_laser = False

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
        self.boss_attack = BossAttack.Rocket

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

            anchor_index = int(self.boss_attack.time / self.boss_attack.duration * (len(self.boss_attack.anchors) - 1))

            if self.boss_attack.shoot_interval <= 0.0 and self.boss_attack.shoot_interval_base != 0.0:
                self.boss_attack.shoot_interval = self.boss_attack.shoot_interval_base
                self.shoot()
            elif self.boss_attack == BossAttack.Laser and anchor_index == 1:
                self.is_laser = True
                self.shoot()

            if self.is_laser and anchor_index == 2:
                self.image = pygame.image.load(self.path_image)
                if not self.path_image.startswith("maximilien"):
                    self.image = pygame.transform.rotate(self.image, -90)
                self.image = pygame.transform.scale(self.image, (self.rect_width, self.rect_height))
                self.is_laser = False

            if self.boss_attack.movement_functions != [] and anchor_index < len(self.boss_attack.anchors) - 1:
                if anchor_index != self.boss_attack.anchor_index:
                    self.boss_attack.anchor_index = anchor_index
                    self.animation_time = 0.0

                if not self.animation_time >= 1.0:
                    self.pos_during_animation = Vec2d(animate_position_2d(self.boss_attack.movement_functions[anchor_index], (self.pos + self.boss_attack.anchors[anchor_index]).to_tuple(), (self.pos + self.boss_attack.anchors[anchor_index + 1]).to_tuple(), self.animation_time))
                    self.rect.center = self.pos_during_animation.to_tuple()
            
            self._finish_animation(self.boss_attack.time, self.boss_attack.duration)

    def update(self, dt):
        if self.life <= self.life_max // 2 and not self.enraged:
            self.enraged = True
            self.interval_attack = 2.5
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
            self.interval_attack = 5.0 if not self.enraged else 2.5
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
            # tire un projectile dans une direction aléatoire
            # on calcule la direction du projectile
            angle = random.uniform(0, 100) - 50
            # on crée le projectile
            self.game.bullet_group_ennemy.add(Bullet(self.game, 0.4 * self.game.SCREEN_WIDTH, 30, self.pos.to_tuple(), angle, (255, 0, 0), 2))
        if self.boss_attack == BossAttack.Rocket:
            # tire un projectile en direction du joueur
            # on calcule la direction du projectile
            direction = self.game.main_player.pos - self.pos
            # on normalise la direction
            direction.normalize()
            # on calcule l'angle du projectile via la direction
            angle = math.atan2(direction.y, direction.x)
            angle = -(angle * (180 / math.pi) - 90)

            # on crée le projectile
            self.game.bullet_group_ennemy.add(Bullet(self.game, 0.4 * self.game.SCREEN_WIDTH, 30, self.pos.to_tuple(), angle, (255, 0, 0), 2))
        elif self.boss_attack == BossAttack.Laser:
            self.image = pygame.image.load(self.path_image_laser)
            if not self.path_image_laser.startswith("maximilien"):
                self.image = pygame.transform.rotate(self.image, -90)
            self.image = pygame.transform.scale(self.image, (self.rect_width, self.rect_height))

            # création d'un laser qui suit le boss
            # création de la surface du laser
            surface_laser = pygame.Surface((25, self.game.SCREEN_HEIGHT))
            surface_laser.fill((255, 0, 0))
            # création du rect du laser
            rect_laser = surface_laser.get_rect()
            rect_laser.x = self.pos_during_animation.x - 12.5
            rect_laser.y = self.pos_during_animation.y

            # verifier la collision avec le joueur
            if self.game.main_player.rect.colliderect(rect_laser):
                self.game.main_player.take_damage(5)

            # on affiche le laser
            self.game.screen.blit(surface_laser, rect_laser)

    def take_damage(self, damage: int):
        """ inflige des dégats au boss """
        if not self.is_invincible:
            self.life -= damage
            if self.life <= 0:
                self.kill()


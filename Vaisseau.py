import pygame

from utils.Vec2d import Vec2d

class Vaisseau(pygame.sprite.Sprite):

    def __init__(self, game, path_image: str, speed: int, init_pos: tuple):
        pygame.sprite.Sprite.__init__(self)

        self.game = game

        self.speed = speed

        self.pos = Vec2d(init_pos)
        self.velocity = Vec2d((0, 0))

        self.image = pygame.image.load(path_image)
        self.rect_height = 100
        self.rect_width = 100
        self.image = pygame.transform.scale(self.image, (self.rect_width, self.rect_height))

        self.rect = self.image.get_rect()
        self.rect.center = init_pos

        self.dx = 0.0

    def update(self, dt):
        if pygame.key.get_pressed()[self.game.actions['left']]:
            self.dx = -self.speed
        elif pygame.key.get_pressed()[self.game.actions['right']]:
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

    def shoot(self):
        """ tire un projectile """
        print("piouuu")

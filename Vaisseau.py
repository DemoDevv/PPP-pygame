import pygame

class Vaisseau(pygame.sprite.Sprite):

    def __init__(self, game, path_image: str, velocity: int):
        super().__init__()

        self.game = game

        self.image = pygame.image.load(path_image)
        self.image = pygame.transform.scale(self.image, (100, 100))

        self.rect = self.image.get_rect()
        self.rect.x = 800
        self.rect.y = 500

        self.velocity = velocity

    def handle_keys(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            pass # TIRER

        if keys[pygame.K_RIGHT]:
            print(self.velocity * self.game.dt)
            self.rect.x += self.velocity * self.game.dt
        elif keys[pygame.K_LEFT]:
            print(self.velocity * self.game.dt)
            self.rect.x -= self.velocity * self.game.dt

    def update(self):
        pass

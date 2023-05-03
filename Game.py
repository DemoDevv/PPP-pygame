import pygame
import time

from Vaisseau import Vaisseau

class Game:

    def __init__(self) -> None:
        self.running = False
        self.screen = pygame.display.set_mode((1280, 1280))
        self.clock = pygame.time.Clock()

        self.dt = 0
        
        self.vaisseaux_group = pygame.sprite.Group()

        self.main_player = Vaisseau(self, "assets/vaisseau_test.png", 10)
        self.vaisseaux_group.add(self.main_player)
    
    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def run(self):
        self.running = True
        while self.running:
            self.handle_event()

            self.vaisseaux_group.update()
            self.main_player.handle_keys()

            self.screen.fill((0, 0, 0))
            self.vaisseaux_group.draw(self.screen)

            pygame.display.flip()

            self.dt = self.clock.tick() / 1000
        

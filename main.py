import pygame
from Game import Game

if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.screen = pygame.display.set_mode(game.get_screen_dimensions())
    game.clock = pygame.time.Clock()
    game.init()

    game.running = True
    while game.running:
        dt = game.clock.tick(game.fps)
        game.step(dt)
        pygame.display.update()

    pygame.quit()

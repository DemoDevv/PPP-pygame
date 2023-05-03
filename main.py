import pygame
from Game import Game
from State import GameState

if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.screen = pygame.display.set_mode(game.get_screen_dimensions(), vsync=1)
    game.clock = pygame.time.Clock()
    game.init()

    game.running = True
    game.add_main_state(GameState.SPLASH_SCREEN) # pendant le splash screen, on ne fait rien a part si on a besoin de charger des assets ou autre.
    while game.running:
        if game.get_current_main_state() == GameState.SPLASH_SCREEN:
            game.add_main_state(GameState.MAIN_MENU) # on passe au menu principal
        dt = game.clock.tick(60)
        game.step(dt)
        pygame.display.update()

    pygame.quit()

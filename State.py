from abc import ABC, abstractmethod
from enum import Enum
from Button import Button

from utils.Font import get_font

import pygame

class State(ABC):
    @abstractmethod
    def init(self, game):
        pass

    @abstractmethod
    def step(self, game, dt: float):
        pass

class GameState(State, ABC):
    pass


class MainMenuState(GameState):
    def init(self, game):
        self.menu_text = get_font(100).render("MAIN MENU", True, (255, 255, 255))
        self.menu_text_rect = self.menu_text.get_rect(center=(game.SCREEN_WIDTH / 2, game.SCREEN_HEIGHT / 2 - 200))

        self.play_button = Button(None, (game.SCREEN_WIDTH / 2, game.SCREEN_HEIGHT / 2), "PLAY", get_font(75), (255, 255, 255), (255, 0, 0))

        self.buttons = [self.play_button]
    
    def step(self, game, dt):
        menu_mouse_position = pygame.mouse.get_pos()
        
        game.screen.blit(self.menu_text, self.menu_text_rect)

        for button in self.buttons:
            button.change_color(menu_mouse_position)
            button.update(game.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button.check_for_input(menu_mouse_position):
                    game.add_main_state(InGameMainState())


class InGameMainState(GameState):
    def init(self, game):
        pass

    def step(self, game, dt):
        game.main_player.speed = 0.1 * game.SCREEN_WIDTH

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False

            if event.type == pygame.KEYUP and event.key in [game.actions['left'], game.actions['right']]:
                game.main_player.dx = 0.0

            if event.type == pygame.KEYDOWN and event.key == game.actions['shoot']:
                game.main_player.shoot()

        game.main_player.update(dt)
            
        game.vaisseaux_group.draw(game.screen)

class InGameState(State, ABC):
    pass

class GameOverState(InGameState):
    def init(self, game):
        pass

    def step(self, game, dt):
        pass

class IntroState(InGameState):
    def init(self, game):
        pass

    def step(self, game, dt):
        pass

class PlayingState(InGameState):
    def init(self, game):
        pass

    def step(self, game, dt):
        pass

class BossState(InGameState):
    def init(self, game):
        pass

    def step(self, game, dt):
        pass

class WinState(InGameState):
    def init(self, game):
        pass

    def step(self, game, dt):
        pass

class EndState(InGameState):
    def init(self, game):
        pass

    def step(self, game, dt):
        pass

class PauseState(InGameState):
    def init(self, game):
        pass

    def step(self, game, dt):
        pass

class GameLevel(Enum):
    MathieuStage = 0
    RomainStage = 1
    JulesStage = 2
    MaximilienStage = 3
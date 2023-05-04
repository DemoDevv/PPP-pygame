import sys
import pygame

from Vaisseau import Vaisseau
from State import InGameMainState, MainMenuState

class Game:

    def __init__(self) -> None:

        self.actions = {
            'up': pygame.K_UP,
            'down': pygame.K_DOWN,
            'left': pygame.K_LEFT,
            'right': pygame.K_RIGHT,
            'shoot': pygame.K_SPACE,
            'skip': pygame.K_RETURN
        }

        self.running = False

        self.clock = None
        self.screen = None

        self.SCREEN_HEIGHT = 720
        self.SCREEN_WIDTH = 1280

        self.fps_base = 60
        self.fps = self.fps_base

        # on utilise le state comme une pile,
        # cela signifie que le state le plus récent est le dernier élément de la liste 
        # et pour revenir au state précédent,
        # on dépile.
        self.main_state = list()
        self.add_main_state(MainMenuState())

    def add_main_state(self, state):
        """ ajoute un state à la pile """
        self.main_state.append(state)
        state.init(self)

    def pop_main_state(self):
        """ retourne au state précédent """
        self.main_state.pop()

    def get_current_main_state(self):
        """ retourne le state actuel """
        return self.main_state[-1]

    def get_screen_dimensions(self) -> tuple:
        """ retourne les dimensions de l'écran """
        return (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)            

    def init(self):
        """ création des groupes et des sprites """
        self.vaisseaux_group = pygame.sprite.Group()

        self.main_player = Vaisseau(self, "assets/vaisseau_test.png", 0.4 * self.SCREEN_WIDTH, (self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT - 100))
        self.vaisseaux_group.add(self.main_player)

    def step(self, dt: float):
        """ mise à jour des sprites """
        dt /= 1000.0

        self.screen.fill((0, 0, 0))

        # on met à jour le state actuel
        self.get_current_main_state().step(self, dt)

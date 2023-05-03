import sys
import pygame

from Vaisseau import Vaisseau

from State import GameState

class Game:

    def __init__(self) -> None:

        self.actions = {
            'up': pygame.K_UP,
            'down': pygame.K_DOWN,
            'left': pygame.K_LEFT,
            'right': pygame.K_RIGHT,
            'shoot': pygame.K_SPACE
        }

        self.running = False

        self.clock = None
        self.screen = None

        self.SCREEN_HEIGHT = 720
        self.SCREEN_WIDTH = 1280

        # on utilise le state comme une pile,
        # cela signifie que le state le plus récent est le dernier élément de la liste 
        # et pour revenir au state précédent,
        # on dépile.
        self.main_state = list()

    def add_main_state(self, state: GameState):
        """ ajoute un state à la pile """
        self.main_state.append(state)

    def pop_main_state(self):
        """ retourne au state précédent """
        self.main_state.pop()

    def get_current_main_state(self):
        """ retourne le state actuel """
        return self.main_state[-1]

    def get_screen_dimensions(self) -> tuple:
        """ retourne les dimensions de l'écran """
        return (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
    
    def _handle_events(self):
        """ gestion des événements """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYUP and event.key in [self.actions['left'], self.actions['right']]:
                self.main_player.dx = 0.0

            if event.type == pygame.KEYDOWN and event.key == self.actions['shoot']:
                self.main_player.shoot()
                

    def init(self):
        """ création des groupes et des sprites """
        self.vaisseaux_group = pygame.sprite.Group()

        self.main_player = Vaisseau(self, "assets/vaisseau_test.png", 0.4 * self.SCREEN_WIDTH, (self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT - 100))
        self.vaisseaux_group.add(self.main_player)

    def step(self, dt: float):
        """ mise à jour des sprites """
        dt /= 1000.0

        self.screen.fill((0, 0, 0))

        self.main_player.speed = 0.1 * self.SCREEN_WIDTH

        self._handle_events()

        self.main_player.update(dt)
        
        self.vaisseaux_group.draw(self.screen)

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
            'skip': pygame.K_RETURN,
            'pause': pygame.K_ESCAPE,
            'chat': pygame.K_t
        }

        self.running = False

        self.clock = None
        self.screen = None

        self.SCREEN_HEIGHT = 720
        self.SCREEN_WIDTH = 1280

        self.fps_base = 60
        self.fps = self.fps_base

        self.background_image = pygame.image.load("assets/background.png")
        self.background_image = pygame.transform.scale(self.background_image, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

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
        self.reset()

    def get_current_main_state(self):
        """ retourne le state actuel """
        return self.main_state[-1]

    def get_screen_dimensions(self) -> tuple:
        """ retourne les dimensions de l'écran """
        return (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)            

    def init(self):
        """ création des groupes et des sprites """
        self.vaisseaux_group = pygame.sprite.GroupSingle()

        self.main_player = Vaisseau(self, 0.4 * self.SCREEN_WIDTH, (self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT - 100))
        self.vaisseaux_group.add(self.main_player)

        self.bullet_group_player = pygame.sprite.Group()
        self.bullet_group_ennemy = pygame.sprite.Group()

        self.ennemies_group = pygame.sprite.Group()

        self.boss_group = pygame.sprite.Group()

        self.competence_group = pygame.sprite.Group()

        self.groups = [self.bullet_group_player, self.bullet_group_ennemy, self.vaisseaux_group, self.ennemies_group, self.boss_group, self.competence_group]

    def reset(self):
        """ remise à zéro des sprites et des groupes """
        self.init()

    def draw_groups(self):
        for group in self.groups:
            group.draw(self.screen)

    def update_groups(self, dt):
        for group in self.groups:
            group.update(dt)

    def step(self, dt: float):
        """ mise à jour des sprites """
        # on convertit le temps en secondes
        dt /= 1000.0

        # on draw l'image qui fais office de fond
        self.screen.blit(self.background_image, (0, 0))

        # on met à jour le state actuel
        self.get_current_main_state().step(self, dt)

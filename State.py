from abc import ABC, abstractmethod
from enum import Enum

from Button import Button
from Vaisseau import AnimationState
from Ennemie import Ennemie
from Boss import Boss

from utils.Font import get_font

from Command import commands

import pygame
import cv2

import random

import pygame_textinput


class GameLevel(Enum):
    """ Enumération des niveaux de jeu """

    def __init__(self, wave_number, spawn_rate, asset_path_enemies, boss_entity=None):
        super().__init__()
        self.current_wave = 0
        self.wave_number = wave_number
        self.spawn_rate = spawn_rate
        self.asset_path_enemies = asset_path_enemies
        self.boss_entity = boss_entity
        self.boss_defeated = False

    def spawn_enemies(self, game):
        self.current_wave += 1

        if self.is_finished():
            return

        spawn_number = self.spawn_rate * self.current_wave
        for _ in range(spawn_number):
            game.ennemies_group.add(Ennemie(game, self.asset_path_enemies, 3 * 0.4, (random.randint(0, game.SCREEN_WIDTH), -random.randint(120, 280))))

    def is_finished(self):
        return self.current_wave > self.wave_number
    
    def reset(self):
        self.current_wave = 0
        self.boss_defeated = False

    MathieuStage = (1, 2, "assets/vaisseau_ennemi.png", {"path_image": "", "name": "Mathieu"})
    RomainStage = (1, 2, "assets/vaisseau_test.png", {"path_image": "", "name": "Romain"})
    JulesStage = (5, 3, "assets/vaisseau_ennemi.png", {"path_image": "", "name": "Jules"})
    MaximilienStage = (5, 4, "assets/vaisseau_ennemi.png", {"path_image": "", "name": "Maximilien"})

levels = [GameLevel.MathieuStage, GameLevel.RomainStage, GameLevel.JulesStage, GameLevel.MaximilienStage]

class State(ABC):
    @abstractmethod
    def init(self, game, **kwargs):
        """ création des groupes et des sprites de ce state ou des boutons pour les GUI """
        pass

    @abstractmethod
    def step(self, game, dt: float):
        """ mise à jour des sprites de ce state """
        pass

class WindowState(State, ABC):
    """ classe abstraite pour les états de la fenêtre principale """
    pass


class InGameState(State, ABC):
    """ classe abstraite pour les états in-game """
    def __init__(self, parent_state: WindowState) -> None:
        super().__init__()
        self.parent_state = parent_state
        self.paused = False
        self.superposed_state = None

    def add_superposed_state(self, superposed_state: "SuperPosedState", game):
        """ ajoute un state superposé à l'écran de jeu """
        self.superposed_state = superposed_state
        superposed_state.init(game)


class SuperPosedState(State, ABC):
    """ classe abstraite pour les états superposés
        (états qui ne sont pas des états in-game mais qui sont superposés à l'écran de jeu
        et qui mettent le jeu en pause)
        il ne peut y avoir qu'un seul état superposé à la fois """
    def __init__(self, parent_ingame_state: InGameState) -> None:
        super().__init__()
        self.parent_ingame_state = parent_ingame_state


class MainMenuState(WindowState):
    def init(self, game):
        pygame.mixer.music.load("assets/main_sound.mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

        self.menu_text = get_font(100).render("MAIN MENU", True, (255, 255, 255))
        self.menu_text_rect = self.menu_text.get_rect(center=(game.SCREEN_WIDTH / 2, game.SCREEN_HEIGHT / 2 - 200))

        self.play_button = Button(None, (game.SCREEN_WIDTH / 2, game.SCREEN_HEIGHT / 2), "PLAY", get_font(75), (255, 255, 255), (255, 0, 0))

        self.buttons = [self.play_button]
    
    def step(self, game, _):
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
                    pygame.mixer.music.stop()
                    transition_sound = pygame.mixer.Sound("assets/play.mp3")
                    transition_sound.set_volume(0.3)
                    transition_sound.play()


class InGameMainState(WindowState):
    def init(self, game):
        self.in_game_state = list() # pareil que pour le main_state, cependant celui-ci est utilisé pour les états lors du InGameState.
        self.add_ingame_state(IntroState(self), game)

    def step(self, game, dt):
        """ mise à jour du state in-game actuel """
        self.get_current_ingame_state().step(game, dt)

    def add_ingame_state(self, state: InGameState, game, **kwargs):
        """ ajoute un state à la pile """
        self.in_game_state.append(state)
        state.init(game, **kwargs)

    def pop_ingame_state(self):
        """ retourne au state précédent """
        self.in_game_state.pop()

    def get_current_ingame_state(self):
        """ retourne le state actuel """
        return self.in_game_state[-1]

class GameOverState(WindowState):
    def init(self, game):
        self.menu_text = get_font(100).render("GAME OVER", True, (255, 255, 255))
        self.menu_text_rect = self.menu_text.get_rect(center=(game.SCREEN_WIDTH / 2, game.SCREEN_HEIGHT / 2 - 200))

        self.replay_button = Button(None, (game.SCREEN_WIDTH / 2, game.SCREEN_HEIGHT / 2), "MAIN MENU", get_font(75), (255, 255, 255), (255, 0, 0))

        self.buttons = [self.replay_button]
    
    def step(self, game, _):
        menu_mouse_position = pygame.mouse.get_pos()
        
        game.screen.blit(self.menu_text, self.menu_text_rect)

        for button in self.buttons:
            button.change_color(menu_mouse_position)
            button.update(game.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.replay_button.check_for_input(menu_mouse_position):
                    game.pop_main_state() # retourne au jeu
                    game.pop_main_state() # retourne au menu principal
                    pygame.mixer.music.play(-1)

# InGameState

class IntroState(InGameState):
    def init(self, game):
        self.video = cv2.VideoCapture("assets/intro.mp4")
        self.compteur_frame = 0

    def step(self, game, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False

            if event.type == pygame.KEYDOWN and event.key == game.actions['skip']:
                self.video.release()
                self.parent_state.add_ingame_state(PlayingState(self.parent_state), game)

        success, video_image = self.video.read()
        if self.compteur_frame == self.video.get(cv2.CAP_PROP_FRAME_COUNT):
            self.video.release()
            self.parent_state.add_ingame_state(PlayingState(self.parent_state), game)
        if success:
            self.compteur_frame += 1
            video_image_resize = cv2.resize(video_image, (game.SCREEN_WIDTH, game.SCREEN_HEIGHT))
            video_surf = pygame.image.frombuffer(video_image_resize.tobytes(), video_image_resize.shape[1::-1], "RGB")
            game.screen.blit(video_surf, (0, 0))

class PlayingState(InGameState):

    def init(self, game):
        self.level_id = 0
        self.level_state = levels[self.level_id]
        self.level_state.current_wave = 0

        # on evite que le boss soit deja mort lorsqu'on recommence le jeu
        for level in levels:
            level.reset()

        # on fais spawn les premiers ennemis
        self.level_state.spawn_enemies(game)

    def step(self, game, dt):
        game.main_player.speed = 0.1 * game.SCREEN_WIDTH # TODO je sais pas ce que sa fout la

        if self.paused:
            game.draw_groups()
            self.superposed_state.step(game, dt)
            return
        
        if not game.main_player.alive():
            game.add_main_state(GameOverState())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False

            if event.type == pygame.KEYDOWN and event.key == game.actions['pause']: # si on appuie sur la touche pause, on met le jeu en pause
                self.add_superposed_state(PauseState(self), game) # on ajoute un état superposé au jeu et on met le jeu en pause via la fonction init
            
            if event.type == pygame.KEYDOWN and event.key == game.actions['chat']: # si on appuie sur la touche chat, on met le jeu en pause
                self.add_superposed_state(ChatState(self), game)

            if game.main_player.current_animation_state == AnimationState.Idle and game.main_player.alive(): # si le joueur est en idle, on peut le déplacer TODO: modifier pour que animation state provienne du vaisseau

                if event.type == pygame.KEYUP and event.key in [game.actions['left'], game.actions['right']]:
                    game.main_player.dx = 0.0

                if event.type == pygame.KEYDOWN and event.key == game.actions['shoot']:
                    game.main_player.shoot()

        # on update les groupes en verifiant si les ennemis sont hit
        hits = pygame.sprite.groupcollide(game.bullet_group_player, game.ennemies_group, True, False)
        for bullet, ennemy in hits.items():
            ennemy[0].take_damage(bullet.damage)

        # on update les groupes en verifiant si le joueur est hit
        hits = pygame.sprite.groupcollide(game.bullet_group_ennemy, game.vaisseaux_group, True, False)
        for bullet, player in hits.items():
            player[0].take_damage(bullet.damage)

        # on verifie si il y a encore des ennemis en vie
        if len(game.ennemies_group) == 0:
            self.level_state.spawn_enemies(game)

        if self.level_state.is_finished():
            if not self.level_state.boss_defeated:
                self.parent_state.add_ingame_state(BossState(self.parent_state), game, level_state=self.level_state)
            else:
                self.level_id += 1
                if self.level_id == len(levels):
                    # on a fini le jeu
                    pass # bug la
                else: # FIXME regarde sa
                    self.level_state = levels[self.level_id]
                    self.level_state.current_wave = 0
                    self.level_state.spawn_enemies(game)

        game.update_groups(dt)
            
        game.draw_groups()

class BossState(InGameState):
    def init(self, game, **kwargs):
        self.level_state = kwargs['level_state']

        # on fais spawn le boss
        game.boss_group.add(Boss(game, **self.level_state.boss_entity, init_pos=(game.SCREEN_WIDTH/2, 240)))

    def step(self, game, dt):
        game.main_player.speed = 0.1 * game.SCREEN_WIDTH # TODO je sais pas ce que sa fout la

        if self.paused:
            game.draw_groups()
            self.superposed_state.step(game, dt)
            return
        
        if not game.main_player.alive():
            game.add_main_state(GameOverState())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False

            if event.type == pygame.KEYDOWN and event.key == game.actions['pause']: # si on appuie sur la touche pause, on met le jeu en pause
                self.add_superposed_state(PauseState(self), game) # on ajoute un état superposé au jeu et on met le jeu en pause via la fonction init
            
            if event.type == pygame.KEYDOWN and event.key == game.actions['chat']: # si on appuie sur la touche chat, on met le jeu en pause
                self.add_superposed_state(ChatState(self), game)

            if game.main_player.current_animation_state == AnimationState.Idle and game.main_player.alive(): # si le joueur est en idle, on peut le déplacer TODO: modifier pour que animation state provienne du vaisseau

                if event.type == pygame.KEYUP and event.key in [game.actions['left'], game.actions['right']]:
                    game.main_player.dx = 0.0

                if event.type == pygame.KEYDOWN and event.key == game.actions['shoot']:
                    game.main_player.shoot()

        # on update les groupes en verifiant si les boss sont hit
        hits = pygame.sprite.groupcollide(game.bullet_group_player, game.boss_group, True, False)
        for bullet, ennemy in hits.items():
            ennemy[0].take_damage(bullet.damage)

        # on update les groupes en verifiant si le joueur est hit
        hits = pygame.sprite.groupcollide(game.bullet_group_ennemy, game.vaisseaux_group, True, False)
        for bullet, player in hits.items():
            player[0].take_damage(bullet.damage)

        # verifier si le boss est mort et pop l'état
        if len(game.boss_group) == 0:
            self.level_state.boss_defeated = True
            self.parent_state.pop_ingame_state()

        game.update_groups(dt)
            
        game.draw_groups()

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

class PauseState(SuperPosedState):
    def init(self, game):
        self.parent_ingame_state.paused = True

        self.opacity_background = pygame.Surface((game.SCREEN_WIDTH, game.SCREEN_HEIGHT), pygame.SRCALPHA)

        self.menu_text = get_font(100).render("PAUSE", True, (255, 255, 255))
        self.menu_text_rect = self.menu_text.get_rect(center=(game.SCREEN_WIDTH / 2, game.SCREEN_HEIGHT / 2 - 200))

        self.continue_button = Button(None, (game.SCREEN_WIDTH / 2, game.SCREEN_HEIGHT / 2), "CONTINUER", get_font(75), (255, 255, 255), (255, 0, 0))
        self.quit_button = Button(None, (game.SCREEN_WIDTH / 2, game.SCREEN_HEIGHT / 2 + 150), "QUITTER", get_font(75), (255, 255, 255), (255, 0, 0))

        self.buttons = [self.continue_button, self.quit_button]

    def step(self, game, dt):
        menu_mouse_position = pygame.mouse.get_pos()

        self.opacity_background.fill((0, 0, 0, 155))
        game.screen.blit(self.opacity_background, (0, 0))
        
        game.screen.blit(self.menu_text, self.menu_text_rect)

        for button in self.buttons:
            button.change_color(menu_mouse_position)
            button.update(game.screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False

            if event.type == pygame.KEYDOWN and event.key == game.actions['pause']: # si on appuie sur la touche pause, on met le jeu en play
                self.parent_ingame_state.paused = False
                self.parent_ingame_state.superposed_state = None
                game.main_player.dx = 0.0

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.continue_button.check_for_input(menu_mouse_position):
                    self.parent_ingame_state.paused = False
                    self.parent_ingame_state.superposed_state = None
                    game.main_player.dx = 0.0

                elif self.quit_button.check_for_input(menu_mouse_position):
                    game.pop_main_state()
                    pygame.mixer.music.play(-1)


class ChatState(SuperPosedState):

    def init(self, game):
        self.parent_ingame_state.paused = True

        self.text_input_visualizer = pygame_textinput.TextInputVisualizer(pygame_textinput.TextInputManager(validator=lambda input: len(input) <= 16), get_font(12), font_color=(255, 255, 255), cursor_color=(255, 255, 255), cursor_blink_interval=500)

    def step(self, game, dt):
        events = pygame.event.get()

        self.text_input_visualizer.update(events)

        game.screen.blit(self.text_input_visualizer.surface, (10, game.SCREEN_HEIGHT - 20))

        for event in events:
            if event.type == pygame.QUIT:
                game.running = False

            if event.type == pygame.KEYDOWN and event.key == game.actions['pause']: # si on appuie sur la touche pause, on met le jeu en play
                self.parent_ingame_state.paused = False
                self.parent_ingame_state.superposed_state = None
                game.main_player.dx = 0.0

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                text_input_value = self.text_input_visualizer.value

                if text_input_value[0] != "/":
                    print("ce n'est pas une commande")
                    break # TODO: afficher un message d'erreur
                
                command_name = text_input_value[1:]
                command_objs = list(filter(lambda command: command.name == command_name, commands))

                if len(command_objs) == 0:
                    print("commande inconnue")
                    break # TODO: gerer les commandes inconnues

                command_obj = command_objs[0]

                command_obj.execute(game) # on execute la commande

                self.parent_ingame_state.paused = False
                self.parent_ingame_state.superposed_state = None
                game.main_player.dx = 0.0

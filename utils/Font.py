import pygame

def get_font(size: int, path: str = 'assets/font.ttf') -> pygame.font.Font:
    """ retourne une police de la taille donnée """
    return pygame.font.Font(path, size)
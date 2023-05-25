import sys


class Command:
    """ Classe qui représente une commande que l'on peut utiliser dans le jeu """

    def __init__(self, name, description, function):
        self.name = name
        self.description = description
        self.function = function

    def execute(self, *args, **kwargs):
        self.function(*args, **kwargs)


commands = [
    Command("help", "Affiche la liste des commandes", lambda: print("\n".join([f"{command.name} : {command.description}" for command in commands]))),
    Command("quit", "Quitte le jeu", lambda: sys.exit()),
    Command("invicible", "Rend le vaisseau invincible", lambda game: game.main_player.invicible()),
]

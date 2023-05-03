from enum import Enum

class GameState(Enum):
    SPLASH_SCREEN = 0
    MAIN_MENU = 1
    INGAME = 2
    PAUSE = 3

class InGameState(Enum):
    GAME_OVER = 0
    INTRO = 1
    PLAYING = 2
    BOSS = 3
    WIN = 4
    END = 5

class GameLevel(Enum):
    MathieuStage = 0
    RomainStage = 1
    JulesStage = 2
    MaximilienStage = 3
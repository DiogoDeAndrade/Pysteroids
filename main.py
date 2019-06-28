import array
import random
from pygame.math import Vector2

from WireMesh import *
from GameDefs import *
from Scene import *
from ScreenAsteroidsTitle import * 
from ScreenAsteroidsGame import * 
from SoundManager import *
from FontManager import *

gScene = Scene()

def load_data():
    WireMesh.load_model("models/player_ship.json", "PlayerShip")
    WireMesh.load_model("models/missile.json", "Missile")

    SoundManager.load("audio/explosion.wav", "Explosion")
    SoundManager.load("audio/laser.wav", "Laser")
    SoundManager.load("audio/engine.wav", "Engine")

    FontManager.load("fonts/vector/Vectorb.ttf", 18, "VectorTTF")
    fnt = FontManager.load("fonts/vectorfont.json", 4, "Vector")

    GameDefs.load_highscores()

def main():

    Screen.startup()

    load_data()

    title_screen = ScreenAsteroidsTitle()
    game_screen = ScreenAsteroidsGame()

    ret = 0
    while (ret == 0):
        ret = title_screen.run()
        if (ret == -1):
            break
        elif (ret == 1):
            game_screen.reset()
            
            ret = 1
            while (ret == 1):
                ret = game_screen.run()
    
if __name__ == "__main__":
    main();

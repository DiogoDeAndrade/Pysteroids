import array
import random
from pygame.math import Vector2

import Engine

from GameDefs import *
from ScreenAsteroidsTitle import * 
from ScreenAsteroidsGame import * 

gScene = Engine.Scene()

def load_data():
    Engine.WireMesh.load_model("models/player_ship.json", "PlayerShip")
    Engine.WireMesh.load_model("models/missile.json", "Missile")

    Engine.SoundManager.load("audio/explosion.wav", "Explosion")
    Engine.SoundManager.load("audio/laser.wav", "Laser")
    Engine.SoundManager.load("audio/engine.wav", "Engine")

    Engine.FontManager.load("fonts/vector/Vectorb.ttf", 18, "VectorTTF")
    fnt = Engine.FontManager.load("fonts/vectorfont.json", 4, "Vector")

    GameDefs.load_highscores()

def main():

    Engine.Screen.startup()

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

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
    WireMesh.LoadModel("models/player_ship.json", "PlayerShip")
    WireMesh.LoadModel("models/missile.json", "Missile")

    SoundManager.Load("audio/explosion.wav", "Explosion")
    SoundManager.Load("audio/laser.wav", "Laser")
    SoundManager.Load("audio/engine.wav", "Engine")

    FontManager.Load("fonts/vector/Vectorb.ttf", 18, "VectorTTF")
    fnt = FontManager.Load("fonts/vectorfont.json", 4, "Vector")
    fnt.lineWidth = 4

def main():

    Screen.startup()

    load_data()

    titleScreen = ScreenAsteroidsTitle()
    gameScreen = ScreenAsteroidsGame()

    ret = 0
    while (ret == 0):
        ret = titleScreen.run()
        if (ret == -1):
            break
        elif (ret == 1):
            gameScreen.lives = 3
            gameScreen.level =1
            gameScreen.score = 0
            
            ret = 1
            while (ret == 1):
                ret = gameScreen.run()
    
if __name__ == "__main__":
    main();

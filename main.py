import array
import random
from pygame.math import Vector2

import Engine

from GameDefs import *
from ScreenAsteroidsTitle import * 
from ScreenAsteroidsGame import * 

gScene = Engine.Scene()

def load_data():
    """Loads all models, sounds and fonts necessary for the game. It also loads the high scores."""

    # Load models
    Engine.WireMesh.load_model("models/player_ship.json", "PlayerShip")
    Engine.WireMesh.load_model("models/missile.json", "Missile")

    # Loads sounds
    Engine.SoundManager.load("audio/explosion.wav", "Explosion")
    Engine.SoundManager.load("audio/laser.wav", "Laser")
    Engine.SoundManager.load("audio/engine.wav", "Engine")

    # Loads fonts
    Engine.FontManager.load("fonts/vector/Vectorb.ttf", 18, "VectorTTF")
    Engine.FontManager.load("fonts/vectorfont.json", 4, "Vector")

    # Loads the highscores
    GameDefs.load_highscores()

def main():
    """Main game pump, initializes the engine, creates the screen and manages the screen flow."""

    # Starts up the game engine
    Engine.Screen.startup()

    # Loads external data
    load_data()

    # Creates screens
    title_screen = ScreenAsteroidsTitle()
    game_screen = ScreenAsteroidsGame()

    # Manages the screen flow.
    # A screen that returns 0 means that it's supposed to keep running. If it returns -1, it means it has to quit to the desktop. If it returns 1, means the game should continue and not
    # go back to the main menu.
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

import json
import os

import Engine

class PlayerDefs:
    rotationSpeed = 360

class GameDefs:
    player_defs = PlayerDefs()
    highscores = []

    @staticmethod
    def load_highscores():

        try:    
            text_file = open("highscore.dat", "rt")
            json_string = text_file.read()
            text_file.close()

            GameDefs.highscores = json.loads(json_string)

        except:
            GameDefs.highscores = []

            for i in range(0,10):
                hs = ("DGA", (i + 1) * 250)
                GameDefs.highscores.append(hs)

        GameDefs.highscores.sort(key = lambda hs: hs[1], reverse = True)

    @staticmethod
    def is_highscore(score):
        if (score > GameDefs.highscores[9][1]):
            return True
        
        return False

    @staticmethod
    def display_highscores(base_y):
        for i in range(0, 10):
            hs_text = str(i + 1).rjust(2," ") + "." + GameDefs.highscores[i][0] + "......" + str(GameDefs.highscores[i][1]).rjust(6, "0")
            Engine.FontManager.write_center(Engine.Screen.screen, "Vector", hs_text, (640, base_y + i * 30), (255, 255, 180), scale = 0.2, width_scale = 0.25)

    @staticmethod
    def add_highscore(score, name):
        hs = (name, score)
        GameDefs.highscores.append(hs)
        GameDefs.highscores.sort(key = lambda hs: hs[1], reverse = True)
        GameDefs.highscores.remove(GameDefs.highscores[10])

        json_string = json.dumps(GameDefs.highscores)

        text_file = open("highscore.dat", "wt")
        text_file.write(json_string)
        text_file.close()

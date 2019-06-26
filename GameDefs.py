from FontManager import *
from Screen import *
import json
import os

class PlayerDefs:
    rotationSpeed = 360

class GameDefs:
    playerDefs = PlayerDefs()
    highScores = []

    @staticmethod
    def LoadHighscores():

        try:    
            text_file = open("highscore.dat", "rt")
            jsonString = text_file.read()
            text_file.close()

            GameDefs.highScores = json.loads(jsonString)

        except:
            GameDefs.highScores = []

            for i in range(0,10):
                hs = ("DGA", (i + 1) * 250)
                GameDefs.highScores.append(hs)

        GameDefs.highScores.sort(key = lambda hs: hs[1], reverse = True)

    @staticmethod
    def IsHighScore(score):
        if (score > GameDefs.highScores[9][1]):
            return True
        
        return False

    @staticmethod
    def DisplayHighScores(baseY):
        for i in range(0, 10):
            hsText = str(i + 1).rjust(2," ") + "." + GameDefs.highScores[i][0] + "......" + str(GameDefs.highScores[i][1]).rjust(6, "0")
            FontManager.WriteCenter(Screen.screen, "Vector", hsText, (640, baseY + i * 30), (255, 255, 180), scale = 0.2, widthScale = 0.25)

    @staticmethod
    def AddHighScore(score, name):
        hs = (name, score)
        GameDefs.highScores.append(hs)
        GameDefs.highScores.sort(key = lambda hs: hs[1], reverse = True)
        GameDefs.highScores.remove(GameDefs.highScores[10])

        jsonString = json.dumps(GameDefs.highScores)

        text_file = open("highscore.dat", "wt")
        text_file.write(jsonString)
        text_file.close()

from FontManager import *
from Screen import *

class PlayerDefs:
    rotationSpeed = 360

class GameDefs:
    playerDefs = PlayerDefs()
    highScores = []

    @staticmethod
    def LoadHighscores():
        GameDefs.highScores = []

        for i in range(0,10):
            hs = ("DGA", (i + 1) * 250)
            GameDefs.highScores.append(hs)

        GameDefs.highScores.sort(key = lambda hs: hs[1], reverse = True)

    @staticmethod
    def DisplayHighScores(baseY):
        for i in range(0, 10):
            hsText = str(i + 1).rjust(2," ") + "." + GameDefs.highScores[i][0] + "......" + str(GameDefs.highScores[i][1]).rjust(6, "0")
            FontManager.WriteCenter(Screen.screen, "Vector", hsText, (640, baseY + i * 30), (255, 255, 180), scale = 0.2, widthScale = 0.25)

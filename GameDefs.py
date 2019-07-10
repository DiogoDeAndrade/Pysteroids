import json
import os

import Engine

class PlayerDefs:
    """Player definitions, it stores constants and gameplay variables to easily access them throughout the code"""
    rotationSpeed = 360
    """ Rotation speed of the player (in degrees per second) """

class GameDefs:
    """Game definitions, it stores constants and game variables like highscores, so we can access them throughout the code"""
    # Stores the player defs (statically)
    player_defs = PlayerDefs()
    """ Player definitions """
    # Stores the highscores (statically)
    highscores = []
    """ Highscores (array of tuples in the form (name, score)) """

    @staticmethod
    def load_highscores():
        """Loads the highscore table from a JSON file called highscore.dat"""

        try:    
            text_file = open("highscore.dat", "rt")
            json_string = text_file.read()
            text_file.close()

            GameDefs.highscores = json.loads(json_string)

        except:
            # If there is no file found with the proper name (or something happens during parsing), create a default highscore table.
            GameDefs.highscores = []

            for i in range(0,10):
                hs = ("DGA", (i + 1) * 250)
                GameDefs.highscores.append(hs)

        GameDefs.highscores.sort(key = lambda hs: hs[1], reverse = True)

    @staticmethod
    def is_highscore(score):
        """Check if the given score should be on the highscore table.
        
        Arguments:
            score {integer} -- Score to check
        
        Returns:
            bool -- True if the score belongs on the table.
        """
        if (score > GameDefs.highscores[9][1]):
            return True
        
        return False

    @staticmethod
    def display_highscores(base_y):
        """Displays the highscore table on the given height
        
        Arguments:
            base_y {integer} -- Height in which to display the highscore table.
        """
        for i in range(0, 10):
            hs_text = str(i + 1).rjust(2," ") + "." + GameDefs.highscores[i][0] + "......" + str(GameDefs.highscores[i][1]).rjust(6, "0")
            Engine.FontManager.write_center(Engine.Screen.screen, "Vector", hs_text, (640, base_y + i * 30), (255, 255, 180), scale = 0.2, width_scale = 0.25)

    @staticmethod
    def add_highscore(score, name):
        """Adds a score with a certain name to the highscore table.
        
        Arguments:
            score {integer} -- Score to the add
            
            name {string} -- Name of the player
        """

        hs = (name, score)
        # Add the highscore
        GameDefs.highscores.append(hs)
        # Sort highscore table
        GameDefs.highscores.sort(key = lambda hs: hs[1], reverse = True)
        # Remove last entry of the highscore table
        GameDefs.highscores.remove(GameDefs.highscores[10])

        # Save the JSON file with the highscores
        json_string = json.dumps(GameDefs.highscores)

        text_file = open("highscore.dat", "wt")
        text_file.write(json_string)
        text_file.close()

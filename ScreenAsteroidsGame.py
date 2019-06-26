from ScreenAsteroids import *
from PlayerShip import *
from EnemyShip import *
from FontManager import *

class ScreenAsteroidsGame(ScreenAsteroids):
    def __init__(self):
        self.reset()

    def reset(self):
        self.level = 1
        self.lives = 3
        self.score = 0
        self.inputChar = -1
        self.inputName = [ "A", ".", "." ]
        self.inputDelay = 0

    def init(self):
        ScreenAsteroids.init(self)

        self.time_to_spawn = 1.5
        self.init_objects(self.level)

        self.enemy_rate = max(16 - self.level, 4)

        self.enemy_timer = self.enemy_rate

    def update(self, delta_time):
        ScreenAsteroids.update(self, delta_time)

        collisions = Scene.main.CheckCollisionsBetweenTags("PlayerShip", [ "Asteroid", "EnemyShip", "EnemyMissile", "EnemyLaser" ])

        if (len(collisions) > 0):
            collisions[0].obj1.Explode()
            self.lives = self.lives - 1
            for collision in collisions:
                collision.obj2.Explode()
            if (self.lives <= 0):
                if (GameDefs.IsHighScore(self.score)):
                    self.inputChar = 0

        collisions = Scene.main.CheckCollisionsBetweenTags("PlayerLaser", [ "Asteroid", "EnemyShip", "EnemyMissile" ])
        if (len(collisions) > 0):
            for collision in collisions:
                collision.obj1.Destroy()
                collision.obj2.Explode()
                self.score = self.score + collision.obj2.scoreToAdd

        if (self.time_to_spawn > 0):
            self.time_to_spawn = self.time_to_spawn - delta_time

        player =  Scene.main.GetObjectByTag("PlayerShip")
        if ((self.lives > 0) and (player == None) and (self.time_to_spawn <= 0)):
            self.spawn_player()

        self.inputDelay = self.inputDelay - delta_time

        keys = pygame.key.get_pressed()

        if (self.inputChar != -1):
            if ((keys[pygame.K_DOWN]) and (self.inputDelay <= 0)):
                self.inputDelay = 0.2
                self.inputName[self.inputChar] = chr(ord(self.inputName[self.inputChar]) + 1)
            elif ((keys[pygame.K_UP]) and (self.inputDelay <= 0)):
                self.inputDelay = 0.2
                self.inputName[self.inputChar] = chr(ord(self.inputName[self.inputChar]) - 1)
            elif ((keys[pygame.K_LCTRL]) and (self.inputDelay <= 0)):
                self.inputDelay = 0.2
                self.inputChar = self.inputChar + 1
                if (self.inputChar > 2):
                    self.inputChar = -1
                    GameDefs.AddHighScore(self.score, "".join(self.inputName))
                else:
                    self.inputName[self.inputChar] = "A"
            if (self.inputChar != -1):
                c = ord(self.inputName[self.inputChar])
                if (c == ord("A") - 1):
                    self.inputName[self.inputChar] = "9"
                elif (c == ord('0') - 1):
                    self.inputName[self.inputChar] = "Z"
                elif (c == ord("Z") + 1):
                    self.inputName[self.inputChar] = "0"
                elif (c == ord("9") + 1):
                    self.inputName[self.inputChar] = "A"
        else:
            if (self.lives <= 0):
                if (self.inputDelay <= 0):
                    if (keys[pygame.K_LCTRL]):
                        self.set_exit(0)

        if (self.level > 1):
            self.enemy_timer = self.enemy_timer - delta_time
            if (self.enemy_timer < 0):
                self.spawn_enemy()

        asteroid =  Scene.main.GetObjectByTag("Asteroid")
        if (asteroid == None):
            self.level = self.level + 1
            self.set_exit(1)

    def spawn_enemy(self):
        enemy = EnemyShip("EnemyShip")
        enemy.position = Vector2(1000, 500)
        if (self.level > 5):
            enemy.weapon = 2
            enemy.current_shot_cooldown = enemy.shot_cooldown = 10
        elif (self.level > 3):
            enemy.weapon = 1
            enemy.current_shot_cooldown = enemy.shot_cooldown = 3
        else:
            enemy.weapon  = 0
            enemy.current_shot_cooldown = enemy.shot_cooldown = 1

        Scene.main.Add(enemy)

        self.enemy_timer = self.enemy_rate

    def spawn_player(self):
        player = Scene.main.GetObjectByTag("PlayerShip")
        if (player == None):
            # Check if some asteroid is nearby
            circle = Circle2d(Vector2(640,320), 60)

            objects = Scene.main.GetObjectsInCollider("Asteroid", circle)

            if (len(objects) == 0):
                Scene.main.Add(PlayerShip("PlayerShip"))

    def render(self):
        ScreenAsteroids.render(self)

        FontManager.Write(Screen.screen, "VectorTTF", str(self.score).zfill(6), (5, 5), (255, 255, 255))
        for i in range(0, self.lives):
            WireMesh.DrawModel(Screen.screen, "PlayerShip", Vector2(i * 20 + 15, 45), 0, Vector2(0.5, 0.5))
        
        player =  Scene.main.GetObjectByTag("PlayerShip")
        if (player == None):
            if (self.lives > 0):
                FontManager.WriteCenter(Screen.screen, "Vector", "STAGE " + str(self.level), (640, 360), (random.uniform(32, 255), random.uniform(32, 255), random.uniform(32, 255)), scale = 0.5)
            else:
                FontManager.WriteCenter(Screen.screen, "Vector", "GAME OVER", (640, 100), (random.uniform(32, 255), random.uniform(32, 255), random.uniform(32, 255)), scale = 1)
                if ((self.inputChar >= 0) or (self.inputName[2] != ".")):
                    FontManager.WriteCenter(Screen.screen, "Vector", "YOU HAVE A HIGHSCORE!", (640, 320), (255, 255, 180), scale = 0.25, widthScale = 0.25)
                    for i in range(0, 3):
                        c = (255, 255, 180)
                        if (i == self.inputChar):
                            c = (random.uniform(30, 255),random.uniform(30, 255),random.uniform(30, 255))
                        FontManager.Write(Screen.screen, "Vector", self.inputName[i], (640 + (i - 1) * 40, 400), c, scale = 0.5, widthScale = 0.5)


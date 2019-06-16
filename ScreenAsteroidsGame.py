from ScreenAsteroids import *
from PlayerShip import *
from EnemyShip import *
from FontManager import *

class ScreenAsteroidsGame(ScreenAsteroids):
    def __init__(self):
        self.level = 1
        self.lives = 3
        self.score = 0

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

        if (self.lives <= 0):
            keys = pygame.key.get_pressed()
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
                FontManager.WriteCenter(Screen.screen, "Vector", "GAME OVER", (640, 360), (random.uniform(32, 255), random.uniform(32, 255), random.uniform(32, 255)), scale = 1)


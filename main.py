import array
import pygame
import time
import random
from pygame.math import Vector2

from SpriteInfo import *
from WireMesh import *
from GameDefs import *
from PlayerShip import *
from EnemyShip import *
from Asteroid import *
from Starfield import *
from Scene import *
from SoundManager import *
from FontManager import *

gSprites = dict()
gScene = Scene()
gScore = 0
gLives = 3
gLevel = 1
gScreen = 0
gScaling = 1
gTimeToSpawn = 0
gEnemyRate = 0
gEnemyTimer = 0

def start_screen(screenId):
    global gScreen
    global gScaling
    global gTimeToSpawn

    # Wait for the fire key to be depressed
    keys = pygame.key.get_pressed()
    while (keys[pygame.K_LCTRL]):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                running = False
        keys = pygame.key.get_pressed()


    gScreen = screenId

    Scene.main.Clear()

    if (gScreen == 0):
        gScaling = 40
    elif (gScreen == 1):
        gTimeToSpawn = 1.5

    init_objects()

def load_data():
    WireMesh.LoadModel("models/player_ship.json", "PlayerShip")
    WireMesh.LoadModel("models/missile.json", "Missile")

    SoundManager.Load("audio/explosion.wav", "Explosion")
    SoundManager.Load("audio/laser.wav", "Laser")
    SoundManager.Load("audio/engine.wav", "Engine")

    FontManager.Load("fonts/vector/Vectorb.ttf", 18, "VectorTTF")
    fnt = FontManager.Load("fonts/vectorfont.json", 4, "Vector")
    fnt.lineWidth = 4

def init_objects():

    global gLevel
    global gEnemyRate
    global gEnemyTimer

    Scene.main.Add(Starfield("Starfield", 400))

    n_asteroids = 3 + gLevel

    for i in range(0,n_asteroids):
        asteroid = Asteroid("Asteroid" + str(i))
        dir = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        asteroid.position = Vector2(640, 360)
        asteroid.position.x = asteroid.position.x + dir.x * random.uniform(200, 640)
        asteroid.position.y = asteroid.position.y + dir.y * random.uniform(100, 360)
        Scene.main.Add(asteroid)

    gEnemyRate = 16 - gLevel
    if (gEnemyRate < 4):
        gEnemyRate = 4

    gEnemyTimer = gEnemyRate
        
def SpawnEnemy():
    global gLevel
    global gEnemyTimer

    enemy = EnemyShip("EnemyShip")
    enemy.position = Vector2(1000, 500)
    if (gLevel > 8):
        enemy.weapon = 2
        enemy.current_shot_cooldown = enemy.shot_cooldown = 10
    elif (gLevel > 4):
        enemy.weapon = 1
        enemy.current_shot_cooldown = enemy.shot_cooldown = 3
    else:
        enemy.weapon  = 0
        enemy.current_shot_cooldown = enemy.shot_cooldown = 1

    Scene.main.Add(enemy)

    gEnemyTimer = gEnemyRate

def update(delta_time):

    global gScore
    global gLives
    global gScreen
    global gScaling
    global gTimeToSpawn
    global gEnemyRate
    global gEnemyTimer
    global gLevel

    Scene.main.Update(delta_time)

    if (gScreen == 0):
        if (gScaling > 1):
            gScaling = gScaling - delta_time * 10
            if (gScaling < 1):
                gScaling = 1
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LCTRL]):
            gLives = 3
            gLevel = 1
            start_screen(1)
    elif (gScreen == 1):
        collisions = Scene.main.CheckCollisionsBetweenTags("PlayerShip", [ "Asteroid", "EnemyShip", "EnemyMissile", "EnemyLaser" ])

        if (len(collisions) > 0):
            collisions[0].obj1.Explode()
            gLives = gLives - 1
            for collision in collisions:
                collision.obj2.Explode()

        collisions = Scene.main.CheckCollisionsBetweenTags("PlayerLaser", [ "Asteroid", "EnemyShip", "EnemyMissile" ])
        if (len(collisions) > 0):
            for collision in collisions:
                collision.obj1.Destroy()
                collision.obj2.Explode()
                gScore = gScore + collision.obj2.scoreToAdd

        if (gTimeToSpawn > 0):
            gTimeToSpawn = gTimeToSpawn - delta_time

        player =  Scene.main.GetObjectByTag("PlayerShip")
        if ((gLives > 0) and (player == None) and (gTimeToSpawn <= 0)):
            SpawnPlayer()

        if (gLives <= 0):
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_LCTRL]):
                start_screen(0)

        if (gLevel > 1):
            gEnemyTimer = gEnemyTimer - delta_time
            if (gEnemyTimer < 0):
                SpawnEnemy()

        asteroid =  Scene.main.GetObjectByTag("Asteroid")
        if (asteroid == None):
            gLevel = gLevel + 1
            start_screen(1)

def render(screen):

    global gScore
    global gScreen
    global gScaling
    global gLevel

    screen.fill((5, 5, 15))

    Scene.main.Render(screen)

    if (gScreen == 0):
        FontManager.WriteCenter(screen, "Vector", "PYSTEROIDS", (640, 320), (random.uniform(32, 255), random.uniform(32, 255), random.uniform(32, 255)), spacingScale = gScaling)
        if (gScaling <= 1):
            FontManager.WriteCenter(screen, "Vector", "PRESS FIRE TO START", (640, 450), (random.uniform(32, 255), random.uniform(32, 255), random.uniform(32, 255)), scale = 0.2)
    elif (gScreen == 1):    
        FontManager.Write(screen, "VectorTTF", str(gScore).zfill(6), (5, 5), (255, 255, 255))
        for i in range(0, gLives):
            WireMesh.DrawModel(screen, "PlayerShip", Vector2(i * 20 + 15, 45), 0, Vector2(0.5, 0.5))
        
        player =  Scene.main.GetObjectByTag("PlayerShip")
        if (player == None):
            if (gLives > 0):
                FontManager.WriteCenter(screen, "Vector", "STAGE " + str(gLevel), (640, 360), (random.uniform(32, 255), random.uniform(32, 255), random.uniform(32, 255)), scale = 0.5)
            else:
                FontManager.WriteCenter(screen, "Vector", "GAME OVER", (640, 360), (random.uniform(32, 255), random.uniform(32, 255), random.uniform(32, 255)), scale = 1)

    pygame.display.flip()

def SpawnPlayer():
    player = Scene.main.GetObjectByTag("PlayerShip")
    if (player == None):
        # Check if some asteroid is nearby
        circle = Circle2d(Vector2(640,320), 60)

        objects = Scene.main.GetObjectsInCollider("Asteroid", circle)

        if (len(objects) == 0):
            Scene.main.Add(PlayerShip("PlayerShip"))


def main():

    global gScreen

    pygame.mixer.pre_init(44100, 16, 2, 1024)
    pygame.init()
    logo = pygame.image.load("sprites/icon.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Pysteroids")

    screen = pygame.display.set_mode((1280, 720), pygame.DOUBLEBUF)

    SoundManager.SetGlobalVolume(0.25)

    load_data()
    start_screen(0)

    running = True

    dt = 0
    prev_time = time.time()

    while running:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                running = False

        keys = pygame.key.get_pressed()
        if ((keys[pygame.K_ESCAPE]) and (keys[pygame.K_LSHIFT])):
            running = False        
        if (((keys[pygame.K_r]) and (keys[pygame.K_LSHIFT]))):
            SpawnPlayer()

        update(dt)
        render(screen)
        
        dt = time.time() - prev_time
        prev_time = time.time()
    
if __name__ == "__main__":
    main();

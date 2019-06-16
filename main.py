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
gScreen = 0
gScaling = 1

def start_screen(screenId):
    global gScreen
    global gScaling

    gScreen = screenId

    Scene.main.Clear()

    if (gScreen == 0):
        gScaling = 40
    elif (gScreen == 1):
        pass

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

    Scene.main.Add(Starfield("Starfield", 400))

    n_asteroids = 10

    for i in range(0,n_asteroids):
        asteroid = Asteroid("Asteroid" + str(i))
        asteroid.position = Vector2(random.uniform(0, 1280), random.uniform(0, 720))
        Scene.main.Add(asteroid)

    enemy = EnemyShip("EnemyShip")
    enemy.position = Vector2(1000, 500)
    enemy.weapon = 2
    enemy.shot_cooldown = 10
    Scene.main.Add(enemy)


def update(delta_time):

    global gScore
    global gLives
    global gScreen
    global gScaling

    Scene.main.Update(delta_time)

    if (gScreen == 0):
        if (gScaling > 1):
            gScaling = gScaling - delta_time * 10
            if (gScaling < 1):
                gScaling = 1
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE]):
            start_screen(1)
    elif (gScreen == 1):
        collisions = Scene.main.CheckCollisionsBetweenTags("PlayerShip", [ "Asteroid", "EnemyShip", "EnemyMissile", "EnemyLaser" ])

        if (len(collisions) > 0):
            collisions[0].obj1.Explode()
            gLives = gLives - 1
            for collision in collisions:
                collision.obj2.Explode()

        collisions = Scene.main.CheckCollisionsBetweenTags("PlayerLaser", [ "Asteroid", "EnemyShip" ])
        if (len(collisions) > 0):
            for collision in collisions:
                collision.obj1.Destroy()
                collision.obj2.Explode()
                gScore = gScore + 100

        player =  Scene.main.GetObjectByTag("PlayerShip")
        if ((gLives > 0) and (player == None)):
            SpawnPlayer()

def render(screen):

    global gScore
    global gScreen
    global gScaling

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

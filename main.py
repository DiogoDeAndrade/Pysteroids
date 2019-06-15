import array
import pygame
import time
import random
from pygame.math import Vector2

from SpriteInfo import *
from WireMesh import *
from GameDefs import *
from PlayerShip import *
from Asteroid import *
from Starfield import *
from Scene import *
from SoundManager import *
from FontManager import *

gSprites = dict()
gScene = Scene()
gScore = 0
gLives = 3

def load_data():
    ship_player = WireMesh.LoadModel("models/player_ship.json", "PlayerShip")

    SoundManager.Load("audio/explosion.wav", "Explosion")
    SoundManager.Load("audio/laser.wav", "Laser")
    SoundManager.Load("audio/engine.wav", "Engine")

    FontManager.Load("fonts/vector/Vectorb.ttf", 18, "Vector")

def init_objects():

    Scene.main.Add(Starfield("Starfield", 400))

    n_asteroids = 10

    for i in range(0,n_asteroids):
        asteroid = Asteroid("Asteroid" + str(i))
        asteroid.position = Vector2(random.uniform(0, 1280), random.uniform(0, 720))
        Scene.main.Add(asteroid)

    SpawnPlayer()

def update(delta_time):

    global gScore
    global gLives

    Scene.main.Update(delta_time)

    collisions = Scene.main.CheckCollisionsBetweenTags("PlayerShip", "Asteroid")

    if (len(collisions) > 0):
        collisions[0].obj1.Explode()
        gLives = gLives - 1
        for collision in collisions:
            collision.obj2.Explode()

    collisions = Scene.main.CheckCollisionsBetweenTags("PlayerLaser", "Asteroid")
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

    screen.fill((5, 5, 15))

    Scene.main.Render(screen)

    FontManager.Write(screen, "Vector", str(gScore).zfill(6), (5, 5), (255, 255, 255))
    
    for i in range(0, gLives):
        WireMesh.DrawModel(screen, "PlayerShip", Vector2(i * 20 + 15, 45), 0, Vector2(0.5, 0.5))

    pygame.display.flip()

def SpawnPlayer():
    player = Scene.main.GetObjectByTag("PlayerShip")
    if (player == None):
        # Check if some asteroid is nearby
        circle = Circle2d(Vector2(640,320), 100)

        objects = Scene.main.GetObjectsInCollider("Asteroid", circle)

        if (len(objects) == 0):
            Scene.main.Add(PlayerShip("PlayerShip"))


def main():

    pygame.mixer.pre_init(44100, 16, 2, 1024)
    pygame.init()
    logo = pygame.image.load("sprites/icon.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Pysteroids")

    SoundManager.SetGlobalVolume(0.25)

    load_data()
    init_objects()

    screen = pygame.display.set_mode((1280, 720), pygame.DOUBLEBUF)

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

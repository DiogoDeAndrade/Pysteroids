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
from Scene import *

gSprites = dict()
gScene = Scene()

def load_data():
    WireMesh.LoadModel("models/player_ship.wm", "PlayerShip")

def init_objects():

    Scene.main.Add(PlayerShip("PlayerShip"))

    n_asteroids = 10

    for i in range(0,n_asteroids):
        asteroid = Asteroid("Asteroid" + str(i))
        asteroid.position = Vector2(random.uniform(0, 1280), random.uniform(0, 720))
        Scene.main.Add(asteroid)
        
def update(delta_time):

    Scene.main.Update(delta_time)

    player =  Scene.main.GetObjectByTag("PlayerShip")
    asteroids = Scene.main.GetObjectsByTag("Asteroid")

    collisions = Scene.main.CheckCollisionsBetweenTags("PlayerShip", "Asteroid")

    if (len(collisions) > 0):
        collisions[0].obj1.Explode()
        for collision in collisions:
            collision.obj2.Explode()

    collisions = Scene.main.CheckCollisionsBetweenTags("PlayerLaser", "Asteroid")
    if (len(collisions) > 0):
        for collision in collisions:
            collision.obj1.Destroy()
            collision.obj2.Explode()

def render(screen):

    screen.fill((10, 10, 30))

    Scene.main.Render(screen)

    pygame.display.flip()

def main():

    pygame.init()
    logo = pygame.image.load("sprites/icon.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Pysteroids")

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
            player = Scene.main.GetObjectByTag("PlayerShip")
            if (player == None):
                Scene.main.Add(PlayerShip("PlayerShip"))

        update(dt)
        render(screen)
        
        dt = time.time() - prev_time
        prev_time = time.time()
    
if __name__ == "__main__":
    main();

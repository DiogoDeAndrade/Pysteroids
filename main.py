import array
import pygame
import time
import random
from pygame.math import Vector2
from SpriteInfo import *
from WireMesh import *
from WireMeshExplosion import *
from GameDefs import *
from PlayerShip import *
from Asteroid import *

gSprites = dict()

def load_data():
    # Player sprites
    WireMesh.LoadModel("models/player_ship.wm", "PlayerShip")
    #gSprites["player"] = SpriteInfo()
    #gSprites["player"].LoadImage("sprites/player01.png", Vector2(128, 128))
    #gSprites["player"].LoadImage("sprites/player02.png", Vector2(128, 128))
    #gSprites["player"].LoadImage("sprites/player03.png", Vector2(128, 128))
    #gSprites["player"].LoadImage("sprites/player04.png", Vector2(128, 128))
    #gSprites["player"].LoadImage("sprites/player05.png", Vector2(128, 128))
    #gSprites["player"].Rescale(0.25)
    pass

def init_objects():

    global player
    global asteroids
    global fx

    player = PlayerShip("PlayerShip")
    asteroids = []
    for i in range(0,10):
        asteroid = Asteroid("Asteroid" + str(i))
        asteroid.position = Vector2(random.uniform(0, 1280), random.uniform(0, 720))
        asteroids.append(asteroid)

    fx = []
        
def update(delta_time):

    global player
    global asteroids
    global fx

    if (player != None):
        player.Update(delta_time)
    
    for asteroid in asteroids:
        asteroid.Update(delta_time)
        
        # Check collision with ship
        if (player != None):
            if (asteroid.Intersects(player)):
                fx.append(WireMeshExplosion(player.gfx, player.position, player.rotation, player.scale))
                player = None

    for e in fx:
        e.Update(delta_time)

    fx = [e for e in fx if e.IsAlive()]

def render(screen):

    global player
    global asteroids
    global fx

    screen.fill((10, 10, 30))

    if (player != None):
        player.Render(screen)

    for asteroid in asteroids:
        asteroid.Render(screen)

    for e in fx:
        e.Render(screen)

    pygame.display.flip()

def main():

    pygame.init()
    logo = pygame.image.load("sprites/icon.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Asteroids")

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

        update(dt)
        render(screen)
        
        dt = time.time() - prev_time
        prev_time = time.time()
    
if __name__ == "__main__":
    main();

import array
import pygame
import time
import random
from pygame.math import Vector2

from SpriteInfo import *
from WireMesh import *
from WireMeshExplosion import *
from Shockwave import *
from ParticleSystem import *
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
                explosion = WireMeshExplosion(player.gfx, player.position, player.rotation, player.scale, True, 150, 300, 0.5, 3)
                explosion.fadeMethod = FadeMethod.Color
                explosion.colors = [Color(1.0, 1.0, 0.0, 1.0), Color(1.0, 0.0, 0.0, 1.0), Color(0.0, 0.0, 0.0, 1.0), Color(0.0, 0.0, 0.0, 0.0)]
                explosion.duration = 2

                shockwave = Shockwave(player.position, 0.75, 200, [Color(1.0, 1.0, 0.0, 1.0), Color(1.0, 0.0, 0.0, 1.0), Color(0.0, 0.0, 0.0, 1.0), Color(0.0, 0.0, 0.0, 0.0)])

                particle_system = ParticleSystem(player.position)
                particle_system.colorOverTime = [Color(1.0, 1.0, 0.0, 1.0), Color(1.0, 0.0, 0.0, 1.0), Color(0.0, 0.0, 0.0, 1.0), Color(0.0, 0.0, 0.0, 0.0)]
                particle_system.startSpeed = (50, 100)
                particle_system.particleLife = (2, 4)
                particle_system.drag = 0.995
                particle_system.rate = 0
                particle_system.Spawn(50)

                fx.append(explosion)
                fx.append(shockwave)
                fx.append(particle_system)
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

    global player

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
        if (((keys[pygame.K_r]) and (keys[pygame.K_LSHIFT])) and (player == None)):
            player = PlayerShip("PlayerShip")

        update(dt)
        render(screen)
        
        dt = time.time() - prev_time
        prev_time = time.time()
    
if __name__ == "__main__":
    main();

import array
import pygame
import time
from pygame.math import Vector2
from SpriteInfo import *
from WireMesh import *
from GameDefs import *
from PlayerShip import *

gSprites = dict()
global player

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

    player = PlayerShip("PlayerShip")
        

#angle = 0

def update(delta_time):

    player.Update(delta_time)
    #global angle
    #angle = angle + delta_time

def render(screen):
    screen.fill((10, 10, 30))

    player.Render(screen)

    #global angle
    #pygame.draw.rect(screen, (255,0,0), (640 + 200 * math.sin(angle), 500, 40, 40), 2)
    
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

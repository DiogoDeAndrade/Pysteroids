import math
import random
import pygame
import enum
from Color import *
from Scene import *
from GameObject import *
from pygame import Vector2

class Emitter(enum.Enum): 
    Point = 0

class Particle:
    def __init__(self, position, velocity, life, color):
        self.position = self.old_position = position
        self.direction = velocity.normalize()
        self.speed = velocity.magnitude()
        self.life = life
        self.time = 0
        self.color = color        
        self.size = 1
    
class ParticleSystem(GameObject):
    def __init__(self, position):
        GameObject.__init__(self, "")

        self.position = position
        self.start_speed = (10, 20)
        self.particle_life = (1, 2)
        self.color_over_time = [(1,1,1,1),(0,0,0,0)]
        self.emitter = Emitter.Point
        self.rate = 10
        self.accumulated_time = 0
        self.duration = 0
        self.drag = 1.0
        self.time = 0

        self.particles = []

        self.tags.append("ParticleSystem");

    def update(self, delta_time):
        self.accumulated_time = self.accumulated_time + delta_time

        particles_to_spawn = (int)(math.floor(self.accumulated_time * self.rate))
        if (particles_to_spawn > 0):
            self.accumulated_time = self.accumulated_time - particles_to_spawn / self.rate
            self.spawn(particles_to_spawn)

        for particle in self.particles:
            particle.time = particle.time + delta_time
            t = particle.time / particle.life

            particle.speed = particle.speed * self.drag
            particle.old_position = particle.position
            particle.position = particle.position + particle.direction * particle.speed * delta_time
            particle.color = Color.interpolate_with_array(self.color_over_time, t)

        for index in range(len(self.particles)-1, -1, -1):
            if (self.particles[index].time > self.particles[index].life):
                del(self.particles[index])

        self.time = self.time + delta_time

        if (not self.is_alive()):
            Scene.main.remove(self)

    def render(self, screen):
        for particle in self.particles:
            pygame.draw.line(screen, particle.color.tuple(), particle.old_position, particle.position, (int)(particle.size))

    def spawn(self, particle_to_spawn):
        if (self.emitter == Emitter.Point):
            for i in range(0, particle_to_spawn):
                ang = random.uniform(0, math.pi * 2)
                v = Vector2(math.cos(ang), math.sin(ang))
                v = v * random.uniform(self.start_speed[0], self.start_speed[1])
                particle = Particle(self.position, v, random.uniform(self.particle_life[0], self.particle_life[1]), self.color_over_time[0])
                self.particles.append(particle)

    def is_alive(self):
        if (self.duration == 0):
            return True
        if (self.time > self.duration):
            if (len(self.particles) > 0):
                return False

        return True
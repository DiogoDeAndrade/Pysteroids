"""Simple particle system

Usage example:
```
    # Spawn a particle system at the given position
    particle_system = Engine.FX.ParticleSystem(self.position)
    # Sets the colors of the particles over time from yellow, to red to black
    particle_system.color_over_time = [Color(1.0, 1.0, 0.0, 1.0), Color(1.0, 0.0, 0.0, 1.0), Color(0.0, 0.0, 0.0, 1.0), Color(0.0, 0.0, 0.0, 0.0)]
    # Particles have a starting speed in the range of [50,100]
    particle_system.start_speed = (50, 100)
    # Particles last from 2 to 4 seconds
    particle_system.particle_life = (2, 4)
    # Particles will slow down over time. They slow down 0.5% each frame
    particle_system.drag = 0.995
    # Besides the initial burst, there will be no more particles spawned
    particle_system.rate = 0
    # Spawn 50 particles immediately
    particle_system.spawn(50)
```
"""
import math
import random
import pygame
import enum

from pygame import Vector2

from Engine import *
from Engine.Color import Color

class Emitter(enum.Enum): 
    """Emitter type"""
    Point = 0
    """Particles are emitted from a point, initial velocity is set to a random 2d vector"""

class Particle:
    """Structure for an individual particle"""
    def __init__(self, position, velocity, life, color):
        """       
        This is used by the particle system's emitter, should not be used directly

        Arguments:
            position {Vector2} -- Position of the particle

            velocity {Vector2} -- Velocity of the particle

            life {float} -- Life of the particle (in seconds)

            color {Color} -- Color of the particle
        """
        self.position = self.old_position = position
        self.direction = velocity.normalize()
        self.speed = velocity.magnitude()
        self.life = life
        self.time = 0
        self.color = color        
        self.size = 1
    
class ParticleSystem(GameObject):
    """ Base particle system class"""
    def __init__(self, position):
        """
        Arguments:
            position {Vector2} -- Position of the particle system
        """
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

        self.tags.append("ParticleSystem")

    def update(self, delta_time):
        """Updates the particle system and its particles
        
        Arguments:
            delta_time {float} -- Time to elapse (in seconds)
        """
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
        """Renders the particle system.

        Currently, it renders each particle as a line from the previous position to the new one, in the particle color, with the width encoded in the particle
        
        Arguments:
            screen {int} -- Display surface handle
        """
        for particle in self.particles:
            pygame.draw.line(screen, particle.color.tuple(), particle.old_position, particle.position, (int)(particle.size))

    def spawn(self, particle_to_spawn):
        """Spawns particles.

        This function should be used internally, unless you desire a burst-like effect.

        Arguments:
            particle_to_spawn {int} -- Number of particles to spawn
        """
        if (self.emitter == Emitter.Point):
            for i in range(0, particle_to_spawn):
                ang = random.uniform(0, math.pi * 2)
                v = Vector2(math.cos(ang), math.sin(ang))
                v = v * random.uniform(self.start_speed[0], self.start_speed[1])
                particle = Particle(self.position, v, random.uniform(self.particle_life[0], self.particle_life[1]), self.color_over_time[0])
                self.particles.append(particle)

    def is_alive(self):
        """Checks if the particle system is still alive, i.e. if there are no particles alive and the lifetime for it has run out
        
        Returns:
            bool -- True if the particle system is still alive
        """
        if (self.duration == 0):
            return True
        if (self.time > self.duration):
            if (len(self.particles) > 0):
                return False

        return True
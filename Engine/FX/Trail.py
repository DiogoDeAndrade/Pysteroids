import pygame

from Engine import *

class TrailParticle:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color
        self.time = 0

class Trail(GameObject):
    def __init__(self, name, duration, colorStart, colorEnd, width, target, mountpoint, tick_time):
        GameObject.__init__(self, name)

        self.duration = duration
        self.start_color = colorStart
        self.end_color = colorEnd
        self.width = width
        self.target = target
        self.mountpoint = mountpoint
        self.tick_time = self.tick = tick_time

        self.points = []

    def update(self, delta_time):

        for pt in self.points:
            pt.time = pt.time + delta_time
            pt.color = Color.interpolate(self.start_color, self.end_color, pt.time / self.duration).tuple()        

        for index in range(len(self.points)-1, -1, -1):
            if (self.points[index].time > self.duration):
                del(self.points[index])

        self.tick = self.tick + delta_time
        if (self.tick > self.tick_time):
            self.points.append(TrailParticle(self.target.get_mountpoint(self.mountpoint)[0], self.start_color))
            self.tick = 0
        elif (len(self.points) > 0):
            self.points[len(self.points) - 1].pos = self.target.get_mountpoint(self.mountpoint)[0]


    def render(self, screen):
        for i in range(0, len(self.points) - 1):
            c = self.points[i].color
            p1 = self.points[i].pos
            p2 = self.points[i + 1].pos
            pygame.draw.line(screen, c, p1, p2, self.width)

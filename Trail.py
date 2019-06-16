from GameObject import *
from Color import *
import pygame

class TrailParticle:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color
        self.time = 0

class Trail(GameObject):
    def __init__(self, name, duration, colorStart, colorEnd, width, target, mountpoint, tickTime):
        GameObject.__init__(self, name)

        self.duration = duration
        self.startColor = colorStart
        self.endColor = colorEnd
        self.width = width
        self.target = target
        self.mountpoint = mountpoint
        self.tickTime = self.tick = tickTime

        self.points = []

    def Update(self, delta_time):

        for pt in self.points:
            pt.time = pt.time + delta_time
            pt.color = Color.Interpolate(self.startColor, self.endColor, pt.time / self.duration).tuple()        

        for index in range(len(self.points)-1, -1, -1):
            if (self.points[index].time > self.duration):
                del(self.points[index])

        self.tick = self.tick + delta_time
        if (self.tick > self.tickTime):
            self.points.append(TrailParticle(self.target.GetMountpoint(self.mountpoint)[0], self.startColor))
            self.tick = 0
        elif (len(self.points) > 0):
            self.points[len(self.points) - 1].pos = self.target.GetMountpoint(self.mountpoint)[0]


    def Render(self, screen):
        for i in range(0, len(self.points) - 1):
            c = self.points[i].color
            p1 = self.points[i].pos
            p2 = self.points[i + 1].pos
            pygame.draw.line(screen, c, p1, p2, self.width)

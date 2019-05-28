import pygame
import math
from pygame.math import Vector2

class WireMesh:
    def __init__(self):
        self.vertex = []
        self.poly = []
        self.polyColor = []
        self.position = (0,0)
        self.rotation = 0
        self.scale = (1,1)
        self.dirty = True
        self.currentPoly = []

    def AddVertex(self, vertex):
        self.vertex.append(vertex)
        return len(self.vertex) - 1

    def BeginPoly(self):
        self.currentPoly = []
        self.currentPolyColor = (255, 255, 255)

    def AddVertexToPoly(self, index):
        self.currentPoly.append(index)

    def EndPoly(self):
        self.poly.append(self.currentPoly)
        self.polyColor.append(self.currentPolyColor)
        self.currentPoly = []
        self.currentPolyColor = (255, 255, 255)

    def SetPolyColor(self, color):
        self.currentPolyColor = color

    def Draw(self, screen):
        if (self.dirty):
            self.Rebuild()   

        for idx, poly in enumerate(self.poly):
            pointlist = [self.cacheVertex[i] for i in poly]
            pygame.draw.aalines(screen, self.polyColor[idx], True, pointlist)

    def DrawPRS(self, screen, position, rotation, scale, color):
        cacheVertex = [self.VertexTransformPRS(v, position,rotation, scale) for v in self.vertex]

        for idx, poly in enumerate(self.poly):
            pointlist = [cacheVertex[i] for i in poly]
            pygame.draw.aalines(screen, self.polyColor[idx], True, pointlist)

    def Rebuild(self):
        self.cacheVertex = [self.VertexTransform(v) for v in self.vertex]
        self.dirty = False

    def VertexTransform(self, vertex):
        a = math.radians(self.rotation)
        s = math.sin(a)
        c = math.cos(a)
        v = Vector2(vertex.x * self.scale.x, vertex.y * self.scale.y)
        v = Vector2(c * v.x - s * v.y, s * v.x + c * v.y)
        v = v + self.position

        return v

    def VertexTransformPRS(self, vertex, position, rotation, scale):
        a = math.radians(rotation)
        s = math.sin(a)
        c = math.cos(a)
        v = Vector2(vertex.x * scale.x, vertex.y * scale.y)
        v = Vector2(c * v.x - s * v.y, s * v.x + c * v.y)
        v = v + position

        return v

    def SetPosition(self, position):
        self.position = position
        self.dirty = True

    def SetRotation(self, rotation):
        self.rotation = rotation
        self.dirty = True

    def SetScale(self, scale):
        self.scale = scale
        self.dirty = True
    
    #-- Model Management --#
    models = dict()

    @staticmethod
    def LoadModel(filename, model_name = ""):
        newMesh = WireMesh()
        with open(filename, "rt") as file:
            str = "\n"
            while (str != ""):                
                str = str.strip()
                if (str == "polygon:"):
                    newMesh.BeginPoly()
                    exit = False
                    while (not exit):
                        str = file.readline().strip()
                        if (str.find(':') != -1):
                            if (str.find('color:') != -1):
                                newMesh.SetPolyColor(WireMesh.ReadColor(file))
                            elif (str.find('vertex:') != -1):
                                vertexExit = False
                                while (not vertexExit):
                                    str = file.readline().strip()
                                    if (str.find(':') != -1):                                        
                                        break
                                    elif (str == ""):
                                        vertexExit = True
                                    else:
                                        v = WireMesh.ParseVector2(str)
                                        newMesh.AddVertexToPoly(newMesh.AddVertex(v))
                                
                                if (not vertexExit):
                                    break
                        elif (str == ""):
                            exit = True

                    newMesh.EndPoly()

                    if (not exit):
                        # Left because I found a tag of something but polygons
                        continue

                # Only reach here if everything works fine (a bit convoluted, but lack of goto does this, and I don't want to use terminators on my file format)
                str = file.readline()

        if (model_name == ""):
            model_name = filename
        
        WireMesh.models[model_name] = newMesh        

    @staticmethod
    def ReadColor(file):
        str = file.readline()
        if (str == ""):
            return (255, 255, 255)
        str = str.strip().replace('(', '').replace(')', '')
        values = str.split(',')
        return (int(values[0]), int(values[1]), int(values[2]))

    @staticmethod
    def ParseVector2(str):
        if (str == ""):
            return (0, 0, 0)
        str = str.replace('(', '').replace(')', '')
        values = str.split(',')
        return Vector2(float(values[0]), float(values[1]))

    @staticmethod
    def GetModel(model_name):
        if (model_name in WireMesh.models):
            return WireMesh.models[model_name]

        return None

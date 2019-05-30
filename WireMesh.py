import pygame
import math
import random
import enum
from pygame.math import Vector2

class RenderMode(enum.Enum): 
    AntiAlias = 0
    Normal = 1

class PrimitiveType(enum.Enum):
    LineStrip = 0,
    LineList = 1
  
class WireMesh:
    def __init__(self):
        self.vertex = []
        self.poly = []
        self.polyColor = []
        self.position = Vector2(0,0)
        self.rotation = 0
        self.scale = Vector2(1,1)
        self.dirty = True
        self.currentPoly = []
        self.closed = True
        self.primitiveType = PrimitiveType.LineStrip
        self.renderMode = RenderMode.AntiAlias
        self.width = 1
        self.overrideColorEnable = False
        self.overrideColor = (255, 255, 255)

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

    def GetColor(self, polyIndex):
        if (self.overrideColorEnable):
            return self.overrideColor
                   
        return self.polyColor[polyIndex]

    def Draw(self, screen):
        if (self.dirty):
            self.Rebuild()   

        self.DrawProcessedVertex(screen, self.cacheVertex)
        
    def DrawPRS(self, screen, position, rotation, scale):
        cacheVertex = [self.VertexTransformPRS(v, position,rotation, scale) for v in self.vertex]

        self.DrawProcessedVertex(screen, cacheVertex)

    def DrawProcessedVertex(self, screen, cacheVertex):
        for idx, poly in enumerate(self.poly):
            pointlist = [cacheVertex[i] for i in poly]
            if (self.primitiveType == PrimitiveType.LineStrip):
                if (self.renderMode == RenderMode.AntiAlias):
                    pygame.draw.aalines(screen, self.GetColor(idx), self.closed, pointlist)
                else:
                    pygame.draw.lines(screen, self.GetColor(idx), self.closed, pointlist, self.width)
            elif (self.primitiveType == PrimitiveType.LineList):
                if (self.renderMode == RenderMode.AntiAlias):
                    for idx in range(0, len(pointlist), 2):
                        pygame.draw.aaline(screen, self.GetColor(idx), pointlist[idx], pointlist[idx + 1], False)
                else:
                    for idx in range(0, len(pointlist), 2):
                        pygame.draw.line(screen, self.GetColor(idx), pointlist[idx], pointlist[idx + 1], self.width)

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
    
    def GetRadius(self):
        maxDist = 0
        for v in self.vertex:
            maxDist = max(v.magnitude_squared(), maxDist)

        return math.sqrt(maxDist)

    def ApplyTransform(self):
        self.vertex = [self.VertexTransform(v) for v in self.vertex]
        self.dirty = True
        self.position = (0,0)
        self.rotation = 0
        self.scale = (1,1)

    def ConvertToLineList(self):
        if (self.primitiveType != PrimitiveType.LineStrip):
            print("Can't convert to line list: not a line strip!")
            return

        newVertex = []
        for polyId, p in enumerate(self.poly):
            newPoly = []
            for src in range(0, len(p)):
                oldId = p[src]
                newVertex.append(self.vertex[oldId])
                newPoly.append(len(newVertex) - 1)
                oldId = p[(src + 1) % len(p)]
                newVertex.append(self.vertex[oldId])
                newPoly.append(len(newVertex) - 1)
            self.poly[polyId] = newPoly
        self.vertex = newVertex
        self.primitiveType = PrimitiveType.LineList

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
    
    @staticmethod
    def Copy(src):
        mesh = WireMesh()
        mesh.vertex = src.vertex.copy()
        mesh.poly = src.poly.copy()
        mesh.polyColor = src.polyColor.copy()
        mesh.position = src.position
        mesh.rotation = src.rotation
        mesh.scale = src.scale
        mesh.dirty = True
        mesh.closed = src.closed
        mesh.primitiveType = src.primitiveType
        mesh.renderMode = src.renderMode
        mesh.width = src.width

        return mesh

    @staticmethod
    def Circle(sides, radius, variance, color):
        mesh = WireMesh()
        
        mesh.BeginPoly()
        mesh.SetPolyColor(color)

        angle = 0
        angleInc = math.pi * 2 / sides

        for i in range(1, sides):
            r = random.uniform(radius - variance, radius + variance)
            idx = mesh.AddVertex(Vector2(r * math.cos(angle), r * math.sin(angle)))
            mesh.AddVertexToPoly(idx)
            angle += angleInc

        mesh.EndPoly()

        return mesh
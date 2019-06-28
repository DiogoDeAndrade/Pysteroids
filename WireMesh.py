import pygame
import math
import random
import enum
import os
import json
from pygame.math import Vector2

class RenderMode(enum.Enum): 
    AntiAlias = 0
    Normal = 1

class PrimitiveType(enum.Enum):
    LineStrip = 0,
    LineList = 1
  
class WireMeshJSON:
    pass

class WireMesh:
    def __init__(self):
        self.name = ""
        self.vertex = []
        self.poly = []
        self.poly_color = []
        self.position = Vector2(0,0)
        self.rotation = 0
        self.scale = Vector2(1,1)
        self.dirty = True
        self.current_poly = []
        self.closed = True
        self.primitive_type = PrimitiveType.LineStrip
        self.render_mode = RenderMode.AntiAlias
        self.width = 1
        self.override_color_enable = False
        self.override_color = (255, 255, 255)
        self.mountpoints = dict()

    def to_JSON(self):
        out = WireMeshJSON()

        out.closed = self.closed
        if (self.primitive_type == PrimitiveType.LineStrip):
            out.primitive = "LineStrip"
        elif (self.primitive_type == PrimitiveType.LineList):
            out.primitive = "LineList"
        if (self.render_mode == RenderMode.Normal):
            out.render_mode = "Normal"
        elif (self.render_mode == RenderMode.AntiAlias):
            out.render_mode = "AntiAlias"
        out.lineWidth = self.width

        out.vertex = [ ]
        for vertex in self.vertex:
            out.vertex.append( (vertex.x, vertex.y) )

        out.polygons = [ ]
        idx = 0
        for polygon in self.poly:
            poly = dict()
            poly["color"] = self.poly_color[idx]
            poly["index"] = polygon
            idx = idx + 1        
            out.polygons.append(poly)

        out.mountpoints = dict()
        for name, mountpoint in self.mountpoints.items():
            mp = dict()
            mp["pos"] = (mountpoint[0][0],mountpoint[0][1])
            mp["dir"] = (mountpoint[1][0],mountpoint[1][1])
            out.mountpoints[name] = mp

        ret = dict()
        ret[self.name] = out

        return json.dumps(ret, default=lambda o: o.__dict__, indent=4)

    def from_JSON(self, data):
        self.closed = data["closed"]
        if (data["primitive"] == "LineStrip"):
            self.primitive_type = PrimitiveType.LineStrip
        elif (data["primitive"] == "LineList"):
            self.primitive_type = PrimitiveType.LineList
        if (data["render_mode"] == "Normal"):
            self.render_mode = RenderMode.Normal
        elif (data["render_mode"] == "AntiAlias"):
            self.render_mode = RenderMode.AntiAlias
        self.width = data["lineWidth"]

        self.vertex = []
        for v in data["vertex"]:
            self.vertex.append(Vector2(v[0], v[1]))

        self.poly = []
        self.poly_color = []

        for p in data["polygons"]:
            self.poly_color.append(p["color"])        
            self.poly.append(p["index"])

        self.mountpoints = dict()

        if ("mountpoints" in data):
            for name in data["mountpoints"]:
                self.mountpoints[name] = ( Vector2(data["mountpoints"][name]["pos"][0], data["mountpoints"][name]["pos"][1]), Vector2(data["mountpoints"][name]["dir"][0], data["mountpoints"][name]["dir"][1]))


    def add_vertex(self, vertex):
        self.vertex.append(vertex)
        return len(self.vertex) - 1

    def begin_poly(self):
        self.current_poly = []
        self.currentPolyColor = (255, 255, 255)

    def add_vertex_to_poly(self, index):
        self.current_poly.append(index)

    def end_poly(self):
        self.poly.append(self.current_poly)
        self.poly_color.append(self.currentPolyColor)
        self.current_poly = []
        self.currentPolyColor = (255, 255, 255)

    def set_poly_color(self, color):
        self.currentPolyColor = color

    def get_color(self, polyIndex):
        if (self.override_color_enable):
            return self.override_color
                   
        return self.poly_color[polyIndex]

    def add_mountpoint(self, name, pos, dir):
        self.mountpoints[name] = ( pos, dir )

    def add_mountpoint_pos(self, name, pos):
        if (name in self.mountpoints):
            self.mountpoints[name] = (pos, self.mountpoints[name][1])
        else:
            self.mountpoints[name] = ( pos, (0, 1) )

    def get_mountpoint(self, name):
        if (name in self.mountpoints):
            return self.vertex_transform(self.mountpoints[name][0]), vertex_transform_no_pos(self.mountpoints[name][1])

        return self.vertex_transform(Vector2(0,0)), vertex_transform(Vector2(0,1))

    def get_mountpointPRS(self, name, position, rotation, scale):
        if (name in self.mountpoints):
            return WireMesh.vertex_transformPRS(self.mountpoints[name][0], position, rotation, scale), WireMesh.vertex_transformPRS(self.mountpoints[name][1], Vector2(0,0), rotation, scale)

        return WireMesh.vertex_transformPRS(Vector2(0,0), position, rotation, scale), WireMesh.vertex_transformPRS(Vector2(0,1), Vector2(0,0), rotation, scale)

    def mountpoint_exists(self, name):
        if (name in self.mountpoints):
            return True

        return False

    def draw(self, screen):
        if (self.dirty):
            self.rebuild()   

        self.draw_processed_vertex(screen, self.cache_vertex)
        
    def drawPRS(self, screen, position, rotation, scale):
        cache_vertex = [WireMesh.vertex_transformPRS(v, position,rotation, scale) for v in self.vertex]

        self.draw_processed_vertex(screen, cache_vertex)

    def draw_processed_vertex(self, screen, cache_vertex):
        for idx, poly in enumerate(self.poly):
            pointlist = [cache_vertex[i] for i in poly]
            if (self.primitive_type == PrimitiveType.LineStrip):
                if (self.render_mode == RenderMode.AntiAlias):
                    pygame.draw.aalines(screen, self.get_color(idx), self.closed, pointlist)
                else:
                    pygame.draw.lines(screen, self.get_color(idx), self.closed, pointlist, (int)(self.width))
            elif (self.primitive_type == PrimitiveType.LineList):
                if (self.render_mode == RenderMode.AntiAlias):
                    for idx2 in range(0, len(pointlist), 2):
                        pygame.draw.aaline(screen, self.get_color(idx), pointlist[idx2], pointlist[idx2 + 1], False)
                else:
                    for idx2 in range(0, len(pointlist), 2):
                        pygame.draw.line(screen, self.get_color(idx), pointlist[idx2], pointlist[idx2 + 1], (int)(self.width))

    def rebuild(self):
        self.cache_vertex = [self.vertex_transform(v) for v in self.vertex]
        self.dirty = False

    def vertex_transform(self, vertex):
        return self.vertex_transform_no_pos(vertex) + self.position

    def vertex_transform_no_pos(self, vertex):
        a = math.radians(self.rotation)
        s = math.sin(a)
        c = math.cos(a)
        v = Vector2(vertex.x * self.scale.x, vertex.y * self.scale.y)
        v = Vector2(c * v.x - s * v.y, s * v.x + c * v.y)

        return v

    @staticmethod
    def vertex_transformPRS(vertex, position, rotation, scale):
        a = math.radians(rotation)
        s = math.sin(a)
        c = math.cos(a)
        v = Vector2(vertex.x * scale.x, vertex.y * scale.y)
        v = Vector2(c * v.x - s * v.y, s * v.x + c * v.y)
        v = v + position

        return v

    def set_position(self, position):
        self.position = position
        self.dirty = True

    def set_rotation(self, rotation):
        self.rotation = rotation
        self.dirty = True

    def set_scale(self, scale):
        self.scale = scale
        self.dirty = True
    
    def get_radius(self):
        maxDist = 0
        for v in self.vertex:
            maxDist = max(v.magnitude_squared(), maxDist)

        return math.sqrt(maxDist)

    def apply_transform(self):
        self.vertex = [self.vertex_transform(v) for v in self.vertex]
        self.dirty = True
        self.position = (0,0)
        self.rotation = 0
        self.scale = (1,1)

    def convert_to_unindexed_line_list(self):
        if (self.primitive_type == PrimitiveType.LineStrip):
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
        elif (self.primitive_type == PrimitiveType.LineList):
            newVertex = []
            for polyId, p in enumerate(self.poly):
                newPoly = []
                for src in range(0, len(p)):
                    oldId = p[src]
                    newVertex.append(self.vertex[oldId])
                    newPoly.append(len(newVertex) - 1)
                self.poly[polyId] = newPoly
            self.vertex = newVertex

        self.primitive_type = PrimitiveType.LineList

    def add_circle(self, sides, radius, variance, color, angular_offset = 0, center_pos = Vector2(0,0)):
        self.begin_poly()
        self.set_poly_color(color)

        angle = angular_offset
        angleInc = math.pi * 2 / sides
        r = radius

        for i in range(0, sides):
            if (variance > 0):
                r = random.uniform(radius - variance, radius + variance)                
            idx = self.add_vertex(center_pos + Vector2(r * math.cos(angle), r * math.sin(angle)))
            self.add_vertex_to_poly(idx)
            angle += angleInc

        self.end_poly()

    #-- Model Management --#
    models = dict()

    @staticmethod
    def load_model(filename, model_name = ""):
        just_filename, file_extension = os.path.splitext(filename)
        if (file_extension == ".wm"):
            return WireMesh.load_modelWM(filename, model_name)
        elif (file_extension == ".json"):
            return WireMesh.load_modelJSON(filename, model_name)
        
        return None
    
    @staticmethod
    def load_modelWM(filename, model_name):
        new_mesh = WireMesh()
        with open(filename, "rt") as file:
            str = "\n"
            while (str != ""):                
                str = str.strip()
                if (str == "polygon:"):
                    new_mesh.begin_poly()
                    exit = False
                    while (not exit):
                        str = file.readline().strip()
                        if (str.find(':') != -1):
                            if (str.find('color:') != -1):
                                new_mesh.set_poly_color(WireMesh.read_color(file))
                            elif (str.find('vertex:') != -1):
                                vertex_exit = False
                                while (not vertex_exit):
                                    str = file.readline().strip()
                                    if (str.find(':') != -1):                                        
                                        break
                                    elif (str == ""):
                                        vertex_exit = True
                                    else:
                                        v = WireMesh.parse_vector2(str)
                                        new_mesh.add_vertex_to_poly(new_mesh.add_vertex(v))
                                
                                if (not vertex_exit):
                                    break
                        elif (str == ""):
                            exit = True

                    new_mesh.end_poly()

                    if (not exit):
                        # Left because I found a tag of something but polygons
                        continue
                elif (str == "mountpoint:"):
                    exit = False
                    mountpoint_name = ""
                    while (not exit):
                        str = file.readline().strip()
                        if (str.find(':') != -1):
                            if (str.find('name:') != -1):
                                mountpoint_name = file.readline().strip()
                            elif (str.find('position:') != -1):
                                mountpoint_position = v = WireMesh.parse_vector2(file.readline().strip())
                                if (mountpoint_name != ""):
                                    new_mesh.add_mountpoint_pos(mountpoint_name, mountpoint_position)
                                    break
                        else:
                            exit = True

                    if (not exit):
                        # Left because I found a tag of something but polygons
                        continue

                # Only reach here if everything works fine (a bit convoluted, but lack of goto does this, and I don't want to use terminators on my file format)
                str = file.readline()

        if (model_name == ""):
            model_name = filename
        
        new_mesh.name = model_name
        WireMesh.models[model_name] = new_mesh    

        return new_mesh    

    @staticmethod
    def load_modelJSON(filename, model_name):
        ret = None

        text_file = open(filename, "rt")
        json_string = text_file.read()
        text_file.close()

        meshes = json.loads(json_string)

        for name in meshes:
            new_mesh = WireMesh()
            new_mesh.from_JSON(meshes[name])

            new_mesh.name = name
            WireMesh.models[name] = new_mesh

            if (ret == None):
                ret = new_mesh

        return ret

    @staticmethod
    def read_color(file):
        str = file.readline()
        if (str == ""):
            return (255, 255, 255)
        str = str.strip().replace('(', '').replace(')', '')
        values = str.split(',')
        return (int(values[0]), int(values[1]), int(values[2]))

    @staticmethod
    def parse_vector2(str):
        if (str == ""):
            return (0, 0, 0)
        str = str.replace('(', '').replace(')', '')
        values = str.split(',')
        return Vector2(float(values[0]), float(values[1]))

    @staticmethod
    def get_model(model_name):
        if (model_name in WireMesh.models):
            return WireMesh.models[model_name]

        return None
    
    @staticmethod
    def copy(src):
        mesh = WireMesh()
        mesh.vertex = src.vertex.copy()
        mesh.poly = src.poly.copy()
        mesh.poly_color = src.poly_color.copy()
        mesh.position = src.position
        mesh.rotation = src.rotation
        mesh.scale = src.scale
        mesh.dirty = True
        mesh.closed = src.closed
        mesh.primitive_type = src.primitive_type
        mesh.render_mode = src.render_mode
        mesh.width = src.width

        return mesh

    @staticmethod
    def circle(sides, radius, variance, color, angular_offset = 0, center_pos = Vector2(0,0)):
        mesh = WireMesh()

        mesh.add_circle(sides, radius, variance, color, angular_offset)

        return mesh

    @staticmethod
    def draw_model(screen, name, position, rotation, scale):
        WireMesh.models[name].drawPRS(screen, position, rotation, scale)
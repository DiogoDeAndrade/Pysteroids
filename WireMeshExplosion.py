
from WireMesh import *

class WireMeshExplosion:
    def __init__(self, original_mesh, original_pos, original_rotation, original_scale):
        # Create a copy of the mesh
        self.gfx = WireMesh.Copy(original_mesh)
        self.gfx.ApplyTransform()
        self.gfx.ConvertToLineList()
        self.gfx.overrideColorEnable = True
        self.gfx.overrideColor = (0, 255, 0)
        self.position = original_pos
        self.rotation = original_rotation
        self.scale = original_scale

    def Update(self, delta_time):
        pass

    def IsAlive(self):
        return True

    def Render(self, screen):
        self.gfx.DrawPRS(screen, self.position, self.rotation, self.scale)


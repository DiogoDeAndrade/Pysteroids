from WireMesh import *
from Ship import *
from Laser import *
from GameDefs import *
from Missile import *
from pygame.math import Vector2

class EnemyShip(Ship):
    def __init__(self, name):
        Ship.__init__(self, name)

        self.gfx = WireMesh.Circle(8, 40, 0, (255,0,255), angularOffset = math.pi * 0.125)
        self.gfx.AddCircle(8, 15, 0, (0, 255, 255), angularOffset = math.pi * 0.125)
        
        self.animatedGfx = WireMesh()
        for i in range(0, 4):
            pos = 30 * Vector2(math.cos(i * math.pi * 0.5), math.sin(i * math.pi * 0.5))
            self.animatedGfx.AddCircle(4, 5, 0, (255, 0, 255), angularOffset = math.pi * 0.25, centerPos = pos)

        self.collider = Circle2d(Vector2(0,0), self.gfx.GetRadius())
        self.radius = self.gfx.GetRadius()
        self.shot_cooldown = 1
        self.current_shot_cooldown = 0
        self.weapon = 0

        self.animatedGfxAngle = 0

        r = ((int)(random.uniform(0,100))) % 4
        if (r == 0):
            self.startPos = Vector2(1400, -120)
            self.targetPos = Vector2(-120, 840)
        elif (r == 1):
            self.startPos = Vector2(-120, -120)
            self.targetPos = Vector2(1400, 840)
        elif (r == 2):
            self.startPos = Vector2(1400, 840)
            self.targetPos = Vector2(-120, -120)
        elif (r == 3):
            self.startPos = Vector2(-120, 840)
            self.targetPos = Vector2(1400, -120)

        self.position = self.startPos
            
        self.patrolDuration = 20
        self.patrolTime = 0

        self.scoreToAdd = 200

        self.tags.append("EnemyShip")
        
    def Update(self, delta_time):

        self.current_shot_cooldown = self.current_shot_cooldown - delta_time
        if (self.current_shot_cooldown < 0):
            self.FireWeapon()

        self.animatedGfxAngle = self.animatedGfxAngle + delta_time * 180      

        self.patrolTime = self.patrolTime + delta_time
        if (self.patrolTime > self.patrolDuration):
            self.Destroy()
            return
        else:
            self.position = Vector2.lerp(self.startPos, self.targetPos, self.patrolTime / self.patrolDuration)

        Ship.Update(self, delta_time)

    def Render(self, screen):
        Ship.Render(self, screen)

        self.gfx.DrawPRS(screen, self.position, self.rotation, self.scale)
        self.animatedGfx.DrawPRS(screen, self.position, self.animatedGfxAngle, self.scale)

    def OnDestroy(self):
        GameObject.OnDestroy(self)

    def FireWeapon(self):
        if (self.weapon == 0):
            r = random.uniform(0,100)
            if (r < 50):
                dir = Vector2(0,1)
            else:
                dir = Vector2(1,0)

            Scene.main.Add(Laser("EnemyLaser", (255, 0, 0), 4, 20, self.position + dir * 40, dir * 400, 2))
            Scene.main.Add(Laser("EnemyLaser", (255, 0, 0), 4, 20, self.position - dir * 40, -dir * 400, 2))

            self.current_shot_cooldown = self.shot_cooldown
            SoundManager.Play("Laser", 0.15)
        elif (self.weapon == 1):
            player =  Scene.main.GetObjectByTag("PlayerShip")
            if (player != None):
                dir = player.position - self.position
                dir.normalize_ip()

                Scene.main.Add(Laser("EnemyLaser", (255, 0, 0), 4, 20, self.position + dir * 40, dir * 400, 2))

                self.current_shot_cooldown = self.shot_cooldown
                SoundManager.Play("Laser", 0.15)
        elif (self.weapon == 2):
            player =  Scene.main.GetObjectByTag("PlayerShip")
            if (player != None):
                missile = Missile("Missile", player, "EnemyMissile")
                missile.position = Vector2(self.position)

                Scene.main.Add(missile)

                self.current_shot_cooldown = self.shot_cooldown
                SoundManager.Play("Laser", 0.15)

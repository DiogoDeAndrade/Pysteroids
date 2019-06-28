from WireMesh import *
from Ship import *
from Laser import *
from GameDefs import *
from Missile import *
from pygame.math import Vector2

class EnemyShip(Ship):
    def __init__(self, name):
        Ship.__init__(self, name)

        self.gfx = WireMesh.circle(8, 40, 0, (255,0,255), angular_offset = math.pi * 0.125)
        self.gfx.add_circle(8, 15, 0, (0, 255, 255), angular_offset = math.pi * 0.125)
        
        self.animated_gfx = WireMesh()
        for i in range(0, 4):
            pos = 30 * Vector2(math.cos(i * math.pi * 0.5), math.sin(i * math.pi * 0.5))
            self.animated_gfx.add_circle(4, 5, 0, (255, 0, 255), angular_offset = math.pi * 0.25, center_pos = pos)

        self.collider = Circle2d(Vector2(0,0), self.gfx.get_radius())
        self.radius = self.gfx.get_radius()
        self.shot_cooldown = 1
        self.current_shot_cooldown = 0
        self.weapon = 0

        self.animated_gfx_angle = 0

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
            
        self.patrol_duration = 20
        self.patrol_time = 0

        self.score_to_add = 200

        self.tags.append("EnemyShip")
        
    def update(self, delta_time):

        self.current_shot_cooldown = self.current_shot_cooldown - delta_time
        if (self.current_shot_cooldown < 0):
            self.fire_weapon()

        self.animated_gfx_angle = self.animated_gfx_angle + delta_time * 180      

        self.patrol_time = self.patrol_time + delta_time
        if (self.patrol_time > self.patrol_duration):
            self.destroy()
            return
        else:
            self.position = Vector2.lerp(self.startPos, self.targetPos, self.patrol_time / self.patrol_duration)

        Ship.update(self, delta_time)

    def render(self, screen):
        Ship.render(self, screen)

        self.gfx.drawPRS(screen, self.position, self.rotation, self.scale)
        self.animated_gfx.drawPRS(screen, self.position, self.animated_gfx_angle, self.scale)

    def on_destroy(self):
        GameObject.on_destroy(self)

    def fire_weapon(self):
        if (self.weapon == 0):
            r = random.uniform(0,100)
            if (r < 50):
                dir = Vector2(0,1)
            else:
                dir = Vector2(1,0)

            Scene.main.add(Laser("EnemyLaser", (255, 0, 0), 4, 20, self.position + dir * 40, dir * 400, 2))
            Scene.main.add(Laser("EnemyLaser", (255, 0, 0), 4, 20, self.position - dir * 40, -dir * 400, 2))

            self.current_shot_cooldown = self.shot_cooldown
            SoundManager.play("Laser", 0.15)
        elif (self.weapon == 1):
            player =  Scene.main.get_object_by_tag("PlayerShip")
            if (player != None):
                dir = player.position - self.position
                dir.normalize_ip()

                Scene.main.add(Laser("EnemyLaser", (255, 0, 0), 4, 20, self.position + dir * 40, dir * 400, 2))

                self.current_shot_cooldown = self.shot_cooldown
                SoundManager.play("Laser", 0.15)
        elif (self.weapon == 2):
            player =  Scene.main.get_object_by_tag("PlayerShip")
            if (player != None):
                missile = Missile("Missile", player, "EnemyMissile")
                missile.position = Vector2(self.position)

                Scene.main.add(missile)

                self.current_shot_cooldown = self.shot_cooldown
                SoundManager.play("Laser", 0.15)

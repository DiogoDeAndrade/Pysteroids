from Collider2d import *

class Scene:
    main = None
    
    def __init__(self):
        if (Scene.main == None):
            Scene.main = self        
        self.update = []
        self.render = []
        self.objects = []
        self.objectsByTag = dict()

    def Add(self, gameObject):
        # Check if object has method Update
        update_method = getattr(gameObject, "Update", None)
        if (callable(update_method)):
            self.update.append(gameObject)

        # Check if object has method Render
        render_method = getattr(gameObject, "Render", None)
        if (callable(render_method)):
            self.render.append(gameObject)

        self.objects.append(gameObject)

        tags = gameObject.tags

        for tag in tags:
            if (not tag in self.objectsByTag):
                self.objectsByTag[tag] = []

            self.objectsByTag[tag].append(gameObject)

    def Remove(self, gameObject):
        try:
            self.update.remove(gameObject)
        except ValueError:
            pass

        try:
            self.render.remove(gameObject)
        except ValueError:
            pass

        try:
            self.objects.remove(gameObject)
        except ValueError:
            pass

        tags = gameObject.tags

        for tag in tags:
            if (tag in self.objectsByTag):
                try:
                    self.objectsByTag[tag].remove(gameObject)
                except valueError:
                    pass

    def GetObjectByTag(self, tag):
        if (tag in self.objectsByTag):
            elements = self.objectsByTag[tag]
            if (len(elements) > 0):
                return elements[0]
            
            return None

        return None

    def GetObjectsByTag(self, tag):
        if (tag in self.objectsByTag):
            return self.objectsByTag[tag]

        return []

    def Update(self, delta_time):
        for updatable_object in self.update:
            updatable_object.Update(delta_time)

    def Render(self, screen):
        for renderable_object in self.render:
            renderable_object.Render(screen)

    def CheckCollisionsBetweenTags(self, tag1, tag2):
        objects1 = self.GetObjectsByTag(tag1)
        objects2 = self.GetObjectsByTag(tag2)

        collisions = []

        for obj1 in objects1:
            for obj2 in objects2:
                if (obj1.Intersects(obj2)):
                    collisions.append(Collision2d(obj1, obj2))

        return collisions

    def GetObjectsInCollider(self, tag, collider):
        objects = self.GetObjectsByTag(tag)

        ret = [] 

        for obj in objects:
            if (obj.Intersects(collider)):
                ret.append(obj)

        return ret

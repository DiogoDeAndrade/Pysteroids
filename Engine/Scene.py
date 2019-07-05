from Engine.Collider2d import *

class Scene:
    main = None
    
    def __init__(self):
        if (Scene.main == None):
            Scene.main = self        
        self.update_objects = []
        self.render_objects = []
        self.objects = []
        self.objects_by_tag = dict()

    def add(self, game_object):
        # Check if object has method Update
        update_method = getattr(game_object, "update", None)
        if (callable(update_method)):
            self.update_objects.append(game_object)

        # Check if object has method Render
        render_method = getattr(game_object, "render", None)
        if (callable(render_method)):
            self.render_objects.append(game_object)

        self.objects.append(game_object)

        tags = game_object.tags

        for tag in tags:
            if (not tag in self.objects_by_tag):
                self.objects_by_tag[tag] = []

            self.objects_by_tag[tag].append(game_object)

    def clear(self):
        self.update_objects = []
        self.render_objects = []
        self.objects = []
        self.objects_by_tag = dict()

    def remove(self, game_object):
        try:
            self.update_objects.remove(game_object)
        except ValueError:
            pass

        try:
            self.render_objects.remove(game_object)
        except ValueError:
            pass

        try:
            self.objects.remove(game_object)
        except ValueError:
            pass

        tags = game_object.tags

        for tag in tags:
            if (tag in self.objects_by_tag):
                try:
                    self.objects_by_tag[tag].remove(game_object)
                except ValueError:
                    pass

    def get_object_by_tag(self, tag):
        if (tag in self.objects_by_tag):
            elements = self.objects_by_tag[tag]
            if (len(elements) > 0):
                return elements[0]
            
            return None

        return None

    def get_objects_by_tag(self, tags):
        if (isinstance(tags, list)):
            objects = []
            for tag in tags:
                if (tag in self.objects_by_tag):
                    objects.extend(self.objects_by_tag[tag])
            return objects

        if (tags in self.objects_by_tag):
            return self.objects_by_tag[tags]

        return []

    def update(self, delta_time):
        for updatable_object in self.update_objects:
            updatable_object.update(delta_time)

    def render(self, screen):
        for renderable_object in self.render_objects:
            renderable_object.render(screen)

    def check_collisions_between_tags(self, tags1, tags2):
        objects1 = self.get_objects_by_tag(tags1)
        objects2 = self.get_objects_by_tag(tags2)

        collisions = []

        for obj1 in objects1:
            for obj2 in objects2:
                if (obj1.intersects(obj2)):
                    collisions.append(Collision2d(obj1, obj2))

        return collisions

    def get_objects_in_collider(self, tag, collider):
        objects = self.get_objects_by_tag(tag)

        ret = [] 

        for obj in objects:
            if (obj.intersects(collider)):
                ret.append(obj)

        return ret

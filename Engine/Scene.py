"""Scene class implementation.

Scenes manage a collection of GameObjects.
"""
from Engine.Collider2d import *

class Scene:
    """Scene base object"""
    main = None
    """Currently active scene. All new objects should be added to this scene.
    """
    
    def __init__(self):
        if (Scene.main == None):
            Scene.main = self        
        self.update_objects = []
        self.render_objects = []
        self.objects = []
        self.objects_by_tag = dict()

    def add(self, game_object):
        """Adds an object to the scene.

        This function will check the given object has an update and render method, and add the object to the correct lists.

        It also adds the object to the right lists of objects, considering its tags.
        
        Arguments:
            game_object {GameObject} -- GameObject to add to scene.
        """
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
        """Clears a scene
        """
        self.update_objects = []
        self.render_objects = []
        self.objects = []
        self.objects_by_tag = dict()

    def remove(self, game_object):
        """Removes a GameObject from this scene"
        
        Arguments:
            game_object {GameObject} -- GameObject to remove from the scene
        """
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
        """Returns the first object that matches a certain tag, or None otherwise
        
        Arguments:
            tag {string} -- Tag to check
        
        Returns:
            GameObject -- First object that matches the given tag.
        """
        if (tag in self.objects_by_tag):
            elements = self.objects_by_tag[tag]
            if (len(elements) > 0):
                return elements[0]
            
            return None

        return None

    def get_objects_by_tag(self, tags):
        """Returns all objects that match the given tags.

        tags can be either a single string, or an array of strings.
        
        Arguments:
            tags {string / string[]} -- Tag or tags to match
        
        Returns:
            GameObject[] -- List of GameObjects that match the given tags.
        """
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
        """Updates all the GameObjects that have an update method.
        
        Arguments:
            delta_time {float} -- Time since the last frame, in seconds.
        """
        for updatable_object in self.update_objects:
            updatable_object.update(delta_time)

    def render(self, screen):
        """Renders all the GameObjects that have a render method.
        
        Arguments:
            screen {int} -- Display surface handle
        """
        for renderable_object in self.render_objects:
            renderable_object.render(screen)

    def check_collisions_between_tags(self, tags1, tags2):
        """Checks all the collisions between objects that match the given tags.

        All the objects that have any of the tags1 are matched with all the objects that have any of the tags2, and collisions are returned.
        
        Arguments:
            tags1 {string / string[]} -- Tags to check

            tags2 {string / string[]} -- Tags to check
        
        Returns:
            Collision2d[] -- All collisions detected.
        """
        objects1 = self.get_objects_by_tag(tags1)
        objects2 = self.get_objects_by_tag(tags2)

        collisions = []

        for obj1 in objects1:
            for obj2 in objects2:
                if (obj1.intersects(obj2)):
                    collisions.append(Collision2d(obj1, obj2))

        return collisions

    def get_objects_in_collider(self, tag, collider):
        """Returns all the objects that are intersecting the given collider.
        
        Arguments:
            tag {string / string[]} -- Tags to match to the objects
            
            collider {Collider2d} -- Collider to check
        
        Returns:
            GameObject[] -- Objects that are intersecting the given collider.
        """

        objects = self.get_objects_by_tag(tag)

        ret = [] 

        for obj in objects:
            if (obj.intersects(collider)):
                ret.append(obj)

        return ret

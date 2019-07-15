"""Lightweight simple game engine

This engine takes care of some objects, effects and collision detection.

The structure is built around the idea of Screens. Screens can have several Scenes, although only one is active.

Scenes are collection of GameObjects, which in turn implement a update and a render method.

"""
from Engine.GameObject import *
from Engine.Screen import *
from Engine.Scene import *
from Engine.WireMesh import *
from Engine.SoundManager import *
from Engine.FontManager import *
from Engine.Collider2d import *
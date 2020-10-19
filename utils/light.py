"""
---------------------------------------------------------------------------------------------------
	Author:
	Francisco Rosal 18676
---------------------------------------------------------------------------------------------------
"""

from utils.color import Color
from utils.glmath import div, frobeniusNorm


class AmbientLight(object):
    def __init__(self, strength = 0, _color = Color.white()):
        self.color = _color
        self.strength = strength

class PointLight(object):
    def __init__(self, position = (0,0,0), _color = Color.white(), intensity = 1):
        self.color = _color
        self.position = position
        self.intensity = intensity

class DirectionalLight(object):
     def __init__(self, direction = (0,-1,0), _color = Color.white(), intensity = 1):
        self.direction = div(direction, frobeniusNorm(direction)) 
        self.intensity = intensity
        self.color = _color
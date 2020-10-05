"""
---------------------------------------------------------------------------------------------------
	Author:
	Francisco Rosal 18676
---------------------------------------------------------------------------------------------------
"""

from utils.color import Color


class AmbientLight(object):
    def __init__(self, strength = 0, _color = Color.white()):
        self.color = _color
        self.strength = strength

class PointLight(object):
    def __init__(self, position = (0,0,0), _color = Color.white(), intensity = 1):
        self.color = _color
        self.position = position
        self.intensity = intensity

from utils.color import Color

class AmbientLight(object):
    def __init__(self, strength = 0, _color = Color.white()):
        self.strength = strength
        self.color = _color

class PointLight(object):
    def __init__(self, position = (0,0,0), _color = Color.white(), intensity = 1):
        self.position = position
        self.intensity = intensity
        self.color = _color

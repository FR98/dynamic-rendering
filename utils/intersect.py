"""
---------------------------------------------------------------------------------------------------
	Author:
	Francisco Rosal 18676
---------------------------------------------------------------------------------------------------
"""


class Intersect(object):
    def __init__(self, distance, point, normal, textCoords, sceneObject):
        self.point = point
        self.normal = normal
        self.distance = distance
        self.sceneObject = sceneObject
        self.textCoords = textCoords

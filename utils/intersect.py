"""
---------------------------------------------------------------------------------------------------
	Author:
	Francisco Rosal 18676
---------------------------------------------------------------------------------------------------
"""


class Intersect(object):
    def __init__(self, distance, point, normal, sceneObject):
        self.point = point
        self.normal = normal
        self.distance = distance
        self.sceneObject = sceneObject

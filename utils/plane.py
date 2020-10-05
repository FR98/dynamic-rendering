"""
---------------------------------------------------------------------------------------------------
	Author:
	Francisco Rosal 18676
---------------------------------------------------------------------------------------------------
"""

from utils.intersect import Intersect
from utils.glmath import sub, dot, frobeniusNorm, suma, mulEscalarVector, div


class Plane(object):

    def __init__(self, position, normal, material):
        self.position = position
        self.material = material
        self.normal = div(normal, frobeniusNorm(normal))

    def ray_intersect(self, orig, dirr):
        denom = dot(dirr, self.normal)

        if abs(denom) > 0.0001:
            t = dot(self.normal, sub(self.position, orig)) / denom

            if t > 0:
                hit = suma(orig, mulEscalarVector(t, dirr))

                return Intersect(
                    distance = t,
                    point = hit,
                    normal = self.normal,
                    sceneObject = self
                )

        return None

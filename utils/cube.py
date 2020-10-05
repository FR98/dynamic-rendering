"""
---------------------------------------------------------------------------------------------------
	Author:
	Francisco Rosal 18676
---------------------------------------------------------------------------------------------------
"""

from utils.plane import Plane
from utils.intersect import Intersect
from utils.glmath import sub, dot, frobeniusNorm, suma, mulEscalarVector, div, vector

class AABB(object):

    def __init__(self, position, size, material):
        self.size = size
        self.planes = []
        self.position = position
        self.material = material

        halfSize = size / 2

        self.planes.append(Plane(suma(position, vector(halfSize, 0, 0)),  vector(1, 0, 0),    material))
        self.planes.append(Plane(suma(position, vector(-halfSize, 0, 0)), vector(-1, 0, 0),   material))
        self.planes.append(Plane(suma(position, vector(0, halfSize, 0)),  vector(0, 1, 0),    material))
        self.planes.append(Plane(suma(position, vector(0, -halfSize, 0)), vector(0, -1, 0),   material))
        self.planes.append(Plane(suma(position, vector(0, 0, halfSize)),  vector(0, 0, 1),    material))
        self.planes.append(Plane(suma(position, vector(0, 0, -halfSize)), vector(0, 0, -1),   material))


    def ray_intersect(self, orig, dirr):
        epsilon = 0.001
        boundsMin = vector('0', '0', '0')
        boundsMax = vector('0', '0', '0')

        for i in ['x', 'y', 'z']:
            boundsMin[i] = self.position[i] - (epsilon + self.size / 2)
            boundsMax[i] = self.position[i] + (epsilon + self.size / 2)

        t = float('inf')
        intersect = None

        for plane in self.planes:
            planeInter = plane.ray_intersect(orig, dirr)

            if planeInter is not None:
                if planeInter.point['x'] >= boundsMin['x'] and planeInter.point['x'] <= boundsMax['x']:
                    if planeInter.point['y'] >= boundsMin['y'] and planeInter.point['y'] <= boundsMax['y']:
                        if planeInter.point['z'] >= boundsMin['z'] and planeInter.point['z'] <= boundsMax['z']:
                            if planeInter.distance < t:
                                t = planeInter.distance
                                intersect = planeInter

        if intersect is None:
            return None

        return Intersect(
            distance = intersect.distance,
            point = intersect.point,
            normal = intersect.normal,
            sceneObject = self
        )

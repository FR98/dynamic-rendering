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

        halfSize = div(size, 2)

        self.planes.append(Plane(suma(position, vector(halfSize['x'], 0, 0)),  vector(1, 0, 0),    material))
        self.planes.append(Plane(suma(position, vector(-halfSize['x'], 0, 0)), vector(-1, 0, 0),   material))
        self.planes.append(Plane(suma(position, vector(0, halfSize['y'], 0)),  vector(0, 1, 0),    material))
        self.planes.append(Plane(suma(position, vector(0, -halfSize['y'], 0)), vector(0, -1, 0),   material))
        self.planes.append(Plane(suma(position, vector(0, 0, halfSize['z'])),  vector(0, 0, 1),    material))
        self.planes.append(Plane(suma(position, vector(0, 0, -halfSize['z'])), vector(0, 0, -1),   material))


    def ray_intersect(self, orig, dirr):
        epsilon = 0.001
        boundsMin = vector('0', '0', '0')
        boundsMax = vector('0', '0', '0')

        for i in ['x', 'y', 'z']:
            boundsMin[i] = self.position[i] - (epsilon + self.size[i] / 2)
            boundsMax[i] = self.position[i] + (epsilon + self.size[i] / 2)

        t = float('inf')
        intersect = None
        uvs = None

        for plane in self.planes:
            planeInter = plane.ray_intersect(orig, dirr)

            if planeInter is not None:
                if planeInter.point['x'] >= boundsMin['x'] and planeInter.point['x'] <= boundsMax['x']:
                    if planeInter.point['y'] >= boundsMin['y'] and planeInter.point['y'] <= boundsMax['y']:
                        if planeInter.point['z'] >= boundsMin['z'] and planeInter.point['z'] <= boundsMax['z']:
                            if planeInter.distance < t:
                                t = planeInter.distance
                                intersect = planeInter

                                if abs(plane.normal['x']) > 0:
                                    u = (planeInter.point['y'] - boundsMin['y']) / (boundsMax['y'] - boundsMin['y'])
                                    v = (planeInter.point['z'] - boundsMin['z']) / (boundsMax['z'] - boundsMin['z'])

                                elif abs(plane.normal['y']) > 0:
                                    u = (planeInter.point['x'] - boundsMin['x']) / (boundsMax['x'] - boundsMin['x'])
                                    v = (planeInter.point['z'] - boundsMin['z']) / (boundsMax['z'] - boundsMin['z'])

                                elif abs(plane.normal['z']) > 0:
                                    u = (planeInter.point['x'] - boundsMin['x']) / (boundsMax['x'] - boundsMin['x'])
                                    v = (planeInter.point['y'] - boundsMin['y']) / (boundsMax['y'] - boundsMin['y'])

                                uvs = [u, v]

        if intersect is None:
            return None

        return Intersect(
            distance = intersect.distance,
            point = intersect.point,
            normal = intersect.normal,
            textCoords = uvs,
            sceneObject = self
        )

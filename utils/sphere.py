from utils.intersect import Intersect
from utils.glmath import sub, dot, frobeniusNorm, suma, mulEscalarVector, div

class Sphere(object):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def ray_intersect(self, orig, dirr):
        L = sub(self.center, orig)
        tca = dot(L, dirr)
        l = frobeniusNorm(L)
        d = (l ** 2 - tca ** 2) ** 0.5
        if d > self.radius:
            return None

        thc = (self.radius ** 2 - d ** 2) ** 0.5
        t0 = tca - thc
        t1 = tca + thc
        if t0 < 0:
            t0 = t1

        if t0 < 0:
            return None

        hit = suma(orig, mulEscalarVector(t0, dirr))
        norm = sub(hit, self.center)
        norm = div(norm, frobeniusNorm(norm))

        return Intersect(
            distance = t0,
            point = hit,
            normal = norm,
            sceneObject = self
        )

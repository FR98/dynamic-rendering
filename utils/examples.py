"""
---------------------------------------------------------------------------------------------------
	Author:
	Francisco Rosal 18676
---------------------------------------------------------------------------------------------------
"""

from gl import Raytracer
from utils.cube import AABB
from utils.plane import Plane
from utils.color import Color
from utils.sphere import Sphere
from utils.material import Material
from obj import Obj, Texture, Envmap
from utils.light import PointLight, AmbientLight


def dr():
    white_snow = Material(diffuse = Color.color(1, 0.98, 0.98), spec = 96)
    black = Material(diffuse = Color.color(0, 0, 0), spec = 96)
    orange_carrot = Material(diffuse = Color.color(0.92, 0.54, 0.13), spec = 96)
    white = Material(diffuse = Color.color(1, 1, 1), spec = 96)
    gray = Material(diffuse = Color.color(0.22, 0.22, 0.22), spec = 96)
    darkblue = Material(diffuse = Color.color(0.031, 0.255, 0.361), spec = 64)

    rayTracer = Raytracer(500, 500)
    rayTracer.pointLight = PointLight(position = Raytracer.vector(0, 0, 0), intensity = 1)
    rayTracer.ambientLight = AmbientLight(strength = 0.1)

    # Cuarto
    # Techo
    rayTracer.scene.append(Plane(Raytracer.vector(0, 5, 0), Raytracer.vector(0, -1, 0), black))
    # Suelo
    rayTracer.scene.append(Plane(Raytracer.vector(0, -5, 0), Raytracer.vector(0, 1, 0), gray))
    # Pared atras
    rayTracer.scene.append(Plane(Raytracer.vector(0, 0, -15), Raytracer.vector(0, 0, 1), gray))
    # Pared izquierda
    rayTracer.scene.append(Plane(Raytracer.vector(-5, 0, 0), Raytracer.vector(1, 0, 0), gray))
    # Pared derecha
    rayTracer.scene.append(Plane(Raytracer.vector(5, 0, 0), Raytracer.vector(-1, 0, 0), gray))

    # Cubos
    rayTracer.scene.append(AABB(Raytracer.vector(-1, -2, -7), 1.5, darkblue))
    rayTracer.scene.append(AABB(Raytracer.vector(1, -2, -7), 1.5, orange_carrot))

    rayTracer.rtRender()
    rayTracer.glFinish('output/dr3.bmp')

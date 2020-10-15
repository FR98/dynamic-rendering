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
from utils.material import Material, TRANSPARENT, REFLECTIVE
from obj import Obj, Texture, Envmap
from utils.light import PointLight, AmbientLight, DirectionalLight


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


def proyecto():
    wood = Material(diffuse = Color.color(0.32, 0.21, 0.04), spec = 96)
    grass = Material(diffuse = Color.color(0.26, 0.42, 0.18), spec = 96)
    water = Material(diffuse = Color.color(0.031, 0.255, 0.361), spec = 50, ior = 1.5, matType = REFLECTIVE)

    rayTracer = Raytracer(500, 500)
    rayTracer.pointLight = PointLight(position = Raytracer.vector(0, 0, 0), intensity = 1)
    rayTracer.pointLight = PointLight(position = Raytracer.vector(0, 1, 0), intensity = 1)
    rayTracer.ambientLight = AmbientLight(strength = 0.1)
    rayTracer.dirLight = DirectionalLight(direction = rayTracer.vector(1, -1, -2), intensity = 0.5)
    rayTracer.envmap = Envmap('assets/unnamed.bmp')

    # Suelo
    rayTracer.scene.append(Plane(Raytracer.vector(0, -5, 0), Raytracer.vector(0, 1, 0), grass))

    # Agua
    rayTracer.scene.append(AABB(Raytracer.vector(-5, -5, -10), Raytracer.vector(7, 0.2, 5), water))
    # Suelo
    rayTracer.scene.append(AABB(Raytracer.vector(-1, -4, -19), Raytracer.vector(20, 1, 10), grass))
    rayTracer.scene.append(AABB(Raytracer.vector(3, -3, -21), Raytracer.vector(17, 1, 10), grass))
    rayTracer.scene.append(AABB(Raytracer.vector(6, -2, -23), Raytracer.vector(15, 1, 10), grass))
    # Casa
    rayTracer.scene.append(AABB(Raytracer.vector(9, 0, -25), Raytracer.vector(10, 10, 10), wood))

    # Creeper
    # Steve

    rayTracer.rtRender()
    rayTracer.glFinish('output/dr3.bmp')

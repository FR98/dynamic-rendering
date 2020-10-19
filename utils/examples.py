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
    wood = Material(texture=Texture('assets/wood.bmp'))
    white_snow = Material(diffuse = Color.color(1, 0.98, 0.98), spec = 96)
    grass = Material(diffuse = Color.color(0.26, 0.42, 0.18), spec = 96)
    water = Material(diffuse = Color.color(0.031, 0.255, 0.361), spec = 50, ior = 1.5, matType = REFLECTIVE)
    darkblue = Material(diffuse = Color.color(0.031, 0.255, 0.361), spec = 64)
    playera = Material(diffuse = Color.color(0.2, 0.86, 0.85), spec = 64)
    piel = Material(diffuse = Color.color(0.85, 0.71, 0.45), spec = 64)
    cafe = Material(diffuse = Color.color(0.32, 0.24, 0.08), spec = 64)
    window = Material(spec = 40, ior = 1.5, matType = TRANSPARENT)

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
    # Ventana
    rayTracer.scene.append(AABB(Raytracer.vector(8, 2, -25), Raytracer.vector(5, 3, 11), window))

    # Steve
    # =======================
    # Piernas
    rayTracer.scene.append(AABB(Raytracer.vector(2, -4, -10), Raytracer.vector(0.5, 1.5, 0.5), darkblue))
    rayTracer.scene.append(AABB(Raytracer.vector(2.6, -4, -10), Raytracer.vector(0.5, 1.5, 0.5), darkblue))
    # Playera
    rayTracer.scene.append(AABB(Raytracer.vector(2.3, -2.5, -10), Raytracer.vector(1.1, 1.5, 0.5), playera))
    rayTracer.scene.append(AABB(Raytracer.vector(1.5, -2, -10), Raytracer.vector(0.5, 0.5, 0.5), playera))
    rayTracer.scene.append(AABB(Raytracer.vector(3.1, -2, -10), Raytracer.vector(0.5, 0.5, 0.5), playera))
    # Brazos
    rayTracer.scene.append(AABB(Raytracer.vector(1.5, -2.75, -10), Raytracer.vector(0.5, 1, 0.5), piel))
    rayTracer.scene.append(AABB(Raytracer.vector(3.1, -2.75, -10), Raytracer.vector(0.5, 1, 0.5), piel))
    # Cabeza
    rayTracer.scene.append(AABB(Raytracer.vector(2.3, -1.3, -10), Raytracer.vector(1.1, 0.9, 1), piel))
    # Pelo
    rayTracer.scene.append(AABB(Raytracer.vector(2.3, -0.75, -10), Raytracer.vector(1.1, 0.2, 1), cafe))
    # Ojos
    rayTracer.scene.append(AABB(Raytracer.vector(2.1, -1.2, -9.5), Raytracer.vector(0.1, 0.1, 0.2), cafe))
    rayTracer.scene.append(AABB(Raytracer.vector(2, -1.2, -9.5), Raytracer.vector(0.1, 0.1, 0.2), white_snow))
    rayTracer.scene.append(AABB(Raytracer.vector(2.5, -1.2, -9.5), Raytracer.vector(0.1, 0.1, 0.2), cafe))
    rayTracer.scene.append(AABB(Raytracer.vector(2.6, -1.2, -9.5), Raytracer.vector(0.1, 0.1, 0.2), white_snow))
    # Boca
    rayTracer.scene.append(AABB(Raytracer.vector(2.1, -1.4, -9.5), Raytracer.vector(0.1, 0.1, 0.2), cafe))
    rayTracer.scene.append(AABB(Raytracer.vector(2.1, -1.5, -9.5), Raytracer.vector(0.1, 0.1, 0.2), cafe))
    rayTracer.scene.append(AABB(Raytracer.vector(2.5, -1.4, -9.5), Raytracer.vector(0.1, 0.1, 0.2), cafe))
    rayTracer.scene.append(AABB(Raytracer.vector(2.5, -1.5, -9.5), Raytracer.vector(0.1, 0.1, 0.2), cafe))
    rayTracer.scene.append(AABB(Raytracer.vector(2.2, -1.5, -9.5), Raytracer.vector(0.1, 0.1, 0.2), cafe))
    rayTracer.scene.append(AABB(Raytracer.vector(2.3, -1.5, -9.5), Raytracer.vector(0.1, 0.1, 0.2), cafe))
    rayTracer.scene.append(AABB(Raytracer.vector(2.4, -1.5, -9.5), Raytracer.vector(0.1, 0.1, 0.2), cafe))


    rayTracer.rtRender()
    rayTracer.glFinish('output/dr3.bmp')

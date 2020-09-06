"""
---------------------------------------------------------------------------------------------------
	Author:
	Francisco Rosal 18676
---------------------------------------------------------------------------------------------------
"""

from gl import Raytracer
from utils.color import Color
from obj import Obj, Texture
from utils.sphere import Sphere
from utils.material import Material

def dr1():
    render = Raytracer(1080, 1080)

    white_snow = Material(diffuse = Color.color(1, 0.98, 0.98))
    black = Material(diffuse = Color.color(0, 0, 0))
    orange_carrot = Material(diffuse = Color.color(0.92, 0.54, 0.13))
    white = Material(diffuse = Color.color(1, 1, 1))
    gray = Material(diffuse = Color.color(0.22, 0.22, 0.22))

    # Body
    render.scene.append(Sphere(Raytracer.vector(0, 1,  -4), 0.5, white_snow))
    render.scene.append(Sphere(Raytracer.vector(0, 0, -4), 0.7, white_snow))
    render.scene.append(Sphere(Raytracer.vector(0, -1, -4), 1, white_snow))

    # Buttons
    render.scene.append(Sphere(Raytracer.vector(0, 0, -3), 0.1, black))
    render.scene.append(Sphere(Raytracer.vector(0, -0.35, -3), 0.1, black))
    render.scene.append(Sphere(Raytracer.vector(0, -0.7, -3), 0.1, black))

    # Nose
    render.scene.append(Sphere(Raytracer.vector(0, 0.75, -3), 0.09, orange_carrot))

    # Eyes
    # render.scene.append(Sphere(Raytracer.vector(-1, 0.9, -3), 0.08, white))
    # render.scene.append(Sphere(Raytracer.vector(0.5, 0.9, -3), 0.08, white))
    render.scene.append(Sphere(Raytracer.vector(-0.5, 0.8, -2.5), 0.03, black))
    render.scene.append(Sphere(Raytracer.vector(0.5, 0.8, -2.5), 0.03, black))

    # render.scene.append(Sphere(Raytracer.vector(-0.08, 0.7,  -3), 0.04, gray))
    # render.scene.append(Sphere(Raytracer.vector(0.08, 0.7,  -3), 0.04, gray))
    # render.scene.append(Sphere(Raytracer.vector(-0.20, 0.77,  -3), 0.04, gray))
    # render.scene.append(Sphere(Raytracer.vector(0.20, 0.77,  -3), 0.04, gray))

    render.rtRender()
    render.glFinish('output/dr1.bmp')

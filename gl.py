"""
---------------------------------------------------------------------------------------------------
	Author:
	Francisco Rosal 18676
---------------------------------------------------------------------------------------------------
"""

from obj import Obj
import utils.glmath as glmath
from utils.color import Color
from utils.memory import MemorySize
from numpy import cos, sin, tan, pi

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2
MAX_RECURSION_DEPTH = 3

def reflectVector(normal, dirVector):
    reflect = 2 * glmath.dot(normal, dirVector)
    reflect = glmath.mulEscalarVector(reflect, normal)
    reflect = glmath.sub(reflect, dirVector)
    reflect = glmath.div(reflect, glmath.frobeniusNorm(reflect))
    return reflect

def refractVector(N, I, ior):
    cosi = max(-1, min(1, glmath.dot(I, N))) 
    etai = 1
    etat = ior

    if cosi < 0:
        cosi = -cosi
    else:
        etai, etat = etat, etai
        N = N * -1

    eta = etai/etat
    k = 1 - eta * eta * (1 - (cosi * cosi))

    if k < 0: 
        return None

    R = eta * I + (eta * cosi - k ** 0.5) * N
    return R / glmath.frobeniusNorm(R)


def fresnel(N, I, ior):
    cosi = max(-1, min(1, glmath.dot(I, N)))
    etai = 1
    etat = ior

    if cosi > 0:
        etai, etat = etat, etai

    sint = etai / etat * (max(0, 1 - cosi * cosi) ** 0.5)

    if sint >= 1:
        return 1

    cost = max(0, 1 - sint * sint) ** 0.5
    cosi = abs(cosi)
    Rs = ((etat * cosi) - (etai * cost)) / ((etat * cosi) + (etai * cost))
    Rp = ((etai * cosi) - (etat * cost)) / ((etai * cosi) + (etat * cost))
    return (Rs * Rs + Rp * Rp) / 2


class Raytracer(object):

    def __init__(self, width, height):
        self.window_color = Color.black()
        self.draw_color = Color.white()
        self.glCreateWindow(width, height)

        self.camPosition = self.vector(0, 0, 0)
        self.fov = 60
        self.scene = []
        self.pointLight = None
        self.ambientLight = None
        self.envmap = None

    @staticmethod
    def glInit(width, height):
        return Raytracer(width, height)

    def glCreateWindow(self, width, height):
        self.width, self.height = width, height
        self.glClear()
        self.glViewPort(0, 0, width, height)

    def glViewPort(self, x, y, width, height):
        self.viewPort_x, self.viewPort_y = x, y
        self.viewPort_width = width if width < self.width else self.width 
        self.viewPort_height = height if height < self.height else self.height
        # self.viewPort = [ [ Color.black() for y in range(self.viewPort_height) ] for x in range(self.viewPort_width) ]

    def glClear(self, r = 0, g = 0, b = 0):
        self.pixels = [ [ Color.color(r, g, b) for x in range(self.width) ] for y in range(self.height) ]
        self.zbuffer = [ [ float('inf') for x in range(self.width)] for y in range(self.height) ]

    def glClearColor(self, r, g, b):
        self.glClear(r, g, b)

    # def glVertex(self, x, y, color=None):
    #     x_relative, y_relative = self.ndp_to_pixels(x, y)
    #     try:
    #         self.pixels[y_relative][x_relative] = color or self.draw_color
    #     except:
    #         pass

    def glBackground(self, texture):
        self.pixels = [ [ texture.getColor(x / self.width, y / self.height) for x in range(self.width)] for y in range(self.height) ]

    def glVertex_coords(self, x, y, color=None):
        # if color == None:
        #     color = self.draw_color

        if x < self.viewPort_x or x >= self.viewPort_x + self.viewPort_width or y < self.viewPort_y or y >= self.viewPort_y + self.viewPort_height:
            return

        if x >= self.width or x < 0 or y >= self.height or y < 0:
            return

        try:
            self.pixels[y][x] = color or self.draw_color
        except:
            pass

    def glColor(self, r = 0, g = 0, b = 0):
        self.draw_color = Color.color(r, g, b)

    def glFinish(self, filename = 'output/output.bmp'):
        render = open(filename, 'wb')

        # File header 14 bytes
        render.write(MemorySize.char('B'))
        render.write(MemorySize.char('M'))
        render.write(MemorySize.dword(14 + 40 + self.width * self.height * 3))
        render.write(MemorySize.dword(0))
        render.write(MemorySize.dword(14 + 40))

        # Image header 40 bytes
        render.write(MemorySize.dword(40))
        render.write(MemorySize.dword(self.width))
        render.write(MemorySize.dword(self.height))
        render.write(MemorySize.word(1))
        render.write(MemorySize.word(24))
        render.write(MemorySize.dword(0))
        render.write(MemorySize.dword(self.width * self.height * 3))
        render.write(MemorySize.dword(0))
        render.write(MemorySize.dword(0))
        render.write(MemorySize.dword(0))
        render.write(MemorySize.dword(0))

        # self.insert_viewPort()
        
        # Pixels. 3 bytes each
        [ [ render.write(self.pixels[x][y]) for y in range(self.width) ] for x in range(self.height) ]
        render.close()

    # def insert_viewPort(self):
    #     # Insert view port into window
    #     for x in range(self.viewPort_width):
    #         for y in range(self.viewPort_height):
    #             self.pixels[x + self.viewPort_x][y + self.viewPort_y] = self.viewPort[x][y]

    # def ndp_to_pixels(self, x, y):
    #     # Las coordenadas x, y son relativas al viewport.
    #     return glmath.relative(x, -1, 1, self.viewPort_width, 1) - 1, glmath.relative(y, -1, 1, self.viewPort_height, 1) - 1

    # def load_model_3D(self, filename, translate=None, scale=None, rotate=None, isWireframe=False):
    #     posX, posY = self.ndp_to_pixels(translate['x'], translate['y'])
    #     translate = self.vector(posX, posY, 0)


    def glZBuffer(self, filename='output/zbuffer.bmp'):
        archivo = open(filename, 'wb')

        height, width = self.height, self.width

        # File header 14 bytes
        archivo.write(bytes('B'.encode('ascii')))
        archivo.write(bytes('M'.encode('ascii')))
        archivo.write(MemorySize.dword(14 + 40 + width * height * 3))
        archivo.write(MemorySize.dword(0))
        archivo.write(MemorySize.dword(14 + 40))

        # Image Header 40 bytes
        archivo.write(MemorySize.dword(40))
        archivo.write(MemorySize.dword(width))
        archivo.write(MemorySize.dword(height))
        archivo.write(MemorySize.word(1))
        archivo.write(MemorySize.word(24))
        archivo.write(MemorySize.dword(0))
        archivo.write(MemorySize.dword(width * height * 3))
        archivo.write(MemorySize.dword(0))
        archivo.write(MemorySize.dword(0))
        archivo.write(MemorySize.dword(0))
        archivo.write(MemorySize.dword(0))

        minZ = float('inf')
        maxZ = -float('inf')
        for x in range(height):
            for y in range(width):
                if self.zbuffer[x][y] != -float('inf'):
                    if self.zbuffer[x][y] < minZ:
                        minZ = self.zbuffer[x][y]

                    if self.zbuffer[x][y] > maxZ:
                        maxZ = self.zbuffer[x][y]

        for x in range(height):
            for y in range(width):
                depth = self.zbuffer[x][y]
                if depth == -float('inf'):
                    depth = minZ
                depth = (depth - minZ) / (maxZ - minZ)
                archivo.write(Color.color(depth,depth,depth))

        archivo.close()

    @staticmethod
    def vector(x, y, z=0, w=0):
        return {
            "x": x,
            "y": y,
            "z": z,
            "w": w
        }

    def rtRender(self):
        for y in range(self.height):
            for x in range(self.width):

                Px = 2 * ((x + 0.5) / self.width) - 1
                Py = 2 * ((y + 0.5) / self.height) - 1

                t = tan( (self.fov * pi / 180) / 2 )
                r = t * self.width / self.height
                Px *= r
                Py *= t

                direction = self.vector(Px, Py, -1)
                direction = glmath.div(direction, glmath.frobeniusNorm(direction))
                self.glVertex_coords(x, y, self.castRay(self.camPosition, direction))

    def scene_intercept(self, orig, direction, origObj = None):
        tempZbuffer = float('inf')
        material = None
        intersect = None

        for obj in self.scene:
            if obj is not origObj:
                hit = obj.ray_intersect(orig, direction)
                if hit is not None:
                    if hit.distance < tempZbuffer:
                        tempZbuffer = hit.distance
                        material = obj.material
                        intersect = hit

        return material, intersect

    def castRay(self, orig, direction, origObj = None, recursion = 0):
        material, intersect = self.scene_intercept(orig, direction, origObj)

        if material is None or recursion >= MAX_RECURSION_DEPTH:
            if self.envmap:
                return self.envmap.getColor(direction)
            return self.window_color

        objectColor = self.vector(
            material.diffuse[2] / 255,
            material.diffuse[1] / 255,
            material.diffuse[0] / 255
        )

        ambientColor = self.vector(0, 0, 0)
        diffuseColor = self.vector(0, 0, 0)
        specColor = self.vector(0, 0, 0)
        reflectColor = [0, 0, 0]
        refractColor = [0, 0, 0]
        finalColor = [0, 0, 0]
        shadow_intensity = 0
        view_dir = glmath.sub(self.camPosition, intersect.point)
        view_dir = glmath.div(view_dir, glmath.frobeniusNorm(view_dir))

        if self.ambientLight:
            ambientColor = self.vector(
                self.ambientLight.strength * self.ambientLight.color[2] / 255,
                self.ambientLight.strength * self.ambientLight.color[1] / 255,
                self.ambientLight.strength * self.ambientLight.color[0] / 255
            )

        if self.pointLight:
            light_dir = glmath.sub(self.pointLight.position, intersect.point)
            light_dir = glmath.div(light_dir, glmath.frobeniusNorm(light_dir))

            intensity = self.pointLight.intensity * max(0, glmath.dot(light_dir, intersect.normal))
            diffuseColor = self.vector(
                intensity * self.pointLight.color[2] / 255,
                intensity * self.pointLight.color[1] / 255,
                intensity * self.pointLight.color[2] / 255
            )

            reflect = reflectVector(intersect.normal, light_dir) 
            spec_intensity = self.pointLight.intensity * (max(0, glmath.dot(view_dir, reflect)) ** material.spec)
            specColor = self.vector(
                spec_intensity * self.pointLight.color[2] / 255,
                spec_intensity * self.pointLight.color[1] / 255,
                spec_intensity * self.pointLight.color[0] / 255
            )

            shadMat, shadInter = self.scene_intercept(intersect.point,  light_dir, intersect.sceneObject)
            if shadInter is not None and shadInter.distance < glmath.frobeniusNorm(glmath.sub(self.pointLight.position, intersect.point)):
                shadow_intensity = 1


        if material.matType == OPAQUE:
            finalColor = glmath.suma(ambientColor, glmath.mulEscalarVector((1 - shadow_intensity), glmath.suma(diffuseColor, specColor)))

        elif material.matType == REFLECTIVE:
            reflect = reflectVector(intersect.normal, direction * -1)
            reflectColor = self.castRay(intersect.point, reflect, intersect.sceneObject, recursion + 1)
            reflectColor = [
                reflectColor[2] / 255,
                reflectColor[1] / 255,
                reflectColor[0] / 255
            ]

            finalColor = glmath.suma(reflectColor, glmath.mulEscalarVector((1 - shadow_intensity), specColor))

        elif material.matType == TRANSPARENT:
            outside = glmath.dot(direction, intersect.normal) < 0
            bias = 0.001 * intersect.normal
            kr = fresnel(intersect.normal, direction, material.ior)

            reflect = reflectVector(intersect.normal, direction * -1)
            reflectOrig = glmath.suma(intersect.point, bias) if outside else glmath.sub(intersect.point, bias)
            reflectColor = self.castRay(reflectOrig, reflect, None, recursion + 1)
            reflectColor = [
                reflectColor[2] / 255,
                reflectColor[1] / 255,
                reflectColor[0] / 255
            ]

            if kr < 1:
                refract = refractVector(intersect.normal, direction, material.ior)
                refractOrig = glmath.sub(intersect.point, bias) if outside else glmath.suma(intersect.point, bias)
                refractColor = self.castRay(refractOrig, refract, None, recursion + 1)
                refractColor = [
                    refractColor[2] / 255,
                    refractColor[1] / 255,
                    refractColor[0] / 255
                ]

            finalColor = glmath.suma(glmath.suma(glmath.mulEscalarVector(kr, reflectColor), glmath.mulEscalarVector((1-kr), refractColor)), multiply((1 - shadow_intensity), specColor))

        finalColor = glmath.mulVectores(finalColor, objectColor)

        r = min(1, finalColor['x'])
        g = min(1, finalColor['y'])
        b = min(1, finalColor['z'])

        return Color.color(r, g, b)

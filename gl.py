"""
---------------------------------------------------------------------------------------------------
	Author:
	Francisco Rosal 18676
---------------------------------------------------------------------------------------------------
"""

from utils.color import Color
from utils.memory import MemorySize
from obj import Obj
import utils.glmath as glmath
from numpy import cos, sin, tan, pi


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
                material = None
                intersect = None

                for obj in self.scene:
                    hit = obj.ray_intersect(self.camPosition, direction)
                    if hit:
                        if hit.distance < self.zbuffer[y][x]:
                            self.zbuffer[y][x] = hit.distance
                            material = obj.material
                            intersect = hit

                if intersect:
                    self.glVertex_coords(x, y, self.pointColor(material, intersect))

    def pointColor(self, material, intersect):
        objectColor = self.vector(
            material.diffuse[2] / 255,
            material.diffuse[1] / 255,
            material.diffuse[0] / 255
        )

        ambientColor = self.vector(0, 0, 0)
        diffuseColor = self.vector(0, 0, 0)
        specColor = self.vector(0, 0, 0)

        shadow_intensity = 0

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

            view_dir = glmath.sub(self.camPosition, intersect.point)
            view_dir = glmath.div(view_dir, glmath.frobeniusNorm(view_dir))

            reflect = 2 * glmath.dot(intersect.normal, light_dir)
            reflect = glmath.mulEscalarVector(reflect, intersect.normal)
            reflect = glmath.sub(reflect, light_dir)

            spec_intensity = self.pointLight.intensity * (max(0, glmath.dot(view_dir, reflect)) ** material.spec)

            specColor = self.vector(
                spec_intensity * self.pointLight.color[2] / 255,
                spec_intensity * self.pointLight.color[1] / 255,
                spec_intensity * self.pointLight.color[0] / 255
            )

            for obj in self.scene:
                if obj is not intersect.sceneObject:
                    hit = obj.ray_intersect(intersect.point,  light_dir)
                    if hit and intersect.distance < glmath.frobeniusNorm(glmath.sub(self.pointLight.position, intersect.point)):
                        shadow_intensity = 1


        finalColor = glmath.mulVectores(
            glmath.suma(
                ambientColor,
                glmath.mulEscalarVector(
                    (1 - shadow_intensity),
                    glmath.suma(diffuseColor, specColor)
                )
            ),
            objectColor
        )

        r = min(1, finalColor['x'])
        g = min(1, finalColor['y'])
        b = min(1, finalColor['z'])

        return Color.color(r, g, b)


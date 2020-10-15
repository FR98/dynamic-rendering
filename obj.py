"""
---------------------------------------------------------------------------------------------------
	Author:
	Francisco Rosal 18676
---------------------------------------------------------------------------------------------------
"""

import struct
from utils.color import Color
from numpy import arctan2, arccos, pi
from utils.glmath import frobeniusNorm, div

class Obj(object):

    def __init__(self, filename):
        with open(filename, 'r') as file:
            self.lines = file.read().splitlines()
        
        self.faces = []
        self.normals = []
        self.vertices = []
        self.texture_coords = []
        self.read()

    def read(self):
        for line in self.lines:
            if len(line) > 0:
                prefix, value = line.split(' ', 1)
                
                if prefix == 'v':
                    # x, y, z
                    self.vertices.append(list(map(float, value.split(' '))))
                elif prefix == 'vn':
                    # x, y, z
                    self.normals.append(list(map(float, value.split(' '))))
                elif prefix == 'vt':
                    self.texture_coords.append(list(map(float, value.split(' '))))
                elif prefix == 'f':
                    # f = v/vt/vn
                    self.faces.append([list(map(int, vertex.split('/'))) for vertex in value.split(' ')])


class Texture(object):
    def __init__(self, path):
        self.path = path
        self.read()
        
    def read(self):
        image = open(self.path, 'rb')
        image.seek(10)
        headerSize = struct.unpack('=l', image.read(4))[0]

        image.seek(14 + 4)
        self.width = struct.unpack('=l', image.read(4))[0]
        self.height = struct.unpack('=l', image.read(4))[0]
        image.seek(headerSize)

        self.pixels = []

        for y in range(self.height):
            self.pixels.append([])
            for x in range(self.width):
                b = ord(image.read(1)) / 255
                g = ord(image.read(1)) / 255
                r = ord(image.read(1)) / 255
                self.pixels[y].append(Color.color(r, g, b))

        image.close()

    def getColor(self, tx, ty):
        if tx >= 0 and tx <= 1 and ty >= 0 and ty <= 1:
            x = int(tx * self.width)
            y = int(ty * self.height)

            return self.pixels[y][x]
        else:
            return Color.color(0,0,0)

class Envmap(object):

    def __init__(self, path):
        self.path = path
        self.read()

    def read(self):
        image = open(self.path, 'rb')
        image.seek(10)
        headerSize = struct.unpack('=l', image.read(4))[0]

        image.seek(14 + 4)
        self.width = struct.unpack('=l', image.read(4))[0]
        self.height = struct.unpack('=l', image.read(4))[0]
        image.seek(headerSize)

        self.pixels = []

        for y in range(self.height):
            self.pixels.append([])
            for x in range(self.width):
                b = ord(image.read(1)) / 255
                g = ord(image.read(1)) / 255
                r = ord(image.read(1)) / 255
                self.pixels[y].append(Color.color(r,g,b))

        image.close()

    def getColor(self, direction):

        direction = div(direction, frobeniusNorm(direction))

        x = int((arctan2( direction['z'], direction['x']) / (2 * pi) + 0.5) * self.width)
        y = int(arccos(-direction['y']) / pi * self.height )

        return self.pixels[y][x]

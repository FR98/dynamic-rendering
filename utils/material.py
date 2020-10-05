"""
---------------------------------------------------------------------------------------------------
	Author:
	Francisco Rosal 18676
---------------------------------------------------------------------------------------------------
"""

from utils.color import Color

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2


class Material(object):
    def __init__(self, diffuse = Color.white(), spec = 0, ior = 1, matType = OPAQUE):
        self.ior = ior
        self.spec = spec
        self.diffuse = diffuse
        self.matType = matType

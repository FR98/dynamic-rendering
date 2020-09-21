"""
---------------------------------------------------------------------------------------------------
	Author:
	Francisco Rosal 18676
---------------------------------------------------------------------------------------------------
"""
from utils.color import Color

class Material(object):
    def __init__(self, diffuse = Color.white(), spec = 0):
        self.diffuse = diffuse
        self.spec = spec

"""
---------------------------------------------------------------------------------------------------
	Author:
	Francisco Rosal 18676
---------------------------------------------------------------------------------------------------
"""
from utils.color import Color

class Material(object):
    def __init__(self, diffuse = Color.white()):
        self.diffuse = diffuse

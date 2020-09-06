"""
---------------------------------------------------------------------------------------------------
	Author:
	Francisco Rosal 18676
---------------------------------------------------------------------------------------------------
"""


class Color(object):

    def __init__(self, r, g, b):
        self.color(r, g, b)

    @staticmethod
    def color(r, g, b):
        return bytes([int(b*255), int(g*255), int(r*255)])

    @staticmethod
    def black():
        return Color.color(0, 0, 0)

    @staticmethod
    def white():
        return Color.color(1, 1, 1)

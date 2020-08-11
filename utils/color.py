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
        return bytes([b, g, r])

    @staticmethod
    def black():
        return Color.color(0, 0, 0)

    @staticmethod
    def white():
        return Color.color(255, 255, 255)

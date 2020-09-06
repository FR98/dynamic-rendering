"""
---------------------------------------------------------------------------------------------------
	Author:
	Francisco Rosal 18676
---------------------------------------------------------------------------------------------------
"""

import struct


class MemorySize(object):

    @staticmethod
    def char(c):
        # 1 byte
        return struct.pack('=c', c.encode('ascii'))

    @staticmethod
    def word(w):
        # 2 bytes
        return struct.pack('=h', w)

    @staticmethod
    def dword(d):
        # 4 bytes
        return struct.pack('=l', d)

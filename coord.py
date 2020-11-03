from OpenGL.GL import *
from OpenGL.GLU import *
import sys
import math
from egl import *

class Coord:

    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "<" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ">" 

    def __add__(self,coord):
        newx = round(self.x + coord.x ,4)
        newy = round(self.y + coord.y ,4)
        newz = round(self.z + coord.z ,4)
        return Coord(newx,newy,newz)

    def __sub__(self,coord):
        newx = round(self.x - coord.x ,4)
        newy = round(self.y - coord.y ,4)
        newz = round(self.z - coord.z ,4)
        return Coord(newx,newy,newz)

    def __mul__(self,factor):
        if isinstance(factor, Coord):
            newx = round(self.x * factor.x ,4)
            newy = round(self.y * factor.y ,4)
            newz = round(self.z * factor.z ,4)
            return Coord(newx,newy,newz)
        elif isinstance(factor, float) or isinstance(factor, int):
            newx = round(self.x * factor ,4)
            newy = round(self.y * factor ,4)
            newz = round(self.z * factor ,4)
            return Coord(newx,newy,newz)

    def __truediv__(self,factor):
        if isinstance(factor, float) or isinstance(factor, int):
            newx = round(self.x / factor ,4)
            newy = round(self.y / factor ,4)
            newz = round(self.z / factor ,4)
            return Coord(newx,newy,newz)

    def copy(self):
        return Coord(self.x,self.y,self.z)
        

    def toTuple(self):
        return (self.x,self.y,self.z)

    def normalize(self):
        size = self.size()
        if size  == 0 :
            return Coord(0,0,0)
        x = self.x / size
        y = self.y / size
        z = self.z / size
        return Coord(x,y,z)

    def round(self,r=4):
        self.x = round(self.x,r)
        self.y = round(self.y,r)
        self.z = round(self.z,r)

    def size(self):
        return math.sqrt( (self.x*self.x) + (self.y*self.y) + (self.z*self.z) )
        
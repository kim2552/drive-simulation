"""
map_model.py

The Map Class represents the environment in which the car will maneuver in.
This will include road surfaces and obstacles.

Written by David Joohoon Kim
joohoon.kim@outlook.com
"""
import pygame
from pygame.math import Vector2
from math import sin, cos, tan, radians, degrees, copysign, pi, sqrt

""" Map Parameters """
SCALE = 4           #TODO::Make SCALE a global parameter from main.py
MAP_WIDTH = 254*SCALE
MAP_HEIGHT = 254*SCALE
BORDER = 4*SCALE


class Map:
    def __init__(self,x,y):
        self.pos = Vector2(x,y)
        self.dim = Vector2(MAP_WIDTH,MAP_HEIGHT)
        self.border = BORDER

    def update(self,dt,pos):
        self.pos.x = pos.x
        self.pos.y = pos.y
        print("Map position:",self.pos)

    def CheckBoundary(self,pos_valid,x,y,car):
        if(x >= car["pos"].x+self.getDim().x-car["length"]-self.getBorder()):
            pos_valid[0] = False
        if(x <= car["pos"].x+self.getBorder()):
            pos_valid[0] = False

        #TODO::Change length and width parameter based on orientation
        if(y >= car["pos"].y+self.getDim().y-car["length"]-self.getBorder()):
            pos_valid[1] = False
        if(y <= car["pos"].y+self.getBorder()):
            pos_valid[1] = False

        return pos_valid

    def getPos(self):
        return self.pos

    def getDim(self):
        return self.dim

    def getBorder(self):
        return self.border

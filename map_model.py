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
#        print("Map position:",self.pos)

    def CheckBoundary(self,x,y,car):
        x_valid = True
        y_valid = True

        if(x >= car["pos"].x+self.getDim().x-car["length"]-self.getBorder()):
            x_valid = False
        if(x <= car["pos"].x+self.getBorder()):
            x_valid = False
        if(y >= car["pos"].y+self.getDim().y-car["length"]-self.getBorder()):
            y_valid = False
        if(y <= car["pos"].y+self.getBorder()):
            y_valid = False

        return [x_valid,y_valid]

    def getPos(self):
        return self.pos

    def getDim(self):
        return self.dim

    def getBorder(self):
        return self.border

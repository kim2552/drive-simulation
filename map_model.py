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

    def CheckTerrain(self,terrain,x,y,car):
        print("x=",x," y=",y)
        print(car.getPosition().x+(192*SCALE))
        print(car.getPosition().x+(61*SCALE))
        print(car.getPosition().x+(191*SCALE))
        print(car.getPosition().x+(55*SCALE))
        if( (x <= car.getPosition().x+(192*SCALE)) and  # MIDDLE GRASS AREA
            (x >= car.getPosition().x+(61*SCALE)) and
            (y <= car.getPosition().y+(191*SCALE)) and
            (y >= car.getPosition().y+(55*SCALE)) ):
            terrain = 1
        elif( (x <= car.getPosition().x+(250*SCALE)) and  # TOP GRASS AREA
              (x >= car.getPosition().x+(4*SCALE)) and
              (y <= car.getPosition().y+(17*SCALE)) and
              (y >= car.getPosition().y+(4*SCALE)) ):
            terrain = 1
        elif( (x <= car.getPosition().x+(250*SCALE)) and  # RIGHT GRASS AREA
              (x >= car.getPosition().x+(231*SCALE)) and
              (y <= car.getPosition().y+(250*SCALE)) and
              (y >= car.getPosition().y+(4*SCALE)) ):
            terrain = 1
            print("hi")
        elif( (x <= car.getPosition().x+(250*SCALE)) and  # BOTTOM GRASS AREA
              (x >= car.getPosition().x+(4*SCALE)) and
              (y <= car.getPosition().y+(250*SCALE)) and
              (y >= car.getPosition().y+(235*SCALE)) ):
            terrain = 1
        elif( (x <= car.getPosition().x+(20*SCALE)) and  # LEFT GRASS AREA
              (x >= car.getPosition().x+(4*SCALE)) and
              (y <= car.getPosition().y+(235*SCALE)) and
              (y >= car.getPosition().y+(4*SCALE)) ):
            terrain = 1
        else:
            terrain = 0

        print("terrain=",terrain)
        return terrain


    def getPos(self):
        return self.pos

    def getDim(self):
        return self.dim

    def getBorder(self):
        return self.border

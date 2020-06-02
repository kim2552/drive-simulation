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
SCALE = 2           #TODO::Make SCALE a global parameter from main.py
MAP_WIDTH = 254*SCALE
MAP_HEIGHT = 254*SCALE
BORDER = 4*SCALE


class Map:
    def __init__(self,x,y):
        self.pos = Vector2(x,y)
        self.vel = Vector2(0,0)
        self.accel = Vector2(0,0)
        self.dim = Vector2(MAP_WIDTH,MAP_HEIGHT)
        self.border = BORDER

    def update(self,dt,accel,pos):
        self.accel.x = accel.x
        self.accel.y = accel.y
        # Map movement direction is opposite of car movement direction.
        self.vel.x = self.vel.x + (self.accel.x*dt)
        self.vel.y = self.vel.y + (self.accel.y*dt)
        self.pos.x = pos.x#self.pos.x + (self.vel.x*dt)
        self.pos.y = pos.y#self.pos.y + (self.vel.y*dt)
        print("MAP:",self.pos)

    def getPos(self):
        return self.pos

    def getDim(self):
        return self.dim

    def getBorder(self):
        return self.border

"""
sensor.py

The sensor represents an ideal sensor for detecting objects/environment in front
of the vehicle.

Written by David Joohoon Kim
joohoon.kim@outlook.com
"""
import pygame
from pygame.math import Vector2
from math import sin, cos, tan, radians, degrees, copysign, pi

from constants import *
import map_model

class Sensor:
    def __init__(self, x=0.0, y=0.0, orient=0.0):
        self.position = Vector2(x,y)
        self.orient = orient
        self.length = 0
        self.width = 5

    def update(self,position,orient):
        self.position.x = position.x
        self.position.y = position.y
        self.orient = orient

    def check_sensor(self,env,distance=100,num_intervals=10):

        self.length = distance

        detected = False

        heading = Vector2(cos(self.orient*pi/180.0),sin(-self.orient*pi/180.0))
        steps = int(distance/num_intervals)
        for i in range(0,num_intervals+1):
            sensor_pos = Vector2(self.position.x + (heading.x*i*steps), self.position.y + (heading.y*i*steps))
            terrain = env.CheckTerrain(self.position.x,self.position.y,sensor_pos)
            if(terrain):
                detected = True
                continue

        return detected

    def get_position(self):
        return self.position

    def get_length(self):
        return self.length

    def get_width(self):
        return self.width
        
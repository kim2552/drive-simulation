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

    def update(self,position,orient):
        self.position.x = position.x
        self.position.y = position.y
        self.orient = orient

    def check_sensor(self,env,distance=100,num_intervals=10):
        detected = False

        # Get middle of the screen
        x_center = SCREEN_WIDTH//2
        y_center = SCREEN_HEIGHT//2

        heading = Vector2(cos(self.orient*pi/180.0),sin(-self.orient*pi/180.0))
        steps = int(distance/num_intervals)
        for i in range(1,num_intervals+1):
            sensor_pos = Vector2(self.position.x + (heading.x*i*steps), self.position.y + (heading.y*i*steps))
            terrain = env.CheckTerrain(x_center,y_center,sensor_pos)
            if(terrain):
                detected = True
        return detected

        
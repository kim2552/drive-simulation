"""
car_model.py

The Car Class represents the physical nature of the car.
Phsyics model is based on Ackermann steering.

Written by David Joohoon Kim
joohoon.kim@outlook.com
"""
import pygame
from pygame.math import Vector2
from math import sin, cos, tan, radians, degrees, copysign, pi

""" Vehicle Parameters """
LENGTH = 30  #(0.1m)
WIDTH = 15   #(0.1m)
MASS = 500   #(kg)


class Car:
    def __init__(self, x, y, angle=90.0, length=LENGTH, width=WIDTH, max_steer=0, max_speed=5, max_accel=5.0):
        self.position = Vector2(x,y)
        self.prev_pos = Vector2(x,y)
        self.velocity = Vector2(0.0,0.0)
        self.accel = 0.0
        self.steer_angle = 0.0
        self.angle = angle
        self.speed = 0.0
        # Constants
        self.length = LENGTH
        self.width = WIDTH

        # Thresholds for input
        self.max_accel = max_accel
        self.max_steer = max_steer
        self.max_speed = max_speed

    ''' Update the vehicle information '''
    def update(self, dt):
        self.prev_pos = self.position

        if(abs(self.speed) < self.max_speed):
            self.speed += self.accel
        self.angle = self.steer_angle

        # Air resistance and friction
        if(self.speed > 0):
            self.speed -= 0.1
        else:
            if(not(self.accel)):
                self.speed = 0

        self.position.x += cos(self.angle*pi/180.0)*self.speed
        self.position.y -= sin(self.angle*pi/180.0)*self.speed

        # Print Characteristics
#        print("SPEED="+str(self.speed))
#        print("STEERANGLE="+str(self.steer_angle))
#        print("VEL="+str(self.velocity))
#        print("POS="+str(self.position))
#        print("ACCEL="+str(self.accel))

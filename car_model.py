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
    def __init__(self,x,y,angle=90,length=LENGTH,width=WIDTH,max_steer=0,max_speed=5,max_accel=5.0):
        self.position = Vector2(x,y)
        self.velocity = Vector2(0.0,0.0)
        self.force = 0.0
        self.steer_angle = 0.0
        self.angle = 0.0
        # Constants
        self.length = LENGTH
        self.width = WIDTH
        self.mass = MASS

        # Thresholds for input
        self.max_accel = max_accel
        self.max_steer = max_steer
        self.max_speed = max_speed

    ''' Update the vehicle information '''
    def update(self, dt):
        accel = self.force/self.mass
        self.velocity.x = ((self.velocity.x*2)+accel*dt)/2
        self.position.x += self.velocity.x*dt

    http://hyperphysics.phy-astr.gsu.edu/hbase/carcr.html
    def setReaction(self,react):
        f = -(0.5*self.mass*(self.velocity.x*self.velocity.x))/self.length
        self.force = f

    def setForce(self,force):
        self.force = force

    def setSteerAngle(self,angle):
        self.steer_angle = angle

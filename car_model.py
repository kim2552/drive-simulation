"""
car_model.py

The Car Class represents the physical nature of the car.
Phsyics model is based on Ackermann steering.

Written by David Joohoon Kim
joohoon.kim@outlook.com
"""
import pygame
from pygame.math import Vector2
from math import sin, cos, tan, radians, degrees, copysign, pi, sqrt

""" Vehicle Parameters """
LENGTH = 30  #(0.1m)
WIDTH = 15   #(0.1m)
MASS = 500   #(kg)
C_DRAG = 10
C_RR = 30*C_DRAG


class Car:
    def __init__(self,x,y,orient=90,max_steer=0,max_speed=5,max_accel=5.0):
        self.pos = Vector2(x,y)
        self.vel = Vector2(0.0,0.0)
        self.accel = Vector2(0.0,0.0)
        self.engine_force = 0.0
        self.steer_angle = 0.0
        self.orient = 0.0

        # Threshold Constants
        self.max_steer = max_steer
        self.max_speed = max_speed

    ''' Update the vehicle information '''
    def update(self, dt):
        F_tract = self.engine_force
        speed=sqrt(self.vel.x*self.vel.x + self.vel.y*self.vel.y)
        F_drag = -C_DRAG*speed         #TODO::Lookup how to do scalar/vector multiplication
        F_rr = -C_RR*speed                        #Rolling Resistance C_rr ~= 30*C_drag
        F_long = F_tract + F_drag + F_rr

        self.accel.x = F_long / MASS
        self.vel.x = self.vel.x + (self.accel.x*dt)
        self.pos.x = self.pos.x + (self.vel.x*dt)
        print("EngineForce=",self.engine_force)
        print("F_long=",F_long)
        print("accel=",self.accel)
        print("velocity=",self.vel)
        print("position=",self.pos)


    def setEngineForce(self,f):
        self.engine_force = f

    def setSteerAngle(self,a):
        self.steer_angle = a

    def getLength(self):
        return LENGTH

    def getWidth(self):
        return WIDTH

    def getPosition(self):
        return self.pos

    def getOrientation(self):
        return self.orient

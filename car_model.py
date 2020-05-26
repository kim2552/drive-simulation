"""
car_model.py

The Car Class represents the physical nature of the car.
Physics model is based on equations from the following link:
https://asawicki.info/Mirror/Car%20Physics%20for%20Games/Car%20Physics%20for%20Games.html

Written by David Joohoon Kim
joohoon.kim@outlook.com
"""
import pygame
from pygame.math import Vector2
from math import sin, cos, tan, radians, degrees, copysign, pi, sqrt

""" Vehicle Parameters """
SCALE = 2             #TODO::Make SCALE a global parameter from main.py
LENGTH = 22*SCALE     #(0.1m)
WIDTH  = 11*SCALE     #(0.1m)
MASS   = 1300/SCALE   #(kg)
C_DRAG = 50     #0.4257
C_RR   = 30*C_DRAG
C_BRAKE = 1000000


class Car:
    def __init__(self,x,y,orient=90,max_steer=0,max_speed=5,max_accel=5.0):
        self.pos = Vector2(x,y)
        self.vel = Vector2(0.0,0.0)
        self.accel = Vector2(0.0,0.0)
        self.engine_force = 0.0
        self.steer_angle = 0.0
        self.orient = 0.0
        self.brake_b = 0
        self.gear = 1               #0:park, 1:drive, 2:reverse

        # Threshold Constants
        self.max_steer = max_steer
        self.max_speed = max_speed

    ''' Update the vehicle information '''
    def update(self, dt):
        speed=sqrt(self.vel.x*self.vel.x + self.vel.y*self.vel.y)

        if(self.steer_angle):
            circ_radius = LENGTH / (sin(self.steer_angle))
            ang_vel = speed / circ_radius
            self.orient = (self.orient + ang_vel)%360

        heading = Vector2(cos(self.orient*pi/180.0),sin(-self.orient*pi/180.0))

        F_tract = self.engine_force*heading

        if( ((self.vel.x>=0 and heading.x>=0)or(self.vel.x<=0 and heading.x<=0)) and\
            ((self.vel.y>=0 and heading.y>=0)or(self.vel.y<=0 and heading.y<=0)) and\
             self.brake_b and (self.gear is 1) ):
            F_tract = -heading*C_BRAKE
        if( ((self.vel.x<=0 and heading.x>=0)or(self.vel.x>=0 and heading.x<=0)) and\
            ((self.vel.y<=0 and heading.y>=0)or(self.vel.y>=0 and heading.y<=0)) and\
             self.brake_b and (self.gear is 2) ):
            F_tract = heading*C_BRAKE

        F_drag = -C_DRAG*self.vel               #TODO::Lookup how to do scalar/vector multiplication
        F_rr = -C_RR*self.vel                   #Rolling Resistance C_rr ~= 30*C_drag
        F_long = F_tract + F_drag + F_rr

        self.accel = F_long / MASS
        self.vel.x = self.vel.x + (self.accel.x*dt)
        self.vel.y = self.vel.y + (self.accel.y*dt)
        self.pos.x = self.pos.x + (self.vel.x*dt)
        self.pos.y = self.pos.y + (self.vel.y*dt)
#        print("speed=",speed)
#        print("heading=",heading)
#        print("EngineForce=",self.engine_force)
#        print("F_tract=",F_tract)
#        print("accel=",self.accel)
#        print("velocity=",self.vel)
        print("position=",self.pos)


    def setGear(self,gear):
        self.gear=gear

    def setEngineForce(self,f):
        self.engine_force = f

    def setSteerAngle(self,a):
        self.steer_angle = a

    def setBraking(self,b):
        self.brake_b = b

    def getLength(self):
        return LENGTH

    def getWidth(self):
        return WIDTH

    def getPosition(self):
        return self.pos

    def getAccel(self):
        return self.accel

    def getOrientation(self):
        return self.orient

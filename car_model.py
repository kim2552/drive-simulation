import pygame
from pygame.math import Vector2
from math import sin, cos, tan, radians, degrees, copysign


class Car:
    def __init__(self, x, y, angle=90.0, length = 60, max_steer=180, max_accel=1.0):
        self.position = Vector2(x,y)
        self.velocity = Vector2(0.0,0.0)
        self.accel = 0.0
        self.steer_angle = 0.0
        self.angle = angle

        # Constants
        self.length = length

        # Thresholds for input
        self.max_accel = max_accel
        self.max_steer = max_steer

    ''' Update the vehicle information '''
    def update(self, dt):
        ## Velocity increases as you press on the gas pedal
        #speed = self.accel * dt

        #if self.steer_angle:
        #    angular_velocity = (speed/self.length)*tan(radians(self.steer_angle))
        #else:
        #    angular_velocity = 0
        #print("SPEED"+str(speed))
        #print("STEERANGLE"+str(self.steer_angle))
        #print("ANGULARVELOCITY"+str(angular_velocity))
        #print("ANGLE"+str(self.angle))
        #self.angle += angular_velocity * dt

        #self.velocity += (speed * cos(radians(self.angle)), speed * sin(radians(self.angle)))
        #self.position += -self.velocity * dt
        #print("POSITION="+str(self.position))

        speed = self.accel * dt
        print("SPEED="+str(speed))

        if self.steer_angle:
            angular_velocity = (speed / self.length)*tan(radians(self.steer_angle))
        else:
            angular_velocity = 0
        print("ANGVEL="+str(angular_velocity))
        self.angle += angular_velocity * dt
        print("ANGLE="+str(self.angle))
        self.velocity = (speed * cos(radians(self.angle)), speed * sin(radians(self.angle)))
        print("VEL="+str(self.velocity))
        self.position += (self.velocity[0] * dt, self.velocity[1] * dt)
        print("POS="+str(self.position))

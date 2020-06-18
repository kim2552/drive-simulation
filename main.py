"""
CarSimPy

This a physics based car simulation ran on Python.
Attempts to model the physics of a car based on several factors.
The simulation runs on PyGame. (Current version 2.0.0dev6)

Written by David Joohoon Kim
joohoon.kim@outlook.com

TODO
- Add collision with map environment
- Choose a scaling method for screen and environment
"""
import os
from math import sin, cos, tan, radians, degrees, copysign, pi
import pygame
from pygame.math import Vector2
from pygame.locals import *

# local import
import car_model
import map_model

# Get image of car
current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, "assets/")
car_image = pygame.image.load(image_path+"car.png")
background_image = pygame.image.load(image_path+"background.png")
#background_image = pygame.image.load(image_path+"mario_circuit_one.png")

""" Screen Parameters """
SCALE = 2
SCREEN_WIDTH = 256*SCALE
SCREEN_HEIGHT = 256*SCALE
GAME_TICKS = 60

class Game:
    def __init__(self):
        """ initialize screen """
        pygame.init()
        pygame.display.set_caption("CarSimPy")

        # Starting Position
        car_pos_x = (SCREEN_WIDTH/2)-100
        car_pos_y = (SCREEN_HEIGHT/2)-100
        map_pos_x = car_pos_x
        map_pos_y = car_pos_y

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.ticks = GAME_TICKS
        self.exit = False
        self.car_image = None
        self.background_image = None

        self.car = car_model.Car(car_pos_x, car_pos_y)
        self.map = map_model.Map(map_pos_x,map_pos_y)

    def CheckBoundary(self,car_info,env):
        # Get middle of the screen
        x = SCREEN_WIDTH//2
        y = SCREEN_HEIGHT//2

        # Check boundaries for object(s)
        pos_valid = env.CheckBoundary(x,y,car_info)

        return pos_valid

    """ defines the controls of the car """
    """ TODO::Refine Controls for 2 wheel steering """
    """ TODO::Use something else for detecting keys, replace if else"""
    def controls(self, car, dt, pressed):
        if pressed[pygame.K_LEFT]:
            car.setSteerAngle(-10)
        elif pressed[pygame.K_RIGHT]:
            car.setSteerAngle(10)
        else:
            car.setSteerAngle(0)
        if pressed[pygame.K_UP]:
            car.setEngineForce(500000)
            car.setGear(1)
        elif pressed[pygame.K_DOWN]:
            car.setEngineForce(-200000)
            car.setGear(2)
        elif pressed[pygame.K_b]:
            car.setBraking(1)
        else:
            car.setEngineForce(0)
            car.setBraking(0)

    """ draws the screen and objects """
    def draw(self, car, env):
        # Draw background
        map_width=(int)(env.getDim().x)
        map_height=(int)(env.getDim().y)
        self.background_image = pygame.transform.scale(background_image,(map_width,map_height))
        self.screen.blit(self.background_image, env.getPos())

        # Draw car
        self.car_image = pygame.transform.scale(car_image,(car.getLength(),car.getWidth()))
        rotated = pygame.transform.rotate(self.car_image, car.getOrientation())
        rect = rotated.get_rect()
        self.screen.blit(rotated, (SCREEN_WIDTH//2,SCREEN_HEIGHT//2))

        pygame.display.flip()

    """ processes the simulation """
    def run(self):
        while not self.exit:
            # Convert time from milliseconds to seconds
            dt = self.clock.get_time() / 1000

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
                elif event.type == VIDEORESIZE:
                    screen = pygame.display.set_mode(event.dict['size'], HWSURFACE|DOUBLEBUF|RESIZABLE)

            # User input
            pressed = pygame.key.get_pressed()
            self.controls(self.car, dt, pressed)

            # Logic
            car_info = self.car.calculate(dt)
            pos_valid = self.CheckBoundary(car_info,self.map)
            self.car.update(dt,car_info,pos_valid)
            self.map.update(dt,self.car.getPosition())

            # Drawing
            self.screen.fill((0,0,0))
            self.draw(self.car,self.map)

            # Update the clock (Called once per frame)
            self.clock.tick(self.ticks)
        """ End of while not self.exit """

        pygame.quit()



if __name__ == '__main__':
    game = Game()
    game.run()

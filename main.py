"""
CarSimPy

This a physics based car simulation ran on Python.
Attempts to model the physics of a car based on several factors.
The simulation runs on PyGame. (Current version 2.0.0dev6)

Written by David Joohoon Kim
joohoon.kim@outlook.com
"""
import os
from math import sin, cos, tan, radians, degrees, copysign, pi
import pygame
from pygame.math import Vector2
from pygame.locals import *

# local import
import car_model

# Get image of car
current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, "assets/")
car_image = pygame.image.load(image_path+"car.png")
background_image = pygame.image.load(image_path+"background.png")

# Screen / Map Parameters
SCREEN_WIDTH = 254*2
SCREEN_HEIGHT = 254*2
MAP_WIDTH = 254*4
MAP_HEIGHT = 254*4
BORDER = 4*4
GAME_TICKS = 60

class Game:
    def __init__(self):
        """ initialize screen """
        pygame.init()
        pygame.display.set_caption("CarSimPy")

        # Starting Position
        self.map_pos_x = 0
        self.map_pos_y = 0
        self.car_start_pos_x = SCREEN_WIDTH/2
        self.car_start_pos_y = SCREEN_HEIGHT/2
        self.car_world_pos_x = self.map_pos_x + self.car_start_pos_x
        self.car_world_pos_y = self.map_pos_y + self.car_start_pos_y

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.ticks = GAME_TICKS
        self.exit = False
        self.car_image = None
        self.background_image = None
        self.cars = []

        # Create car(s) 
        for x in range(1):
            car = car_model.Car(self.car_start_pos_x, self.car_start_pos_y,
                self.car_world_pos_x, self.car_world_pos_y)
            self.cars.append(car)

    def enforceBoundary(self, car):
        return 0
        if(car.pos.x > SCREEN_WIDTH-20-BORDER):
            car.pos.x = SCREEN_WIDTH-21-BORDER
            car.vel = Vector2(0,0)
        if(car.pos.x < 20+BORDER):
            car.pos.x = 21+BORDER
            car.vel = Vector2(0,0)
        if(car.pos.y > SCREEN_HEIGHT-20-BORDER):
            car.pos.y = SCREEN_HEIGHT-21-BORDER
            car.vel = Vector2(0,0)
        if(car.pos.y < 20+BORDER):
            car.pos.y = 21+BORDER
            car.vel = Vector2(0,0)

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
    def draw(self, cars):
        # Draw background
        #self.background_image = pygame.transform.scale(background_image,(MAP_WIDTH,MAP_HEIGHT))
        #self.screen.blit(self.background_image,(self.map_pos_x,self.map_pos_y))

        # Draw car(s)
        for car in cars:
            self.car_image = pygame.transform.scale(car_image,(car.getLength(),car.getWidth()))
            rotated = pygame.transform.rotate(self.car_image, car.getOrientation())
            rect = rotated.get_rect()
            # Draw background
            self.background_image = pygame.transform.scale(background_image,(MAP_WIDTH,MAP_HEIGHT))
            self.screen.blit(self.background_image, car.getPosition()-(rect.width//2, rect.height//2))
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
            for c in self.cars:
                self.controls(c, dt, pressed)

            # Logic
            for c in self.cars:
                c.update(dt)
                self.enforceBoundary(c)

            # Drawing
            self.screen.fill((0,0,0))
            self.draw(self.cars)

            # Update the clock (Called once per frame)
            self.clock.tick(self.ticks)
        """ End of while not self.exit """

        pygame.quit()



if __name__ == '__main__':
    game = Game()
    game.run()

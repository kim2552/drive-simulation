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

# local import
import car_model

# Get image of car
current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, "car.png")
car_image = pygame.image.load(image_path)

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GAME_TICKS = 60

class Game:
    def __init__(self):
        """ initialize screen """
        pygame.init()
        pygame.display.set_caption("CarSimPy")
        self.car_start_pos_x = SCREEN_WIDTH/2
        self.car_start_pos_y = SCREEN_HEIGHT/2
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.ticks = GAME_TICKS
        self.exit = False
        self.car_image = None
        self.obstacle_list = []

    """ defines the controls of the car """
    """ TODO::Refine Controls for 2 wheel steering """
    def controls(self, car, dt, pressed):
        if pressed[pygame.K_LEFT]:
            car.setSteerAngle(5)
        elif pressed[pygame.K_RIGHT]:
            car.setSteerAngle(5)
        if pressed[pygame.K_UP]:
            car.setForce(100000)
        elif pressed[pygame.K_DOWN]:
            car.setForce(-100000)
        else:
            car.setForce(0)

    """ enforces collision with object and boundaries """
    """ TODO::Create Walls for the car to collide with """
    def enforceBoundaries(self, car):
        if(car.position.x > 640):
            car.setReaction(1)
        if(car.position.x < 10):
            car.setForce(0)
        if(car.position.y > 470):
            car.setForce(0)
        if(car.position.y < 10):
            car.setForce(0)

    """ draws the screen and objects """
    def draw(self, car):
        self.car_image = pygame.transform.scale(car_image,(car.length,car.width))
        rotated = pygame.transform.rotate(self.car_image, car.angle)
        rect = rotated.get_rect()
        self.screen.blit(rotated, car.position-(rect.width//2, rect.height//2))
        pygame.display.flip()

    """ processes the simulation """
    def run(self):
        # Create car model
        car = car_model.Car(self.car_start_pos_x, self.car_start_pos_y)

        while not self.exit:
            # Convert time from milliseconds to seconds
            dt = self.clock.get_time() / 1000

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            # User input
            pressed = pygame.key.get_pressed()
            self.controls(car, dt, pressed)

            ## Enfore map boundaries on the car
            self.enforceBoundaries(car)

            # Logic
            car.update(dt)

            # Drawing
            self.screen.fill((0,0,0))
            self.draw(car)

            # Update the clock (Called once per frame)
            self.clock.tick(self.ticks)
        """ End of while not self.exit """

        pygame.quit()



if __name__ == '__main__':
    game = Game()
    game.run()

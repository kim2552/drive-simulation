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
from random import randint

import pygame
from pygame.locals import *
from pygame.math import Vector2

import car_model
import map_model
import obstacle_model

from constants import *

# Get image of the car
current_dir = os.path.dirname(os.path.abspath(__file__))
assets_path = os.path.join(current_dir, "assets/")
car_image = pygame.image.load(assets_path + "car.png")
background_image = pygame.image.load(assets_path + "background.png")
rock_image = pygame.image.load(assets_path + "rock.png")
sensor_image = pygame.image.load(assets_path + "sensor_beam.png")

# Sound Effects TODO::Get better sound effects
pygame.mixer.init()
car_crash_sound = pygame.mixer.Sound(assets_path + "sounds/crash.wav")
car_driving_sound = pygame.mixer.Sound(assets_path + "sounds/car_driving_3.wav")
car_snow_sound = pygame.mixer.Sound(assets_path + "sounds/car_snow.wav")
car_skid_sound = pygame.mixer.Sound(assets_path + "sounds/tire_skid.wav")


class Game:
    def __init__(self):
        """ initialize screen """
        pygame.init()
        pygame.display.set_caption("Drive-Simulation")

        # Starting Position
        car_pos_x = (SCREEN_WIDTH / 2) - 100
        car_pos_y = (SCREEN_HEIGHT / 2) - 100
        map_pos_x = car_pos_x
        map_pos_y = car_pos_y

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.ticks = GAME_TICKS
        self.exit = False
        self.terrain = 0  # 0=road, 1=grass

        self.car = car_model.Car(car_pos_x, car_pos_y)
        self.map = map_model.Map(map_pos_x, map_pos_y)
        self.obstacles = []
        for i in range(NUM_OBSTACLES):
            x_pos = randint(100, 800)
            y_pos = randint(100, 800)
            rock = obstacle_model.Obstacle(map_pos_x + x_pos, map_pos_y + y_pos)
            self.obstacles.append(rock)

    @staticmethod
    def check_boundary(car_info, env, obstacles):
        # Get middle of the screen
        x = SCREEN_WIDTH // 2
        y = SCREEN_HEIGHT // 2

        # Check boundaries for object(s)
        pos_valid = [True, True]
        for ob in obstacles:
            pos_valid = ob.check_boundary(pos_valid, x, y, car_info)
        pos_valid = env.check_boundary(pos_valid, x, y, car_info)

        return pos_valid

    def check_terrain(self, car, env):
        # Get middle of the screen
        x = SCREEN_WIDTH // 2
        y = SCREEN_HEIGHT // 2

        self.terrain = env.check_terrain(x, y, car.get_position())
        return self.terrain

    """ defines the controls of the car """
    """ TODO::Refine Controls for 2 wheel steering """
    """ TODO::Use something else for detecting keys, replace if else"""

    @staticmethod
    def controls(car, dt, pressed):
        if pressed[pygame.K_LEFT]:
            car.set_steer_angle(-10)
        elif pressed[pygame.K_RIGHT]:
            car.set_steer_angle(10)
        else:
            car.set_steer_angle(0)
        if pressed[pygame.K_UP]:
            car.set_engine_force(500000)
            car.set_gear(1)
        elif pressed[pygame.K_DOWN]:
            car.set_engine_force(-200000)
            car.set_gear(2)
        elif pressed[pygame.K_b]:
            car.set_braking(1)
        else:
            car.set_engine_force(0)
            car.set_braking(0)

    """ draws the screen and objects """

    def draw(self, car, env, obstacles):
        # Draw background
        map_width = int(env.get_dim().x)
        map_height = int(env.get_dim().y)
        background_scaled = pygame.transform.scale(background_image, (map_width, map_height))
        self.screen.blit(background_scaled, env.get_pos())

        # Draw car
        car_scaled = pygame.transform.scale(car_image, (int(car.get_length()), int(car.get_width())))
        car_rotated = pygame.transform.rotate(car_scaled, car.get_orientation())
        self.screen.blit(car_rotated, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        # Draw obstacle(s)
        for ob in obstacles:
            rock_scaled = pygame.transform.scale(rock_image, (int(ob.get_dim().x), int(ob.get_dim().y)))
            self.screen.blit(rock_scaled, ob.get_position())

        # Draw sensor(s)
        fs_obj = car.front_sensor
        fs_scaled = pygame.transform.scale(sensor_image, (int(fs_obj.get_length()), int(fs_obj.get_width())))
        fs_rotated = pygame.transform.rotate(fs_scaled, car.get_orientation())
        front_sensor_position = Vector2((SCREEN_WIDTH // 2) + car.get_length(),
                                        (SCREEN_HEIGHT // 2) + (car.get_width() // 2))
        self.screen.blit(fs_rotated, front_sensor_position)

        pygame.display.flip()

    def run(self):
        """processes the simulation"""
        while not self.exit:
            # Local save of parameters
            prev_terrain = self.terrain

            # Convert time from milliseconds to seconds
            dt = self.clock.get_time() / 1000

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
                elif event.type == VIDEORESIZE:
                    pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)

            # User input
            pressed = pygame.key.get_pressed()
            self.controls(self.car, dt, pressed)

            # Sensors
            self.car.front_sensor.update(self.car.get_position(), self.car.get_orientation())
            detected = self.car.front_sensor.check_sensor(self.map, 100, 1)
            print(detected)

            # Logic
            self.terrain = self.check_terrain(self.car, self.map)
            self.car.set_terrain(self.terrain)
            car_info = self.car.calculate(dt)
            pos_valid = self.check_boundary(car_info, self.map, self.obstacles)
            self.car.update(dt, car_info, pos_valid)
            self.map.update(dt, self.car.get_position())
            for ob in self.obstacles:
                ob.update(self.map.get_pos())

            # Drawing
            self.screen.fill((0, 0, 0))
            self.draw(self.car, self.map, self.obstacles)

            # Sound Effects
            if SOUND_ON:
                if not (pos_valid[0]) or not (pos_valid[1]):  # The Car crashed
                    car_crash_sound.play()
                drive_sound = False
                if abs(car_info["vel"].x) > 50 or abs(car_info["vel"].y) > 50:  # Car speed > 50
                    drive_sound = True
                if not (pygame.mixer.Channel(0).get_busy()):  # Prevent sound overlap
                    if drive_sound:
                        if prev_terrain is not self.terrain:
                            car_snow_sound.stop()
                            car_driving_sound.stop()
                        if self.terrain == 0:
                            car_driving_sound.play()
                        if self.terrain == 1:
                            car_snow_sound.play()
                    else:
                        car_snow_sound.stop()
                        car_driving_sound.stop()
                else:
                    if not drive_sound:
                        car_snow_sound.stop()
                        car_driving_sound.stop()
                if abs(self.car.get_ang_vel()) > 3.0:
                    car_skid_sound.play()
                else:
                    car_skid_sound.stop()

            # Update the clock (Called once per frame)
            self.clock.tick(self.ticks)
        # End of while not self.exit

        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()

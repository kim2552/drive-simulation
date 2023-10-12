"""
obstacle_model.py

The Obstacle Class represents obstacles for the car.

Written by David Joohoon Kim
joohoon.kim@outlook.com
"""

from pygame.math import Vector2

from modules.constants import *


class Obstacle:
    def __init__(self, x, y, angle=90.0, width=30, height=30, max_speed=5, max_accel=0):
        self.position = Vector2(0.0, 0.0)
        self.pos_rel_map = Vector2(x, y)  # Position relative to map
        self.velocity = Vector2(0.0, 0.0)
        self.dim = Vector2(OBSTACLE_LENGTH, OBSTACLE_WIDTH)
        self.accel = 0.0
        self.angle = angle
        self.speed = 0.0

        # Constants
        self.width = width
        self.height = height

        # Thresholds for input
        self.max_accel = max_accel
        self.max_speed = max_speed

    def update(self, pos):
        self.position.x = pos.x + self.pos_rel_map.x
        self.position.y = pos.y + self.pos_rel_map.y

    def check_boundary(self, pos_valid, x, y, car):
        #        print("X: ",x," and Y: ",y)
        #        print("length of car:",car["length"])
        #        print("boundaryX:",car["pos"].x+self.getDim().x+self.pos_rel_map.x)
        #        print("boundaryX2:",car["pos"].x+self.pos_rel_map.x-car["length"])
        #        print("boundaryY:",car["pos"].y+self.getDim().y+self.pos_rel_map.y)
        #        print("boundaryY2:",car["pos"].y+self.pos_rel_map.y-car["length"])
        if ((x <= car["pos"].x + self.pos_rel_map.x + self.get_dim().x - 20) and
                (x >= car["pos"].x + self.pos_rel_map.x - car["length"] + 20) and
                (y <= car["pos"].y + self.pos_rel_map.y + self.get_dim().y - 20) and
                (y >= car["pos"].y + self.pos_rel_map.y - car["length"] + 20)):
            pos_valid[0] = False
            pos_valid[1] = False

        return pos_valid

    def get_position(self):
        return self.position

    def get_dim(self):
        return self.dim

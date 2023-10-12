"""
map_model.py

The Map Class represents the environment in which the car will maneuver in.
This will include road surfaces and obstacles.

Written by David Joohoon Kim
joohoon.kim@outlook.com
"""
from pygame.math import Vector2

from modules.constants import *


class Map:
    def __init__(self, x, y):
        self.pos = Vector2(x, y)
        self.dim = Vector2(MAP_WIDTH, MAP_HEIGHT)
        self.border = BORDER

    def update(self, dt, pos):
        self.pos.x = pos.x
        self.pos.y = pos.y
        # print("Map position:",self.pos)

    def check_boundary(self, pos_valid, x, y, car):
        if x >= car["pos"].x + self.get_dim().x - car["length"] - self.get_border():
            pos_valid[0] = False
        if x <= car["pos"].x + self.get_border():
            pos_valid[0] = False

        # TODO::Change length and width parameter based on orientation
        if y >= car["pos"].y + self.get_dim().y - car["length"] - self.get_border():
            pos_valid[1] = False
        if y <= car["pos"].y + self.get_border():
            pos_valid[1] = False

        return pos_valid

    @staticmethod
    def check_terrain(x, y, position):
        terrain = 0
        # print("x=",x," y=",y)
        # print(position.x+(192*SCALE))
        # print(position.x+(61*SCALE))
        # print(position.x+(191*SCALE))
        # print(position.x+(55*SCALE))
        if ((x <= position.x + (192 * SCALE)) and  # MIDDLE GRASS AREA
                (x >= position.x + (61 * SCALE)) and
                (y <= position.y + (191 * SCALE)) and
                (y >= position.y + (55 * SCALE))):
            terrain = 1
        elif ((x <= position.x + (250 * SCALE)) and  # TOP GRASS AREA
              (x >= position.x + (4 * SCALE)) and
              (y <= position.y + (17 * SCALE)) and
              (y >= position.y + (4 * SCALE))):
            terrain = 1
        elif ((x <= position.x + (250 * SCALE)) and  # RIGHT GRASS AREA
              (x >= position.x + (231 * SCALE)) and
              (y <= position.y + (250 * SCALE)) and
              (y >= position.y + (4 * SCALE))):
            terrain = 1
        elif ((x <= position.x + (250 * SCALE)) and  # BOTTOM GRASS AREA
              (x >= position.x + (4 * SCALE)) and
              (y <= position.y + (250 * SCALE)) and
              (y >= position.y + (235 * SCALE))):
            terrain = 1
        elif ((x <= position.x + (20 * SCALE)) and  # LEFT GRASS AREA
              (x >= position.x + (4 * SCALE)) and
              (y <= position.y + (235 * SCALE)) and
              (y >= position.y + (4 * SCALE))):
            terrain = 1
        else:
            terrain = 0

        # print("terrain=",terrain)
        return terrain

    def get_pos(self):
        return self.pos

    def get_dim(self):
        return self.dim

    def get_border(self):
        return self.border

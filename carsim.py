import os
from math import sin, cos, tan, radians, degrees, copysign, pi
import pygame
from pygame.math import Vector2

# local import
import car_model
import obstacle_model

# Get image of car
current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, "car.png")
car_image = pygame.image.load(image_path)

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GAME_TICKS = 60
CAR_WIDTH = 30
CAR_HEIGHT = 15

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Car Sim")
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.ticks = GAME_TICKS
        self.exit = False
        self.car_image = None
        self.obstacle_list = []

    ''' processes the simulation '''
    def run(self):
        # Create car model
        car = car_model.Car(self.width/2, self.height/2, 0, CAR_WIDTH, CAR_HEIGHT)
        obstacle = obstacle_model.Obstacle(self.width/4, self.height/2, 0, CAR_WIDTH, CAR_HEIGHT)

        self.obstacle_list.append(obstacle)

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

            # Enfore map boundaries on the car
            #self.enforceBoundaries(car, self.obstacle_list)

            # Logic
            car.update(dt)
            for obs in self.obstacle_list:
                obs.update(dt)

            ## Enfore map boundaries on the car
            self.enforceBoundaries(car, self.obstacle_list)

            # Drawing
            self.screen.fill((0,0,0))
            self.draw(car)
            self.draw(obstacle)

            # Update the clock (Called once per frame)
            self.clock.tick(self.ticks)
        ''' End of while not self.exit '''

        pygame.quit()

    ''' defines the controls of the car '''
    def controls(self, car, dt, pressed):
        if pressed[pygame.K_LEFT]:
            car.steer_angle += 5
        elif pressed[pygame.K_RIGHT]:
            car.steer_angle -= 5
        if pressed[pygame.K_UP]:
            car.accel += 0.1
        elif pressed[pygame.K_DOWN]:
            car.accel -= 0.1
        else:
            car.accel = 0
        car.accel = max(-car.max_accel, min(car.accel, car.max_accel))

    def enforceBoundaries(self, car, obstacle_list):
        if(car.position.x > 640):
            car.position.x = 610
        if(car.position.x < 0):
            car.position.x = 10
        if(car.position.y > 480):
            car.position.y = 470
        if(car.position.y < 0):
            car.position.y = 10

        for obs in obstacle_list:
            self.intersect(car, obs)

    def intersect(self, car, obs):
        car_width = car.position.x-car.width
        car_height = car.position.x-car.height
        obs_width = obs.position.x-obs.width
        obs_height = obs.position.y-obs.height
        print(car.position.x)
        print(obs.position.x)
        print(obs_width)
        if(car.position.x <= obs.position.x and car.position.x >= obs_width and car.position.y <= obs.position.y and car.position.y >= obs_height):
            print("HI 1")
            if(abs(car.position.x-obs.position.x) < abs(car.position.x-obs_width)):
                car.position.x = obs.position.x
            else:
                car.position.x = obs_width
            if(abs(car.position.y-obs.position.y) < abs(car.position.y-obs_width)):
                car.position.y = obs.position.y
            else:
                car.position.y = obs_width
        if(car_width <= obs.position.x and car_width >= obs_width and car_height <= obs.position.y and car_height >= obs_height):
            print("HI 2")
            if(abs(car_width-obs.position.x) > abs(car_width-obs_width)):
                car.position.x = obs.position.x
            else:
                car.position.x = obs_width
            if(abs(car_height-obs.position.y) > abs(car_height-obs_width)):
                car.position.y = obs.position.y
            else:
                car.position.y = obs_width

    ''' Draws the screen and objects '''
    def draw(self, car):
        self.car_image = pygame.transform.scale(car_image, (CAR_WIDTH,CAR_HEIGHT))
        rotated = pygame.transform.rotate(self.car_image, car.angle)
        rect = rotated.get_rect()
        self.screen.blit(rotated, car.position - (rect.width / 2, rect.height / 2))
        pygame.display.flip()


if __name__ == '__main__':
    game = Game()
    game.run()

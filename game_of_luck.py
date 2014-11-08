from pygame.math import Vector2
import pygame.time
import random
import sys


#-------------
import renderer
#------------

class Game_of_luck:

    FPS = 60
    WHEEL_CENTER = (400, 300)
    SLOWDOWN = 2

    def __init__(self, difficulty):
        self.wheel = Wheel_of_fortune(difficulty, Game_of_luck.WHEEL_CENTER)
        self.clock = pygame.time.Clock()

    def find_closest_to_target(self):
        closest = Fortune_ball(Vector2(-1234, -1234), (0, 0))
        for ball in self.wheel.balls:
            if ball.vector[0] <= 0 and ball.vector[1] < 0 and ball.vector[0] > closest.vector[0]:
                closest = ball
        return closest


    def start_game(self):

        pygame.init()
        screen = pygame.display.set_mode((800, 600))


        closest = self.wheel.balls[0]
        should_stop = False
        slowdown = Game_of_luck.SLOWDOWN
        while True:
            self.clock.tick(Game_of_luck.FPS)
            self.wheel.rotate(self.wheel.speed / 100)
            self.wheel.speed -= slowdown

            if self.wheel.speed <= 30 and should_stop is False:
                closest = self.find_closest_to_target()
                if closest.vector[0] != -1234:
                    self.wheel.speed = 30
                    slowdown = 0
                    should_stop = True

            if should_stop is True:
                if closest.vector[0] > 0:
                    if closest.type == "bad_luck":
                        return False
                    else:
                        return True

            renderer.draw_everything(screen, self.generate_coordinates())
            pygame.display.update()


    def generate_coordinates(self):
        coordinates = ([ball.generate_coordinates() for ball in self.wheel.balls])
        coordinates.insert(0, ("gradient_white", 0, 0))
        coordinates.append(("arrow_of_fortune", 400, 55))
        print(coordinates)
        return coordinates

    # def to_json():
        #return "arrow_of_fortune\n20\n" + str(- Wheel_of_fortune.RADIUS) + "\n\n" + "".join([ball.to_json() + "\n" for ball in self.wheel.balls])


class Wheel_of_fortune:
    RADIUS = 200
    BALLS_COUNT = 11

    def __init__(self, good_balls_count, center):
        self.center = center
        self.good_balls_count = good_balls_count
        self.speed = random.randint(400,800)
        #self.speed = random.randint(400, 700)
        self.balls = [Fortune_ball(Vector2(0, Wheel_of_fortune.RADIUS).rotate((i * 360) / \
                                              Wheel_of_fortune.BALLS_COUNT), \
                                              center) \
                                                        for i in range(Wheel_of_fortune.BALLS_COUNT)]


        random.shuffle(self.balls)
        for i in range(good_balls_count):
            self.balls[i].type = "good_luck"



    def rotate(self, angle):
        for ball in self.balls:
            ball.vector.rotate_ip(angle)


class Fortune_ball:
    def __init__(self, vector, wheel_center):
        self.wheel_center = wheel_center
        self.type = "bad_luck"
        self.vector = vector

    def generate_coordinates(self):
        return (self.type, self.vector.x + self.wheel_center[0], self.vector.y + self.wheel_center[1])
   
   # def to_json():
        #return self.type + "\n" + str(self.vector.x + self.wheel_center[0]) + "\n" + str(self.vector.y + self.wheel_center[1]) + "\n"

game = Game_of_luck(7)
game.start_game()
# print(game.generate_coordinates())
from pygame.math import Vector2
import pygame.time
import random
import sys



# # del------------------------------------------------del
# import pygame
# #import renderer

# pygame.init()
# #screen = pygame.display.set_mode((800, 600))
# # ---------------------------------------------------/




class Game_of_luck:

    FPS = 60
    WHEEL_CENTER = (400, 300)
    SLOWDOWN = 2

    def __init__(self, difficulty):
        self.wheel = Wheel_of_fortune(difficulty, Game_of_luck.WHEEL_CENTER)
        self.clock = pygame.time.Clock()

        self.closest = self.wheel.balls[0]
        self.should_stop = False
        self.slowdown = Game_of_luck.SLOWDOWN

    def find_closest_to_target(self):
        closest = Fortune_ball(Vector2(-1234, -1234), (0, 0))
        for ball in self.wheel.balls:
            if ball.vector[0] <= 0 and ball.vector[1] < 0 and ball.vector[0] > closest.vector[0]:
                closest = ball
        return closest

    def iter(self, input):
        self.clock.tick(Game_of_luck.FPS)
        self.wheel.rotate(self.wheel.speed / 100)
        self.wheel.speed -= self.slowdown

        if self.wheel.speed <= 30 and self.should_stop is False:
            self.closest = self.find_closest_to_target()
            if self.closest.vector[0] != -1234:
                self.wheel.speed = 30
                self.slowdown = 0
                self.should_stop = True

        if self.should_stop is True:
            if self.closest.vector[0] > 0:
                if self.closest.type == "bad_luck":
                    return False
                else:
                    return True 


    # def start_game(self):
    #     while True:
    #         self.clock.tick(Game_of_luck.FPS)
    #         self.wheel.rotate(self.wheel.speed / 100)
    #         self.wheel.speed -= self.slowdown

    #         if self.wheel.speed <= 30 and self.should_stop is False:
    #             self.closest = self.find_closest_to_target()
    #             if self.closest.vector[0] != -1234:
    #                 self.wheel.speed = 30
    #                 self.slowdown = 0
    #                 self.should_stop = True

    #         if self.should_stop is True:
    #             if self.closest.vector[0] > 0:
    #                 if self.closest.type == "bad_luck":
    #                     return False
    #                 else:
    #                     return True 

            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         sys.exit()

    def generate_coordinates(self):
        coordinates = ([ball.generate_coordinates() for ball in self.wheel.balls])
        coordinates.insert(0, ("gradient_white", 0, 0))
        coordinates.append(("arrow_of_fortune", 400, 55))
        return coordinates

    def handle_input(input):
        pass



    # to json
    # def __str__(self):
    #    # return json
    #     background = '"background" : {"image" : "gradient_white", "x" : 0, "y" : 0},  '
    #     arrow = '"arrow_of_fortune_id" : {"image" : "arrow_of_fortune", "x" : 400, "y" : 60}, '
    #     #arrow = " \"key_of_arrow_object\" : {\"image\" : \"images/arrow_of_fortune.png\", \"x\" : " + str(self.wheel.center[0])  + ", \"y\" + " + str(self.wheel.center[1] - Wheel_of_fortune.RADIUS - 20) + "  } "
    #     return "{ \"images\" : {"  + background + arrow + ("".join([str(ball) + ", " for ball in self.wheel.balls]))[:-2] + "} }"
    #     #return "Arrow_of_fortune\n20\n" + str(- Wheel_of_fortune.RADIUS) + "\n\n" + "".join([str(ball) + "\n" for ball in self.wheel.balls])




class Wheel_of_fortune:
    RADIUS = 200
    BALLS_COUNT = 11

    def __init__(self, good_balls_count, center):
        self.center = center
        self.good_balls_count = good_balls_count
        self.speed = random.randint(800, 1200)
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

    # to json
    # def __str__(self):
    #     return json.dumps({str(id(self)) : {'image' : self.type, 'x' : self.vector[0] + self.wheel_center[0], \
    #         'y': self.vector[1] + self.wheel_center[1]}})[1:][:-1]





# #test ------------------------------   ///////////////////////
# game = Game_of_luck(3)
# print(game.generate_coordinates())
# print()
# game.iter(None)
# print(game.generate_coordinates())
# #print(game.wheel.balls[0])
# #print()
# #print(game)
# #-----------------------
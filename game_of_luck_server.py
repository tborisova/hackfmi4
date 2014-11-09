from pygame.math import Vector2
import pygame.time
import random
import sys

<<<<<<< HEAD:game_of_luck.py

# # del------------------------------------------------del
# import pygame
# #import renderer
# pygame.init()
# #screen = pygame.display.set_mode((800, 600))
# # ---------------------------------------------------/


class Game_of_luck:

from time import sleep, localtime
from weakref import WeakKeyDictionary

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel

class ClientChannel(Channel):
    
    def __init__(self, *args, **kwargs):
        self.nickname = "anonymous"
        Channel.__init__(self, *args, **kwargs)
  
    def Close(self):
        self._server.DelPlayer(self)
    
    def Network_print_game_state(self, data):
        data1 = self._server.do_stuff()        
        
        objects = self._server.generate_coordinates()
        self._server.SendToAll({'action': 'render_game_state', 'objects': objects, 'should_stop': data1['should_stop'], 'closest_type': data1['closest_type']})

    def Network_player_move(self, data):
        self._server.player.move(data['move'])

class Game_of_luck(Server):

    channelClass = ClientChannel
    FPS = 60
    WHEEL_CENTER = (400, 300)
    SLOWDOWN = 6

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

    def iter(self, keyboard_input, mouse_input):
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

    def additional_params(self):
        return {}

    def AddPlayer(self, player):
        self.players[player] = True

    def DelPlayer(self, player):
        self.players[player] = False

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
        self.speed = random.randint(400,800)
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

   
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: {0} host:port".format(sys.argv[0]))
        print("e.g. {0} localhost:31425".format(sys.argv[0]))
    else:
        host, port = sys.argv[1].split(":")
        s = Game_of_luck(localaddr=(host, int(port)))
        difficulty = 3
        s.Launch(difficulty)


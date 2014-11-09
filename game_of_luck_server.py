from pygame.math import Vector2
import pygame.time
import random
import sys

from time import sleep, localtime
from weakref import WeakKeyDictionary
from get_ip import check_for_internet_conection as get_ip
from PodSixNet.Server import Server
from PodSixNet.Channel import Channel


class ClientChannel(Channel):

    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)

    def Close(self):
        self._server.DelPlayer(self)

    def Network_print_game_state(self, data):
        data1 = self._server.do_stuff()

        objects = self._server.generate_coordinates()
        self._server.SendToAll({'action': 'render_game_state',
                                'objects': objects,
                                'should_stop': data1['should_stop'],
                                'closest_type': data1['closest_type']})

    def Network_player_move(self, data):
        if self._server.player_can_write(self):
            self._server.player.move(data['move'])


class Game_of_luck(Server):

    channelClass = ClientChannel
    FPS = 60
    WHEEL_CENTER = (400, 300)
    SLOWDOWN = 2

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.players = WeakKeyDictionary()
        self.players_order = WeakKeyDictionary()
        self.current_index = 0
        self.clock = pygame.time.Clock()
        print('Server launched')

    def player_can_write(self, channel):
        return self.players_order[channel] == 0

    def do_stuff(self):
        data = {}
        self.clock.tick(Game_of_luck.FPS)
        self.wheel.rotate(self.wheel.speed / 100)
        self.wheel.speed -= self.slowdown

        if self.wheel.speed <= 30 and self.should_stop is False:
            closest = self.find_closest_to_target()
            if closest.vector[0] != -1234:
                self.wheel.speed = 30
                self.slowdown = 0
                self.should_stop = True

        closest_type = True
        if self.should_stop is True:
            data['should_stop'] = True
            if closest.vector[0] > 0:
                if closest.type == "bad_luck":
                    closest_type = False
                else:
                    closest_type = True
        else:
            data['should_stop'] = False
        data['closest_type'] = closest_type
        return data

    def Launch(self, difficulty):
        self.wheel = Wheel_of_fortune(difficulty, Game_of_luck.WHEEL_CENTER)
        self.closest = self.wheel.balls[0]
        self.should_stop = False
        self.slowdown = Game_of_luck.SLOWDOWN

        while True:
            self.Pump()
            sleep(0.0001)

    def Connected(self, channel, addr):
        if self.current_index < 2:
            self.AddPlayer(channel)

    def AddPlayer(self, player):
        self.players[player] = True
        self.players_order[player] = self.current_index
        self.current_index += 1

    def DelPlayer(self, player):
        self.players[player] = False

    def SendToAll(self, data):
        [p.Send(data) for p in self.players]

    def find_closest_to_target(self):
        closest = Fortune_ball(Vector2(-1234, -1234), (0, 0))
        for ball in self.wheel.balls:
            if ball.vector[0] <= 0 and ball.vector[
                    1] < 0 and ball.vector[0] > closest.vector[0]:
                closest = ball
        return closest

    def generate_coordinates(self):
        coordinates = ([ball.generate_coordinates()
                        for ball in self.wheel.balls])
        coordinates.insert(0, ("gradient_white", 0, 0))
        coordinates.append(("arrow_of_fortune", 400, 55))
        return coordinates


class Wheel_of_fortune:
    RADIUS = 200
    BALLS_COUNT = 11

    def __init__(self, good_balls_count, center):
        self.center = center
        self.good_balls_count = good_balls_count
        self.speed = random.randint(400, 800)
        self.balls = [
            Fortune_ball(
                Vector2(
                    0,
                    Wheel_of_fortune.RADIUS).rotate(
                    (i * 360) / Wheel_of_fortune.BALLS_COUNT),
                center) for i in range(
                Wheel_of_fortune.BALLS_COUNT)]

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
        return (
            self.type,
            self.vector.x +
            self.wheel_center[0],
            self.vector.y +
            self.wheel_center[1])

if __name__ == "__main__":
    host = get_ip()
    s = Game_of_luck(localaddr=(host, int(31425)))
    s.Launch(5)

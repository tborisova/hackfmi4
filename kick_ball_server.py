from pygame.locals import *
import pygame
import math
import json
import socket
from get_ip import check_for_internet_conection as get_ip
import sys

from time import sleep, localtime
from weakref import WeakKeyDictionary

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel
from settings import *


class ClientChannel(Channel):

    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)

    def Close(self):
        self._server.game_over = True
        self._server.DelPlayer(self)

    def Network_print_game_state(self, data):
        self._server.update(self)
        self._server.SendToAll({'action': 'game_state',
                                'get_json': self._server.get_json(),
                                'score': self._server.score,
                                'newimg_angle': self._server.ball.angle,
                                'ball_rect_x': self._server.ball.rect.x,
                                'ball_rect_y': self._server.ball.rect.y,
                                'ball_rect_h': self._server.ball.rect.height,
                                'ball_rect_w': self._server.ball.rect.width,
                                'highscore': self._server.highscore})

    def Network_mouse_pos(self, data):
        if self._server.player_can_write(self):
            self._server.pointer.rect.x = data['x']
            self._server.pointer.rect.y = data['y']


class Ball(pygame.sprite.Sprite):

    def __init__(self, x, y, image_name='ball.png'):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(IMAGES_PATH + image_name)
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.gravity = GRAVITY
        self.cap = CAP
        self.bounce = BOUNCE
        self.friction = FRICTION
        self.kick = KICK
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.on_ground = False
        self.spin = 0
        self.angle = 0
        self.center()

    def center(self):
        self.rect.centerx, self.rect.centery = CENTER
        self.x = self.rect.x
        self.y = self.rect.y

    def update(self):
        self.x += self.dx / 2
        self.y += self.dy / 2
        self.angle += self.spin
        if self.angle < 0:
            self.angle += 360
        if self.angle > 360:
            self.angle -= 360
        if not self.on_ground:
            self.dy += self.gravity
        if self.dy > self.cap:
            self.dy = self.cap
        if self.on_ground:
            self.dx *= self.friction
            self.spin = -self.dx
        if self.on_ground and abs(self.dx) - 0.5 < 0:
            self.dx = 0
            self.spin = -self.dx
        self.rect.x = self.x
        self.rect.y = self.y


class Pointer(pygame.sprite.Sprite):

    def __init__(self):
        self.rect = pygame.Rect(
            pygame.mouse.get_pos()[0],
            pygame.mouse.get_pos()[1],
            1,
            1)
        self.mask = pygame.Mask((1, 1))
        self.mask.set_at((0, 0), 1)


class Game(Server):
    channelClass = ClientChannel

    def player_can_write(self, channel):
        return True

    def Connected(self, channel, addr):
        if self.current_index < 2:
            self.AddPlayer(channel)

    def DelPlayer(self, player):
        self.players[player] = False

    def AddPlayer(self, player):
        self.players[player] = True
        self.players_order[player] = self.current_index
        self.current_index += 1

    def SendToAll(self, data):
        [p.Send(data) for p in self.players]

    def __init__(self, *args, **kwargs):
        pygame.init()
        Server.__init__(self, *args, **kwargs)
        self.players = WeakKeyDictionary()
        self.players_order = WeakKeyDictionary()
        self.current_index = 0
        self.ball = Ball(*CENTER)
        self.pointer = Pointer()
        self.score = 0
        self.difficulty = 3
        self.highscore = 0
        self.paused = False
        self.subrect = self.ball.image.get_rect()
        self.subrect.width = 84
        self.subrect.height = 83
        self.newimg = self.ball.image
        self.tries = TRIES
        self.game_over = False
        print('Server launched')
        
    def check_for_collision(self):
        if pygame.sprite.collide_mask(
                self.pointer,
                self.ball) and not self.paused:
            if self.ball.mask.get_at(
                    (int(self.pointer.rect.x - self.ball.x), int(self.pointer.rect.y - self.ball.y))):
                hit = self.ball.mask.overlap(self.pointer.mask, (int(
                    self.pointer.rect.x - self.ball.x), int(self.pointer.rect.y - self.ball.y)))
                hit = (
                    hit[0] -
                    self.ball.rect.width /
                    2,
                    hit[1] -
                    self.ball.rect.height /
                    2)
                angle = math.degrees(math.atan2(hit[0], hit[1]))
                dx = 30 * math.cos(math.radians(angle + 90))
                dy = 30 * math.sin(math.radians(angle - 90))
                self.ball.dx = dx
                self.ball.dy = dy
                self.ball.on_ground = False
                self.ball.spin = -dx / 5
                self.score += 1

    def update(self, player):
        self.check_for_collision()
        if self.ball.x > WINDOWWIDTH - self.ball.rect.width:
            self.ball.x = WINDOWWIDTH - self.ball.rect.width
            self.ball.dx = -self.ball.dx * self.ball.friction
            self.ball.spin = self.ball.dy
        if self.ball.y > WINDOWHEIGHT - self.ball.rect.height:
            if self.score > 0:
                self.tries -= 1
                self.score = 0
            self.ball.y = WINDOWHEIGHT - self.ball.rect.height
            if not self.ball.on_ground:
                self.ball.dx *= self.ball.friction
            self.ball.spin = -self.ball.dx
            if (self.ball.dy * self.ball.bounce) - 5 > 0:
                self.ball.dy = -self.ball.dy * self.ball.bounce
            else:
                self.ball.dy = 0
                self.ball.on_ground = True
        if self.ball.x < 0:
            self.ball.x = 0
            self.ball.dx = -self.ball.dx * self.ball.bounce
            self.ball.spin = -self.ball.dy

        if self.score > self.highscore:
            self.highscore = self.score

        self.ball.update()
        print(self.tries)

        if self.tries <= 0:
            self.game_over = True
            self.SendToAll({'action': 'game_over',
                            'data': self.get_json(),
                            'highscore': self.highscore})
            self.DelPlayer(player)
            pygame.quit()

    def get_json(self):
        return json.dumps(
            {'images': {str(id(self)): {'image': 'ball', 'x': self.ball.x, 'y': self.ball.y}}})

    def Launch(self):
        while True:
            self.Pump()
            sleep(0.0001)

if __name__ == "__main__":
    host = get_ip()
    s = Game(localaddr=(host, int(31425)))
    s.Launch()

from pygame.locals import *
import pygame
import math
import json
import sys

from time import sleep, localtime
from weakref import WeakKeyDictionary

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel
from settings import *


class ClientChannel(Channel):

    def __init__(self, *args, **kwargs):
        self.nickname = "anonymous"
        Channel.__init__(self, *args, **kwargs)
  
    def Close(self):
        self._server.game_over = True
        self._server.DelPlayer(self)
  
    def Network_print_game_state(self, data):
        self._server.update()
        self._server.SendToAll({'action': 'game_state', 'get_json': self._server.get_json(), 'score': self._server.score, 
                               'newimg_angle': self._server.ball.angle, 'ball_rect_x': self._server.ball.rect.x, 'ball_rect_y': self._server.ball.rect.y, 
                               'ball_rect_h': self._server.ball.rect.height, 'ball_rect_w': self._server.ball.rect.width, 'highscore': self._server.highscore})
                               #'mouse_x': self._server.pointer.rect.x, 'mouse_y': self._server.pointer.rect.y})

    def Network_mouse_pos(self, data):
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
        print("HERE")
        print(self.angle)

class Pointer(pygame.sprite.Sprite):

    def __init__(self):
        self.rect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)
        self.mask = pygame.Mask((1, 1))
        self.mask.set_at((0, 0), 1)


class Game(Server):
    channelClass = ClientChannel

    # this is called when a player is connected
    def Connected(self, channel, addr):
        self.AddPlayer(channel)

    def DelPlayer(self, player):
        # print("Deleting Player {0}".format(str(player.addr)))
        del self.players[player]
        self.SendPlayers()

    def AddPlayer(self, player):
        # if len(self.players) < 2:
        # print("New Player {0}".format(str(player.addr)))
        self.players[player] = True
        self.SendPlayers()
        # print("players {0}".format([p for p in self.players]))

    def SendPlayers(self):
        self.SendToAll({"action": "players", "players": [p.nickname for p in self.players]})
    
    def SendToAll(self, data):
        # print("HERE")
        # print(data)
        [p.Send(data) for p in self.players]

    def __init__(self, *args, **kwargs):
        pygame.init()
        Server.__init__(self, *args, **kwargs)
        self.players = WeakKeyDictionary()
        print('Server launched')
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

    def check_for_collision(self):
        if pygame.sprite.collide_mask(self.pointer, self.ball) and not self.paused:
            if self.ball.mask.get_at((int(self.pointer.rect.x - self.ball.x), int(self.pointer.rect.y - self.ball.y))):
                hit = self.ball.mask.overlap(
                    self.pointer.mask, (int(self.pointer.rect.x - self.ball.x), int(self.pointer.rect.y - self.ball.y)))
                hit = (
                    hit[0] - self.ball.rect.width / 2, hit[1] - self.ball.rect.height / 2)
                angle = math.degrees(math.atan2(hit[0], hit[1]))
                dx = 30 * math.cos(math.radians(angle + 90))
                dy = 30 * math.sin(math.radians(angle - 90))
                self.ball.dx = dx
                self.ball.dy = dy
                self.ball.on_ground = False
                self.ball.spin = -dx / 5
                self.score += 1

    def update(self):
        self.check_for_collision()
        if self.ball.x > WINDOWWIDTH - self.ball.rect.width:
            self.ball.x = WINDOWWIDTH - self.ball.rect.width
            self.ball.dx = -self.ball.dx * self.ball.friction
            self.ball.spin = self.ball.dy
        if self.ball.y > WINDOWHEIGHT - self.ball.rect.height:
            if not self.paused and self.score > 0:
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
            #pokazvane na topkata
        self.ball.update()
        # rotated = pygame.transform.rotate(self.ball.image, self.ball.angle)
        # size = rotated.get_size()
        # self.subrect.centerx = size[0] / 2
        # self.subrect.centery = size[1] / 2
        # self.newimg = rotated.subsurface(self.subrect)

        if self.tries == 0:
            self.game_over = True
            self.SendToAll({'action': 'game_over', 'data' : self.get_json(), 'highscore': self.highscore})
            pygame.quit()
            exit()

    def get_json(self):
        return json.dumps({'images': {str(id(self)): {'image': 'ball', 'x': self.ball.x, 'y': self.ball.y}}})

    def Launch(self):
        while True:
            self.Pump()
            sleep(0.0001)

if __name__ == "__main__":
    # get command line argument of server, port
    if len(sys.argv) != 2:
        print("Usage: {0} host:port".format(sys.argv[0]))
        print("e.g. {0} localhost:31425".format(sys.argv[0]))
    else:
        host, port = sys.argv[1].split(":")
        s = Game(localaddr=(host, int(port)))
        s.Launch()


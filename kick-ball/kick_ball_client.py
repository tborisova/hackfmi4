from pygame.locals import *
import pygame
import math
import json
import sys

from kick_ball_server import Game
from settings import *
from time import sleep
from sys import stdin, exit

from PodSixNet.Connection import connection, ConnectionListener


class Gui(ConnectionListener):

    def __init__(self, difficulty, host, port):
        pygame.init()
        pygame.display.set_caption('Kick Ball')
        pygame.display.set_icon(pygame.image.load('../images/icon.png'))
        self.screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        self.screen.fill((0, 0, 0))
        self.screen_center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        self.clock = pygame.time.Clock()
        self.font1 = pygame.font.Font('./data/font.ttf', 40)
        self.font2 = pygame.font.Font('./data/font.ttf', 22)
        self.font3 = pygame.font.Font('./data/font.ttf', 52)
        self.font4 = pygame.font.Font('./data/font.ttf', 16)
        self.Connect((host, port))
        connection.Send({'action': 'print_game_state'})
        pygame.display.flip()
        
    def Network_game_state(self, data):
          self.clock.tick(60)
          self.handle_game_event()
          # print(data.keys())
          self.screen.fill((0, 0, 0))
          # print(data)
          self.draw_info(data['score'], data['highscore'])
          pygame.display.flip()
          connection.Send({'action': 'print_game_state'})


    def Loop(self):
        connection.Pump()
        self.Pump()
        # connection.send({'action': 'print_game_state', 'data': 'blk'})

    # def start_game(self):
    #       connection.send({'action': 'print_game_state'})

    def Network_connected(self, data):
        print('dddd')
        print("You are now connected to the server")
    
    def Network_error(self, data):
        print("error: {0}".format(data['error'][1]))
        connection.Close()
    
    def Network_disconnected(self, data):
        print('Server disconnected')
        print(data)
        exit()

    def handle_game_event(self):
        for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
        x, y = pygame.mouse.get_pos()
        connection.Send({'action': 'mouse_pos', 'x' : x, 'y': y})

    def draw_message(self, message):
        font = pygame.font.Font('./data/font.ttf', 52)
        label = font.render(message, 1, WHITE)
        rect = label.get_rect()
        rect.center = CENTER
        self.screen.blit(label, rect)

    def draw_info(self, score, highscore):
        score_text = self.font1.render(str(score), 1, (255, 155, 155))
        score_rect = score_text.get_rect()
        score_rect.x = 20
        highscore_text = self.font2.render(str(highscore), 1, (255, 255, 255))
        highscore_rect = highscore_text.get_rect()
        highscore_rect.y = score_rect.bottom + 5
        highscore_rect.x = 5
        title = self.font3.render('Keep the ball in the air!', 1, (255, 255, 255))
        title_rect = title.get_rect()
        title_rect.centerx = WINDOWWIDTH / 2
        title_rect.y = score_rect.centery
        self.screen.blit(score_text, score_rect)
        self.screen.blit(highscore_text, highscore_rect)
        self.screen.blit(title, title_rect)

if __name__ == "__main__": 
    if len(sys.argv) != 2:
        print("Usage: {0} host:port".format(sys.argv[0]))
        print("e.g. {0} localhost:31425".sys.argv[0])
    else:
        host, port = sys.argv[1].split(":")
        c = Gui(10, host, int(port))
        while 1:
            c.Loop()
            sleep(0.001)

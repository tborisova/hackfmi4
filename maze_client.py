import sys
import random
import json
import time
import pygame
from get_ip import check_for_internet_conection as get_ip
import time
from event_handler import unparse

from renderer import draw_everything

from time import sleep, localtime
from weakref import WeakKeyDictionary

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel
from PodSixNet.Connection import connection, ConnectionListener


class ClientMaze(ConnectionListener):

    def __init__(self, host, port):
        try:
            pygame.init()
            self.Connect((host, int(port)))
            self.screen = pygame.display.set_mode((800, 600))
        except:
            exit()

    def Loop(self):
        connection.Send({'action': 'print_game_state'})
        connection.Pump()
        self.Pump()

    def Network_connected(self, data):
        print("You are now connected to the server")

    def Network_error(self, data):
        print("error: {0}".format(data['error'][1]))
        connection.Close()

    def Network_disconnected(self, data):
        print('Server disconnected')
        exit()

    def Network_render_game_state(self, data):
        keys = pygame.key.get_pressed()

        if data['player_wins']:
            sys.exit()
        elif data['time_is_up']:
            sys.exit()
        if keys[pygame.K_LEFT]:
            connection.Send({'action': 'player_move', 'move': 'left'})
            sleep(0.1)
        if keys[pygame.K_RIGHT]:
            connection.Send({'action': 'player_move', 'move': 'right'})
            sleep(0.1)
        if keys[pygame.K_DOWN]:
            connection.Send({'action': 'player_move', 'move': 'down'})
            sleep(0.1)
        if keys[pygame.K_UP]:
            connection.Send({'action': 'player_move', 'move': 'up'})
            sleep(0.1)

        draw_everything(self.screen, data['objects'])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.update()

if __name__ == "__main__":
    host = get_ip()
    s = ClientMaze(host, int(31425))
    s.Loop()

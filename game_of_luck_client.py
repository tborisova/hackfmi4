import sys
import random
import json
import time
import pygame
import time
from renderer import draw_everything
from event_handler import unparse
from time import sleep, localtime
from weakref import WeakKeyDictionary

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel
from PodSixNet.Connection import connection, ConnectionListener


class ClientLuck(ConnectionListener):

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
        draw_everything(self.screen, data['objects'])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        pygame.display.update()

        if data['should_stop']:
            return data['closest_type']
            exit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: {0} host:port".format(sys.argv[0]))
        print("e.g. {0} localhost:31425", sys.argv[0])
    else:
        host, port = sys.argv[1].split(":")
        c = ClientLuck(host, int(port))
        while True:
            c.Loop()
            sleep(0.01)

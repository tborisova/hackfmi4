from PodSixNet.Connection import connection, ConnectionListener
import pygame
import time
from time import sleep, localtime
import game_of_luck
import renderer
import sys

class Client(ConnectionListener):

    def __init__(self, host, port):
        try:
            pygame.init()
            self.Connect((host, int(port)))
            self.screen = pygame.display.set_mode((800, 600))
        except:
            exit()

    def Loop(self):
        connection.Send({'action': 'handle_input', 'input' : pygame.key.get_pressed()})
        connection.Pump()
        self.Pump()

    def Network_connected(self, data):
        print("You are now connected to the server")

    def Network_error(self, data):
        print("error: {0}".format(data['error'][1]))
        connection.Close()

    def Network_disconnected(self, data):
        # print()
        # print('Server disconnected')
        # print()
        exit()


    def Network_draw_everything(self, data):
        #print(data)
        renderer.draw_everything(self.screen, data['objects'])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
              sys.exit()
        x, y = pygame.mouse.get_pos()
        connection.Send({'action': 'mouse_pos', 'x': x, 'y': y})
        pygame.display.update()
       # if data['should_stop']:
        #    return data['closest_type']
        #    sys.exit()

        #keys = pygame.key.get_pressed()






if __name__ == "__main__": 
    # if len(sys.argv) != 2:
    #     print("Usage: {0} host:port".format(sys.argv[0]))
    #     print("e.g. {0} localhost:31425",sys.argv[0])
    # else:
    host = 'localhost'
    port =  22022
    c = Client(host, int(port))

    while True:
        c.Loop()
        sleep(0.01)
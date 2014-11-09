import sys
import random
import json
import time
import pygame
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
          time.sleep(0.01)
      if keys[pygame.K_RIGHT]:
          connection.Send({'action': 'player_move', 'move': 'right'})
          time.sleep(0.01)
      if keys[pygame.K_DOWN]:
          connection.Send({'action': 'player_move', 'move': 'down'})
          time.sleep(0.01)
      if keys[pygame.K_UP]:
          connection.Send({'action': 'player_move', 'move': 'up'})
          time.sleep(0.01)

      draw_everything(self.screen, data['objects'])

      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              sys.exit()
      pygame.display.update()
      
if __name__ == "__main__": 
    if len(sys.argv) != 2:
        print("Usage: {0} host:port".format(sys.argv[0]))
        print("e.g. {0} localhost:31425",sys.argv[0])
    else:
        host, port = sys.argv[1].split(":")
        c = ClientMaze(host, int(port))
        while 1:
            c.Loop()
            sleep(0.01)

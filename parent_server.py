import sys
#from event_handler import unparse

from weakref import WeakKeyDictionary
from time import sleep, localtime

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel

import kick_ball
import game_of_luck


class ClientChannel(Channel):
    def __init__(self, *args, **kwargs):
        self.nickname = "anonymous"
        Channel.__init__(self, *args, **kwargs)
  
    def Close(self):
        print("CLOSING")

    def Network_set_game(self, data):
        self._server.current_game = data['game'] # this is a string, should be made into class - search how 

    def Network_handle_input(self, data):
        print(data)
        # if self._server.player_can_write(self):
        self._server.handle_input(data['keyboard_input'], data['mouse_input'])
        self._server.SendToAll({'action' : 'draw_everything', 'objects' : self._server.current_game.generate_coordinates(), 'additional_params' : self._server.current_game.additional_params()})


class GameServer(Server):

    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
      #  print(args)
      #  print(kwargs)
        self.players_order = WeakKeyDictionary()
        self.players = WeakKeyDictionary()
        self.current_index = 0
        print('Server launched')
        self.main_application = None #... not None ...
        self.current_game = kick_ball.Game(5)

    def player_can_write(self, channel):
        return self.players_order[channel] == 0

    def Connected(self, channel, addr):
        if self.current_index < 2:
            self.AddPlayer(channel)

    def AddPlayer(self, player):
        self.players[player] = True
        self.players_order[player] = self.current_index
        self.current_index += 1

    def SendToAll(self, data):
        [p.Send(data) for p in self.players]

    def Launch(self):
        while True:

            self.Pump()
            sleep(0.0001)

    def handle_input(self, keyboard_intput=None, mouse_input=None):
        if self.current_game is not None:
            result = self.current_game.iter(keyboard_intput, mouse_input)
            if result is not None:
                self.current_game = None
                # self.SendToAll({'action' : 'draw_everything', 'objects' : self.main_application.generate_coordinates()})
                sys.exit()
#exit
        else:
            #
            pass
            #wait to pick game
        self.SendToAll({'action': 'draw_everything', 'objects': self.current_game.generate_coordinates()})
                                            #'player_wins': self.check_if_player_wins(), 'time_is_up': self._server.time_is_up()})




if __name__ == "__main__":
    # get command line argument of server, port
    # if len(sys.argv) != 2:
    #     print("Usage: {0} host:port".format(sys.argv[0]))
    #     print("e.g. {0} localhost:31425".format(sys.argv[0]))
    # else:
    #host, port = sys.argv[1].split(":")

    s = GameServer(localaddr=('10.0.201.111', 22022))
    s.current_game = kick_ball.Game(5)

    #s.urrent_game = maze_game.MazeGame(5)
    s.Launch()

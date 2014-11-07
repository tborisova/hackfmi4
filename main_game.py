__author__ = 'Stoyan'

from itertools import cycle

from player import Player
from BubbleTrouble.gui import start
from setup import *

class Game:

    def __init__(self):
        self.challenger = Player()
        self.challenged = Player()
        self.mini_game = None
        self.players = (self.challenger, self.challenged)
        self.player_on_turn = cycle(self.players)

    def change_roles(self):
        self.challenged, self.challenger = self.challenger, self.challenged

    def start_mini_game(self, difficulty):
        completed = self.mini_game.start(difficulty)
        if completed:
            self.player_on_turn.score += CHALLENGE_POINTS
        else:
            self.player_on_turn -= CHALLENGE_POINTS
        self.player_on_turn.next()

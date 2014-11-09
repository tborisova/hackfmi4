import socket
import pygame
pygame.init()
from hardcoded import *
from client import *
from parent_server import GameServer

FPS = 60
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


def check_for_internet_conection():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 0))
        return s.getsockname()[0]
    except OSError:
        return None


def __init__(self):
    self.init_graphics()
    self.clock = pygame.time.Clock()


def init_graphics(self):
    logo = pygame.transform.scale(images.images["logo"], (32, 32))
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Challenge Accepted", "Challenge Accepted")


# if __name__ == "__main__":
#
#    s = GameServer(localaddr=('10.0.201.111', 22022))
#    s.current_game = kick_ball.Game(5)
#    s.Launch()
#    host = '10.0.201.111'
#    port =  22022
#    c = Client(host, int(port))
if __name__ == "__main__":
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    ingame = False
    current_left_layout = "start"
    current_right_layout = None
    while True:
        events = pygame.event.get()
        if ingame:
            continue
        if current_left_layout is not None:
            update_elements(current_left_layout, events)
            draw_layout(screen, current_left_layout)
        if current_right_layout is not None:
            update_elements(current_right_layout, events)
            draw_layout(screen, current_right_layout)
        pygame.display.update()
       # c.Loop()
       # sleep(0.01)

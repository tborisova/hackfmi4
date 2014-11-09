import socket
import sys
import pygame
pygame.init()
from hardcoded import Layout
import images
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


def init_graphics():
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
ingame = False
LAYOUTS = Layout.load_layouts()
current_left_layout = "start"
current_right_layout = None


def start_conntrol():
    if LAYOUTS[current_left_layout].connect_to_server_button.clicked:
        globals()["current_right_layout"] = "connect_to_server"
    if LAYOUTS[current_left_layout].connect_to_server_button.clicked:
        globals()["current_right_layout"] = "create_server"
    if LAYOUTS[current_left_layout].connect_to_server_button.clicked:
        sys.exit()


def start_server_controll():
    if LAYOUTS[current_left_layout].connect_to_server_button.clicked:
        globals()["current_left_layout"] = "game"
        globals()["current_right_layout"] = None


if __name__ == "__main__":
    init_graphics()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    while True:
        events = pygame.event.get()
        if ingame:
            continue
        else:
            screen.fill((55, 155, 255))
        if current_left_layout is not None:
            LAYOUTS[current_left_layout].update_elements(events)
            LAYOUTS[current_left_layout].draw(screen)
        if current_right_layout is not None:
            LAYOUTS[current_right_layout].update_elements(events)
            LAYOUTS[current_right_layout].draw(srceen)
        pygame.display.update()
       # c.Loop()
       # sleep(0.01)

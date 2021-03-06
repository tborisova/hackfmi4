from pygame.locals import *
import pygame
import sys
from get_ip import check_for_internet_conection as get_ip

from settings import *
from time import sleep
from sys import stdin, exit

from PodSixNet.Connection import connection, ConnectionListener


class Gui(ConnectionListener):

    def __init__(self, difficulty, host, port):
        pygame.init()
        pygame.display.set_caption('Kick Ball')
        pygame.display.set_icon(pygame.image.load(IMAGES_PATH + 'icon.png'))
        self.screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        self.screen.blit(
            pygame.image.load(IMAGES_PATH + 'ball_background.png'), (0, 0))
        self.screen_center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        self.clock = pygame.time.Clock()
        self.font1 = pygame.font.Font(FONTS_PATH + 'font.tff', 40)
        self.font2 = pygame.font.Font(FONTS_PATH + 'font.tff', 22)
        self.font3 = pygame.font.Font(FONTS_PATH + 'font.tff', 52)
        self.font4 = pygame.font.Font(FONTS_PATH + 'font.tff', 16)
        try:
            self.Connect((host, int(port)))
        except:
            exit()
        connection.Send({'action': 'print_game_state'})
        pygame.display.flip()

    def Network_game_state(self, data):
        self.clock.tick(60)
        self.handle_game_event()
        self.screen.fill((0, 0, 0))
        self.draw_info(data)
        pygame.display.flip()

    def Loop(self):
        connection.Send({'action': 'print_game_state'})
        connection.Pump()
        self.Pump()

    def Network_players(self, data):
        print(data)

    def Network_connected(self, data):
        print("You are now connected to the server")

    def Network_error(self, data):
        print("error: {0}".format(data['error'][1]))
        connection.Close()

    def Network_disconnected(self, data):
        print('Server disconnected')
        print(data)
        exit()

    def Network_game_over(self, data):
        print(data)
        pygame.quit()
        sys.exit()

    def handle_game_event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            x, y = pygame.mouse.get_pos()
            connection.Send({'action': 'mouse_pos', 'x': x, 'y': y})

    def draw_message(self, message):
        font = pygame.font.Font(IMAGES_PATH + 'font.ttf', 52)

        label = font.render(message, 1, WHITE)
        rect = label.get_rect()
        rect.center = CENTER
        self.screen.blit(label, rect)

    def draw_info(self, data):
        score_text = self.font1.render(str(data['score']), 1, (255, 155, 155))
        score_rect = score_text.get_rect()
        score_rect.x = 20
        highscore_text = self.font2.render(
            str(data['highscore']), 1, (255, 255, 255))
        highscore_rect = highscore_text.get_rect()
        highscore_rect.y = score_rect.bottom + 5
        highscore_rect.x = 5
        title = self.font3.render(
            'Keep the ball in the air!', 1, (255, 255, 255))
        title_rect = title.get_rect()
        title_rect.centerx = WINDOWWIDTH / 2
        title_rect.y = score_rect.centery
        self.screen.blit(score_text, score_rect)
        self.screen.blit(highscore_text, highscore_rect)
        self.screen.blit(title, title_rect)
        rect = Rect(
            data['ball_rect_x'],
            data['ball_rect_y'],
            data['ball_rect_w'],
            data['ball_rect_h'])
        img = pygame.image.load(IMAGES_PATH + 'ball.png')
        rotated = pygame.transform.rotate(img, data['newimg_angle'])
        size = rotated.get_size()
        subrect = img.get_rect()
        subrect.width = 84
        subrect.height = 83
        subrect.centerx = size[0] / 2
        subrect.centery = size[1] / 2
        rotated_img = rotated.subsurface(subrect)
        self.screen.blit(rotated_img, rect)

if __name__ == "__main__":
    host = get_ip()
    s = Game(localaddr=(host, int(31425)))
    s.Launch()

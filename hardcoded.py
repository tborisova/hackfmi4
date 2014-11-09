import pygame
from gui_elements import *


class Layout:

    def __init__(self):
        self.input_boxes = []
        self.text_boxes = []
        self.buttons = []
        self.views = []

    def update_elements(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in self.buttons:
                        button.update_state(event.pos, True)
                    for input_box in self.input_boxes:
                        input_box.update_state(event.pos, True)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for button in self.buttons:
                        button.update_state(event.pos, False)
                    for input_box in self.input_boxes:
                        input_box.update_state(event.pos, False)
            elif event.type == pygame.KEYDOWN:
                if event.key in gui_elements.InputBox.HANDLED_KEYS:
                    for input_box in self.input_boxes:
                        input_box.handle_key_event(event.key)
        for button in self.buttons:
            button.update_state(pygame.mouse.get_pos(), None)
        for input_box in self.input_boxes:
            input_box.update_state(pygame.mouse.get_pos(), None)


# Initialising elements for the Game Menu
first_player_text = TextBox(
    (200, 50), (200, 40), "Player 1", (0, 0, 0), (r"data/font.ttf", 100))
second_player_text = TextBox(
    (200, 50), (600, 40), "Player 2", (0, 0, 0), (r"data/font.ttf", 100))
maze_button = Button(
    "default", (255, 50), (155, 300), "Maze Runner", None, (0, 0, 0), (None, 100))
maze_input = InputBox(
    (70, 35), (343, 300), "0", (0, 0, 0), (None, 40), (255, 255, 255), (0, 0, 0), 1)
game_of_luck_button = Button(
    "default", (255, 50), (155, 380), "Game of Luck", None, (0, 0, 0), (None, 100))
game_of_luck_input = InputBox(
    (70, 35), (343, 380), "0", (0, 0, 0), (None, 40), (255, 255, 255), (0, 0, 0), 1)
kick_the_ball_button = Button(
    "default", (255, 50), (155, 460), "Kick the Ball", None, (0, 0, 0), (None, 100))
kick_the_ball_input = InputBox(
    (70, 35), (343, 460), "0", (0, 0, 0), (None, 40), (255, 255, 255), (0, 0, 0), 1)

game_input_boxes = [maze_input, game_of_luck_input, kick_the_ball_input]
game_buttons = [maze_button, game_of_luck_button, kick_the_ball_button]
game_text_boxes = [first_player_text]  # , second_player_text]
game_views = game_input_boxes + game_buttons + game_text_boxes

for input_box in game_input_boxes:
    input_box.char_limit = 4
    input_box.handled_chars = set(range(pygame.K_0, pygame.K_9 + 1))


# Initialising elements for the start menu
start_title_text = TextBox(
    (200, 50), (200, 40), "Challange Accepted", (0, 0, 0), (r"data/font.ttf", 100))
start_server_setup_title_text = TextBox(
    (200, 50), (600, 40), "Setup Server", (0, 0, 0), (r"data/font.ttf", 100))
start_connect_to_server_title_text = TextBox(
    (200, 50), (600, 40), "Connect to Server", (0, 0, 0), (r"data/font.ttf", 100))
start_connect_to_server_button = Button(
    "default", (350, 50), (200, 300), "Connect to Server", None, (0, 0, 0), (None, 100))
start_server_setup_button = Button(
    "default", (350, 50), (200, 380), "Setup Server", None, (0, 0, 0), (None, 100))
start_exit_button = Button(
    "default", (350, 50), (200, 460), "Exit", None, (0, 0, 0), (None, 100))
# maze_input = InputBox(
#     (70, 35), (343, 300), "000", (0, 0, 0), (None, 40), (255, 255, 255), (0, 0, 0), 1)
# game_of_luck_input = InputBox(
#     (70, 35), (343, 380), "000", (0, 0, 0), (None, 40), (255, 255, 255), (0, 0, 0), 1)
# kick_the_ball_input = InputBox(
#     (70, 35), (343, 460), "000", (0, 0, 0), (None, 40), (255, 255, 255), (0, 0, 0), 1)

start_side = 0
start_background = (55, 155, 255)
start_input_boxes = []
start_buttons = [
    start_connect_to_server_button,
    start_server_setup_button,
    start_exit_button]
start_text_boxes = [start_title_text]
start_views = start_input_boxes + start_buttons + start_text_boxes


def draw_layout(surface, layout):
    side = globals()[layout + "_side"]
    containing_rect = pygame.Rect((0, side * 400), (400, 600))
    pygame.draw.rect(
        surface,
        globals()[layout + "_background"],
        containing_rect)
    for view in globals()[layout + "_views"]:
        view.draw(surface)
    pygame.draw.rect(surface, (0, 0, 0), containing_rect, 2)

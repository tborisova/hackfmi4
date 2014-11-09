from gui_elements import *

first_player_text = TextBox(
    (200, 50), (200, 40), "Player 1", (0, 0, 0), (r"kick-ball/data/font.ttf", 100))
second_player_text = TextBox(
    (200, 50), (600, 40), "Player 2", (0, 0, 0), (r"kick-ball/data/font.ttf", 100))
maze_button = Button(
    "default", (255, 50), (155, 300), "Maze Runner", None, (0, 0, 0), (None, 100))
maze_input = InputBox((70, 35), (343, 300), "000",
                      (0, 0, 0), (None, 40), (255, 255, 255), (0, 0, 0), 1)
game_of_luck_button = Button(
    "default", (255, 50), (155, 380), "Game of Luck", None, (0, 0, 0), (None, 100))
game_of_luck_input = InputBox(
    (70, 35), (343, 380), "000", (0, 0, 0), (None, 40), (255, 255, 255), (0, 0, 0), 1)
kick_the_ball_button = Button(
    "default", (255, 50), (155, 460), "Kick the Ball", None, (0, 0, 0), (None, 100))
kick_the_ball_input = InputBox(
    (70, 35), (343, 460), "000", (0, 0, 0), (None, 40), (255, 255, 255), (0, 0, 0), 1)

game_input_boxes = [maze_input, game_of_luck_input, kick_the_ball_input]
game_buttons = [maze_button, game_of_luck_button, kick_the_ball_button]
game_text_boxes = [first_player_text, second_player_text]
game_views = game_input_boxes + game_buttons + game_text_boxes

for input_box in game_input_boxes:
    input_box.char_limit = 4
    input_box.handled_chars = set(range(pygame.K_0, pygame.K_9 + 1))


def update_elements(surface, layout, events):
    input_boxes = globals()[layout + "_input_boxes"]
    buttons = globals()[layout + "_input_boxes"]
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in buttons:
                    button.update_state(event.pos, True)
                for input_box in input_boxes:
                    input_box.update_state(event.pos, True)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                for button in buttons:
                    button.update_state(event.pos, False)
                for input_box in input_boxes:
                    input_box.update_state(event.pos, False)
        elif event.type == pygame.KEYDOWN:
            if event.key in gui_elements.InputBox.HANDLED_KEYS:
                for input_box in input_boxes:
                    input_box.handle_key_event(event.key)
    for button in buttons:
        button.update_state(pygame.mouse.get_pos(), None)
    for input_box in input_boxes:
        input_box.update_state(pygame.mouse.get_pos(), None)

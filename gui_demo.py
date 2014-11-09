import pygame
import sys
import gui_elements

pygame.init()

screen = pygame.display.set_mode((800, 600))

clock = pygame.time.Clock()

first_player_text = gui_elements.TextBox(
    (300, 100), (200, 100), "Challenge Accepted?", (0, 0, 0), (r"data/fonts/font.tff", 150))

create_button = gui_elements.Button(
    "default", (255, 50), (200, 300), "Create", None, (0, 0, 0), (None, 100))

join_button = gui_elements.Button(
    "default", (255, 50), (200, 380), "Join", None, (0, 0, 0), (None, 100))


maze_button2 = gui_elements.Button(
    "default", (255, 50), (555, 300), "Maze Runner", None, (0, 0, 0), (None, 100))
maze_input2 = gui_elements.InputBox(
    (70, 35), (743, 300), "", (0, 0, 0), (None, 40), (255, 255, 255), (0, 0, 0), 1)

game_of_luck_button2 = gui_elements.Button(
    "default", (255, 50), (555, 380), "Game of Luck", None, (0, 0, 0), (None, 100))
game_of_luck_input2 = gui_elements.InputBox(
    (70, 35), (743, 380), "", (0, 0, 0), (None, 40), (255, 255, 255), (0, 0, 0), 1)

kick_the_ball_button2 = gui_elements.Button(
    "default", (255, 50), (555, 460), "Kick the Ball", None, (0, 0, 0), (None, 59))
kick_the_ball_input2 = gui_elements.InputBox(
    (70, 35), (743, 460), "", (0, 0, 0), (None, 40), (255, 255, 255), (0, 0, 0), 1)

# ip_text = gui_elements.TextBox(
#     (60, 50), (450, 90), "IP:", (0, 0, 0), (r"data/fonts/font.tff", 40))
# ip_input0 = gui_elements.InputBox(
#     (50, 40), (500, 93), "000", (0, 0, 0), (None, 40), (255, 255, 255), (0, 0, 0), 1)
# ip_input1 = gui_elements.InputBox(
#     (50, 40), (560, 93), "000", (0, 0, 0), (None, 40), (255, 255, 255), (0, 0, 0), 1)
# ip_input2 = gui_elements.InputBox(
#     (50, 40), (620, 93), "000", (0, 0, 0), (None, 40), (255, 255, 255), (0, 0, 0), 1)
# ip_input3 = gui_elements.InputBox(
#     (50, 40), (680, 93), "000", (0, 0, 0), (None, 40), (255, 255, 255), (0, 0, 0), 1)
#
# ip_text = gui_elements.TextBox(
#     (60, 50), (450, 90), "IP:", (0, 0, 0), (r"data/fonts/font.tff", 40))


input_boxes = [maze_input2, game_of_luck_input2, kick_the_ball_input2]
buttons = [join_button, create_button, maze_button2, game_of_luck_button2, kick_the_ball_button2]
text_boxes = [first_player_text, ]
views = input_boxes + buttons + text_boxes

for input_box in input_boxes:
    input_box.char_limit = 4
    input_box.handled_chars = set(range(pygame.K_0, pygame.K_9 + 1))

while True:
    for event in pygame.event.get():
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

    screen.fill((55, 155, 255))
    for view in views:
        view.draw(screen)
    pygame.draw.line(screen, (0, 0, 0), (400, 0), (400, 600), 2)
   # screen.blit(game_window, (200, 100))
    pygame.display.update()
    clock.tick(60)

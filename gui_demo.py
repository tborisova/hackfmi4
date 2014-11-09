import pygame
import sys
import gui_elements

pygame.init()

screen = pygame.display.set_mode((800, 600))

clock = pygame.time.Clock()

first_player_text = gui_elements.TextBox(
    (200, 50), (200, 40), "Player 1", (0, 0, 0), (r"kick-ball/data/font.ttf", 100))
second_player_text = gui_elements.TextBox(
    (200, 50), (600, 40), "Player 2", (0, 0, 0), (r"kick-ball/data/font.ttf", 100))
maze_button = gui_elements.Button(
    "default", (255, 50), (155, 300), "Maze Runner", None, (0, 0, 0), (None, 100))
maze_input = gui_elements.InputBox(
    (70, 35), (343, 300), "000", (0, 0, 0), (None, 40), (255, 255, 255), (0, 0, 0), 1)
game_of_luck_button = gui_elements.Button(
    "default", (255, 50), (155, 380), "Game of Luck", None, (0, 0, 0), (None, 100))
game_of_luck_input = gui_elements.InputBox(
    (70, 35), (343, 380), "000", (0, 0, 0), (None, 40), (255, 255, 255), (0, 0, 0), 1)
kick_the_ball_button = gui_elements.Button(
    "default", (255, 50), (155, 460), "Kick the Ball", None, (0, 0, 0), (None, 100))
kick_the_ball_input = gui_elements.InputBox(
    (70, 35), (343, 460), "000", (0, 0, 0), (None, 40), (255, 255, 255), (0, 0, 0), 1)


input_boxes = [maze_input, game_of_luck_input, kick_the_ball_input]
buttons = [maze_button, game_of_luck_button, kick_the_ball_button]
text_boxes = [first_player_text, second_player_text]
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

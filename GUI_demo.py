import pygame
import sys
import GUI_elements

pygame.init()

screen = pygame.display.set_mode((500, 500))

clock = pygame.time.Clock()
username_text = GUI_elements.TextBox((200, 50), (255, 205), "Username")
username_input = GUI_elements.InputBox((200, 50), (255, 255), "")
password_text = GUI_elements.TextBox((200, 50), (255, 305), "Password")
password_input = GUI_elements.InputBox((200, 50), (255, 355), "")
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                password_input.update_state(event.pos, True)
                username_input.update_state(event.pos, True)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                password_input.update_state(event.pos, False)
                username_input.update_state(event.pos, False)
    password_input.update_state(pygame.mouse.get_pos(), None)
    username_input.update_state(pygame.mouse.get_pos(), None)

    screen.fill((55, 155, 255))
    password_input.draw(screen)
    username_input.draw(screen)
    username_text.draw(screen)
    password_text.draw(screen)
    pygame.display.update()
    clock.tick(60)

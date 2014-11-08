import pygame
from pygame.math import Vector2 as Vector

# TODO
# Make custom cursors
CURSORS = {"arrow": lambda: pygame.mouse.set_cursor(*pygame.cursors.arrow),
           "textmarker": lambda: pygame.mouse.set_cursor(
               (8, 16), (3, 5), *pygame.cursors.compile(
                   pygame.cursors.textmarker_strings))}


class InputBox(pygame.Rect):

    def __init__(self, dimensions, pos, text="", text_colour=(0, 0, 0),
                 text_font=(None, 50), bg_colour=(255, 255, 255)):
        pygame.Rect.__init__(self, (pos[0] - dimensions[0] / 2,
                                    pos[1] - dimensions[1] / 2), dimensions)
        self.dimensions = dimensions
        self.pos = pos
        self.text = text
        self.text_colour = text_colour
        self.text_font = text_font
        self.create_text_avatar()
        self.bg_colour = bg_colour
        self.clicked = False
        self.state = "normal"

    def draw(self, surface):
        if self.bg_colour is not None:
            pygame.draw.rect(surface, self.bg_colour, self, 0)
        surface.blit(self.text_avatar, (
            self.pos[0] - self.text_avatar.get_width() / 2,
            self.pos[0] - self.text_avatar.get_height() / 2))

    def create_text_avatar(self):
        self.text_avatar = pygame.font.Font(*self.text_font).render(
            self.text, 20, self.text_colour)
        if self.text_avatar.get_width() > self.dimensions[0] or \
           self.text_avatar.get_height() > self.dimensions[1]:
            self.text_avatar = pygame.transform.scale(
                self.text_avatar, self.dimensions)

    def update_state(self, cursor_pos, event):
        cursor_on_inputbox = self.collidepoint(cursor_pos)
        if self.state is "active":
            if not event:
                if cursor_on_inputbox:
                    self.state = "hover"
                    self.clicked = True
                    CURSORS["textmarker"]()
                    # self.sound_effect.play()
                else:
                    self.state = "normal"
                    CURSORS["arrow"]()
        elif self.state is "hover":
            if event and cursor_on_inputbox:
                self.state = "active"
            elif not cursor_on_inputbox:
                self.state = "normal"
                CURSORS["arrow"]()
        else:
            if event and cursor_on_inputbox:
                self.state = "active"
                CURSORS["textmarker"]()
            elif cursor_on_inputbox:
                self.state = "hover"
                CURSORS["textmarker"]()


class TextBox(pygame.Rect):

    def __init__(self, dimensions, pos, text, text_colour=(0, 0, 0),
                 text_font=(None, 50), bg_colour=None):
        pygame.Rect.__init__(self, (pos[0] - dimensions[0] / 2,
                                    pos[1] - dimensions[1] / 2), dimensions)
        self.dimensions = dimensions
        self.pos = pos
        self.text = text
        self.text_colour = text_colour
        self.text_font = text_font
        self.create_text_avatar()
        self.bg_colour = bg_colour

    def draw(self, surface):
        if self.bg_colour is not None:
            pygame.draw.rect(surface, self.bg_colour, self, 0)
        surface.blit(self.text_avatar, (
            self.pos[0] - self.text_avatar.get_width() / 2,
            self.pos[1] - self.text_avatar.get_height() / 2))

    def create_text_avatar(self):
        InputBox.create_text_avatar(self)

class Button(TextBox):

    def __init__(self, dimensions, pos, text, text_colour=(0, 0, 0),
                 text_font=(None, 50), bg_colour=None):
        pygame.TextBox.__init__(self, dimensions, pos, text, text_colour, 
                                text_font)



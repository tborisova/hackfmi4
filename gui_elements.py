import pygame
from pygame import Rect
from pygame.math import Vector2 as Vector

# TODO
# Make custom cursors
CURSORS = {"arrow": lambda: pygame.mouse.set_cursor(*pygame.cursors.arrow),
           "textmarker": lambda: pygame.mouse.set_cursor(
               (8, 16), (3, 5), *pygame.cursors.compile(
                   pygame.cursors.textmarker_strings))}


class InputBox(Rect):

    PADDING = 3
    HANDLED_KEYS = set(
        [
            pygame.K_DELETE,
            pygame.K_BACKSPACE,
            pygame.K_LEFT,
            pygame.K_RIGHT]).union(
        range(
            pygame.K_a,
            pygame.K_z +
            1)).union(
        range(
            pygame.K_0,
            pygame.K_9 +
            1))

    def __init__(self, dimensions, pos, text="", text_colour=(0, 0, 0),
                 text_font=(None, 50), bg_colour=(255, 255, 255),
                 frame_colour=None, frame_size=0):
        Rect.__init__(self, (pos[0] - dimensions[0] / 2,
                             pos[1] - dimensions[1] / 2), dimensions)
        self.text = text
        self.text_colour = text_colour
        self.text_font = text_font
        self.create_char_avatars()
        self.bg_colour = bg_colour
        self.frame_colour = frame_colour
        self.frame_size = frame_size
        self.input_cursor = Rect((self.left, self.top + InputBox.PADDING),
                                 (2, (self.height - 2 * InputBox.PADDING)))
        self.put_cursor(self.right)
        self.clicked = False
        self.state = "normal"
        self.char_limit = None
        self.handled_chars = InputBox.HANDLED_KEYS

    def draw(self, surface):
        if self.bg_colour is not None:
            pygame.draw.rect(surface, self.bg_colour, self, 0)
        if self.frame_colour is not None:
            pygame.draw.rect(surface, self.frame_colour, self, self.frame_size)
        shift = 0
        for char in self.char_avatars:
            surface.blit(char, (
                self.left + InputBox.PADDING + shift,
                self.centery - char.get_height() / 2))
            shift += char.get_width()
        if self.state == "active":
            pygame.draw.rect(surface, self.text_colour, self.input_cursor)

    def create_char_avatars(self):
        self.char_avatars = []
        for char in self.text:
            char_avatar = pygame.font.Font(*self.text_font).render(
                char, 20, self.text_colour)
            if char_avatar.get_height() > self.y:
                char_avatar = pygame.transform.scale(
                    char_avatar, (char_avatar.get_width(), self.height))
            self.char_avatars.append(char_avatar)

    def put_cursor(self, cursor_x):
        error = cursor_x - (self.left + InputBox.PADDING)
        self.cursor_index = len(self.char_avatars)
        for index, char in enumerate(self.char_avatars):
            if error < char.get_width() / 2:
                self.cursor_index = index
                break
            error -= char.get_width()
        cursor_x -= error
        self.input_cursor.move_ip(cursor_x - self.input_cursor.left, 0)

    def update_state(self, cursor_pos, event):
        cursor_on_inputbox = self.collidepoint(cursor_pos)
        if self.state is "active":
            if not cursor_on_inputbox:
                if event:
                    self.state = "normal"
                CURSORS["arrow"]()
            if cursor_on_inputbox:
                if event:
                    self.put_cursor(cursor_pos[0])
                CURSORS["textmarker"]()
        elif self.state is "hover":
            if event and cursor_on_inputbox:
                self.state = "active"
                self.put_cursor(cursor_pos[0])
            elif not cursor_on_inputbox:
                self.state = "normal"
                CURSORS["arrow"]()
        else:
            if event and cursor_on_inputbox:
                self.state = "active"
                CURSORS["textmarker"]()
                self.put_cursor(cursor_pos[0])
            elif cursor_on_inputbox:
                self.state = "hover"
                CURSORS["textmarker"]()

    def shift_cursor(self, positions):
        direction = int(abs(positions) / positions)
        side = 1
        if direction == 1:
            side = 0
        for index in range(0, abs(positions)):
            self.input_cursor.move_ip((direction * self.char_avatars[
                self.cursor_index - side].get_width()), 0)
            self.cursor_index += direction

    def handle_key_event(self, key):
        if self.state != "active":
            pass
        elif key == pygame.K_BACKSPACE and self.cursor_index:
            self.shift_cursor(-1)
            self.text = self.text[:self.cursor_index] + \
                self.text[1 + self.cursor_index:]
            self.create_char_avatars()
        elif key == pygame.K_DELETE and self.cursor_index < len(
                self.char_avatars):
            self.text = self.text[:self.cursor_index] + \
                self.text[self.cursor_index + 1:]
            self.create_char_avatars()
        elif key in self.handled_chars:
            if self.char_limit is None or self.char_limit > len(self.text):
                self.text = self.text[:self.cursor_index] + chr(key) +\
                    self.text[self.cursor_index:]
                self.create_char_avatars()
                self.shift_cursor(1)
        elif key == pygame.K_LEFT and self.cursor_index:
            self.shift_cursor(-1)

        elif key == pygame.K_RIGHT and self.cursor_index < len(
                self.char_avatars):
            self.shift_cursor(1)


class TextBox(Rect):

    def __init__(self, dimensions, pos, text, text_colour=(0, 0, 0),
                 text_font=(None, 50), bg_colour=None):
        Rect.__init__(self, (pos[0] - dimensions[0] / 2,
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
        self.text_avatar = pygame.font.Font(*self.text_font).render(
            self.text, 20, self.text_colour)
        if self.text_avatar.get_width() > self.x - 2 * InputBox.PADDING or \
           self.text_avatar.get_height() > self.y - 2 * InputBox.PADDING:
            self.text_avatar = pygame.transform.scale(
                self.text_avatar, (self.dimensions[0] - 2 * InputBox.PADDING,
                                   self.dimensions[1] - 2 * InputBox.PADDING))


class Button(TextBox):

    BUTTON_TYPES = {"default": {"normal": {"background": (160, 6, 8),
                                           "frame": (0, 0, 0)},
                                "hover": {"background": (191, 9, 8),
                                          "frame": (0, 0, 0)},
                                "active": {"background": (130, 6, 8),
                                           "frame": (0, 0, 0)}}}

    def __init__(self, button_type, dimensions, pos, text,
                 background=None, text_colour=(0, 0, 0), text_font=(None, 50),
                 frame_size=3):
        TextBox.__init__(self, dimensions, pos, text, text_colour,
                         text_font)
        self.button_type = button_type
        self.frame_size = frame_size
        self.state_colours = Button.BUTTON_TYPES[button_type]
        self.state = "normal"
        self.clicked = False
        self.background = background
        if background is not None:
            self.background = pygame.transform.scale(background, dimensions)

    def draw(self, surface):
        pygame.draw.rect(surface, self.state_colours[self.state]["background"],
                         self)
        pygame.draw.rect(surface, self.state_colours[self.state]["frame"],
                         self, self.frame_size)
        if self.background is not None:
            pygame.blit(surface, self.topleft)
        TextBox.draw(self, surface)

    def update_state(self, cursor_pos, event):
        cursor_on_button = self.collidepoint(cursor_pos)
        if self.state is "active":
            if event is not None:
                if cursor_on_button:
                    self.state = "hover"
                else:
                    self.state = "normal"
        elif self.state is "hover":
            if event and cursor_on_button:
                self.state = "active"
                self.clicked = True
            elif not cursor_on_button:
                self.state = "normal"
        else:
            if event and cursor_on_button:
                self.state = "active"
                self.clicked = True
            elif cursor_on_button:
                self.state = "hover"

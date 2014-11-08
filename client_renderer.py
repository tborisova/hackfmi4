import pygame
import json
import images

class Client:

    FPS = 60
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 800

    def __init__(self):
        self.init_graphics()
        self.clock = pygame.time.Clock()

    def init_graphics(self):
        logo = pygame.transform.scale(images.images["logo"], (32, 32))
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Challenge Accepted", "Challenge Accepted")
        self.screen = pygame.display.set_mode((1040, 600))
        self.inner_game_screen = pygame.Surface((800, 600), 0, self.screen)



    # def get_dicts_from_json(self, frame_json):
    #     frame_objects = json.load(frame_json)
    #     image_objects = json.load(frame_objects[images])
    #     text_objects = json.load(frame_objects[texts])
    #     # ... other objects?

    def get_all_objects(self, frame_json):
        # frame_json = get_json()
        frame_json = open("test_frame.json")
        #
        return json.load(frame_json)       

    def render(self):
        image_objects = {}
        #text_objects = {}
        
        while True:
            #draw_background(self.screen)

            # recieve frame?
            #all_objects = self.get_all_objects(frame_json)
            all_objects = self.get_all_objects(None)

            self.draw_all_images(self, self.inner_game_screen, all_objects[images])
            #draw_text(self, inner_game_screen)
            self.screen.draw((120, 40), self.inner_game_screen)

    def draw_all_images(self, sruface, images):
        for image in images:
            self.draw_image(surface, image)

    def draw_image(self, surface, image_info):
        image = images[image_info[image]]
        surface.blit(image, (image_info[x], image_info[y]))
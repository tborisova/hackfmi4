import pygame
import json
import images
import sys

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
        self.screen = pygame.display.set_mode((1040, 680))
        self.inner_game_screen = pygame.Surface((800, 600), 0, self.screen)



    def get_all_objects(self, frame_json):
        #frame_json = get_json()    ?


        #-----------------------------------------Del
        with open("test_frame.json") as test_frame:
            try:
                return json.load(test_frame)
            except ValueError:
                lines = test_frame.readlines()
                #print(lines)
                return { "images" : {"55299120" : { "image" : "good_luck" , "x" : 217, "y" : 217}, "55298352" : { "image" : "good_luck" , "x" : 344, "y" : 492}, "55292592" : { "image" : "good_luck" , "x" : 581, "y" : 216}, "55299312" : { "image" : "good_luck" , "x" : 249, "y" : 431}, "55299344" : { "image" : "good_luck" , "x" : 291, "y" : 132}, "42733968" : { "image" : "good_luck" , "x" : 551, "y" : 430}, "42734000" : { "image" : "good_luck" , "x" : 457, "y" : 491}, "55299856" : { "image" : "bad_luck" , "x" : 507, "y" : 131}, "55299792" : { "image" : "bad_luck" , "x" : 398, "y" : 100}, "55299280" : { "image" : "bad_luck" , "x" : 202, "y" : 329}, "55292624" : { "image" : "bad_luck" , "x" : 598, "y" : 327}} }
        #--------------------------------DEL


    def handle_game(self):

        while True:
            #get_input_from_server()

            #do_background_stuff()
            #draw_background(self.screen)

            self.inner_game_screen.fill((255, 255, 255))
            # recieve frame?
            #all_objects = self.get_all_objects(frame_json)
            all_objects = self.get_all_objects(None)

            self.draw_all_images(self.inner_game_screen, all_objects["images"])
            #draw_text(self, inner_game_screen)
            self.screen.blit(self.inner_game_screen, (120, 40))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            pygame.display.update()



    def draw_all_images(self, surface, images):
        for image in images:
            self.draw_image(surface, images[image])

    def draw_image(self, surface, image_info):
        image = images.images[image_info["image"]]
        surface.blit(image, (image_info["x"], image_info["y"]))
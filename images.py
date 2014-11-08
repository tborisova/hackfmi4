import pygame

images = {
            "top_wall" : pygame.transform.scale(pygame.image.load("images/top_wall.png"), (25, 25)),
            "left_wall": pygame.transform.scale(pygame.image.load("images/left_wall.png"), (25, 25)),
            "top_left_wall": pygame.transform.scale(pygame.image.load("images/top_left_wall.png"), (25, 25)),
            "maze_player": pygame.transform.scale(pygame.image.load("images/maze_player.png"), (16, 16)),
            "bad_luck" : pygame.image.load("images/bad_luck.png"),
            "good_luck" : pygame.image.load("images/good_luck.png"),
            "logo" : pygame.image.load("images/logo.png"),
            "arrow_of_fortune" : pygame.image.load("images/arrow_of_fortune.png"),
            #"maze_win" : pygame.transform.scale(pygame.image.load("images/maze_win.png"), (16, 16))
            "ball": pygame.image.load("images/ball.png")
        }
import pygame
import json


def parse(events):
    parsed_events = {"left": False,
                     "right": False,
                     "up": False,
                     "down": False
                     }
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                parsed_events["up"] = True
            elif event.key == pygame.K_DOWN:
                parsed_events["down"] = True
            elif event.key == pygame.K_LEFT:
                parsed_events["left"] = True
            elif event.key == pygame.K_RIGHT:
                parsed_events["right"] = True
    parsed_events["mouse_pos"] = {"x": pygame.mouse.get_pos()[0],
                                  "y": pygame.mouse.get_pos()[1]
                                  }
    parsed = json.dumps(parsed_events)
    with open("events.json", "w") as json_file:
        json_file.write(parsed)


def unparse():
    with open("events.json", "rb") as json_file:
        return json.load(json_file)

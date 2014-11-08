import random
import json
import time
import pygame
import sys
import time
#from renderer import draw_everything

class Cell:
    def __init__(self):
        self.top_wall = True
        self.left_wall = True
        self.was_visited = False

class Player:
    def __init__(self, maze):
        self.x = 7
        self.y = 7
        self.displacement = 7
        self.cell_size = 25
        self.maze = maze

    def move(self, direction):
        maze = list(zip(*self.maze))
        if direction == "up":
            if self.y > 0 and not maze[self.x // self.cell_size][self.y // self.cell_size].top_wall:
                self.y -= self.cell_size
        if direction == "down":
            if self.y // self.cell_size + 1 < len(maze) and self.y < len(maze) * self.cell_size and not maze[self.x // self.cell_size][self.y // self.cell_size + 1].top_wall:
                self.y += self.cell_size
        if direction == "left":
            if self.x > 0 and not maze[self.x // self.cell_size][self.y // self.cell_size].left_wall:
                self.x -= self.cell_size
        if direction == "right":
            if self.x // self.cell_size + 1 < len(maze) and self.x < len(maze) * self.cell_size and not maze[self.x // self.cell_size + 1][self.y // self.cell_size].left_wall:
                self.x += self.cell_size


class MazeGame:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        #self.maze = [[Cell() for i in range(3)] for j in range(3)]
        self.set_difficulty()
        self.generate_maze()
        self.player = Player(self.maze)
        self.width = 800
        self.height = 600
        self.displacement_x = self.width // 2 - len(self.maze) * self.player.cell_size + (len(self.maze) // 2) * self.player.cell_size
        self.displacement_y = self.height // 2 - len(self.maze) * self.player.cell_size + (len(self.maze) // 2) * self.player.cell_size

    def no_continuation_test(self, cell_x, cell_y):
        should_pop = True
        if cell_y + 1 < len(self.maze) and not self.maze[cell_x][cell_y + 1].was_visited:
            should_pop = False
        if cell_x + 1 < len(self.maze) and not self.maze[cell_x + 1][cell_y].was_visited:
            should_pop = False
        if cell_y - 1 >= 0 and not self.maze[cell_x][cell_y - 1].was_visited:
            should_pop = False
        if cell_x - 1 >= 0 and not self.maze[cell_x - 1][cell_y].was_visited:
            should_pop = False
        return should_pop

    def list_all_available_neighbours(self, cell_x, cell_y):
        neighbours = []
        if cell_y + 1 < len(self.maze) and not self.maze[cell_x][cell_y + 1].was_visited:
            neighbours.append(1)
        if cell_x + 1 < len(self.maze) and not self.maze[cell_x + 1][cell_y].was_visited:
            neighbours.append(2)
        if cell_y - 1 >= 0 and not self.maze[cell_x][cell_y - 1].was_visited:
            neighbours.append(3)
        if cell_x - 1 >= 0 and not self.maze[cell_x - 1][cell_y].was_visited:
            neighbours.append(4)
        return neighbours

    def select_random_neighbour(self, cell_x, cell_y):
        neighbours = self.list_all_available_neighbours(cell_x, cell_y)
        if len(neighbours) < 1:
            position = 0
        else:
            position = random.randint(0, len(neighbours) - 1)
        if len(neighbours) != 0:
            cell = neighbours[position]
            #this might be a problem
            if cell == 1:
                self.maze[cell_x][cell_y + 1].left_wall = False
                self.maze[cell_x][cell_y + 1].was_visited = True
                return cell_x, cell_y + 1
            elif cell == 2:
                self.maze[cell_x + 1][cell_y].top_wall = False
                self.maze[cell_x + 1][cell_y].was_visited = True
                return cell_x + 1, cell_y
            elif cell == 3:
                self.maze[cell_x][cell_y].left_wall = False
                self.maze[cell_x][cell_y - 1].was_visited = True
                return cell_x, cell_y - 1
            elif cell == 4:
                self.maze[cell_x][cell_y].top_wall = False
                self.maze[cell_x - 1][cell_y].was_visited = True
                return cell_x - 1, cell_y
        return

    def generate_maze(self):
        visited = []
        visited.append((0, 0))
        no_continuation = self.no_continuation_test(0, 0)
        self.maze[0][0].was_visited = True
        cell = (0, 0)
        while len(visited) > 0:
            cell = visited[len(visited) - 1]

            if no_continuation:
                visited.pop()
            else:
                visited.append(self.select_random_neighbour(cell[0], cell[1]))

                if visited[len(visited) - 1] is None:
                    visited.pop()
            if len(visited) > 0:
                cell = visited[len(visited) - 1]


            no_continuation = self.no_continuation_test(cell[0], cell[1])

    def generate_coordinates(self):
        coordinates = []
        maze = (list(zip(*self.maze)))
        for i in range(len(self.maze)):
            for j in range(len(self.maze)):
                if maze[i][j].left_wall and maze[i][j].top_wall:
                    coordinates.append(("top_left_wall", self.displacement_x + i * self.player.cell_size, self.displacement_y + j * self.player.cell_size))
                elif maze[i][j].top_wall:
                    coordinates.append(("top_wall", self.displacement_x + i * self.player.cell_size, self.displacement_y + j * self.player.cell_size))
                elif maze[i][j].left_wall:
                    coordinates.append(("left_wall", self.displacement_x + i * self.player.cell_size, self.displacement_y + j * self.player.cell_size))

        for i in range(len(maze)):
            coordinates.append(("left_wall", self.displacement_x + len(maze) * self.player.cell_size,
                                self.displacement_y + i * self.player.cell_size))
            coordinates.append(("top_wall", self.displacement_x + i * self.player.cell_size,
                                self.displacement_y + len(maze) * self.player.cell_size))
        coordinates.append(("maze_player", self.displacement_x + self.player.x, self.displacement_y + self.player.y))
        coordinates.append(("maze_win", self.displacement_x + (len(maze) - 1) * self.player.cell_size + self.player.displacement,
                            self.displacement_y + (len(maze) - 1) * self.player.cell_size + self.player.displacement))
        coordinates.append(("clock", str(self.time - int(self.difference)), 0, 0))
        return coordinates


        # json_string = ''
        # images = []
        # for coordinate in coordinates:
        #     if coordinate[0] == 'clock':
        #         json_string += json.dumps({str(id(coordinate)): {'clock': coordinate[0], 'time': coordinate[1], 'x': coordinate[2], 'y': coordinate[3]}})
        #     else:
        #
        #     json_string += json.dumps({(str(id(coordinate))): {'image': coordinate[0], 'x': coordinate[1], 'y': coordinate[2]}})
        # return json_string

    def check_if_player_wins(self):
        if self.player.x == (len(self.maze) - 1) * self.player.cell_size + self.player.displacement and \
            self.player.y == (len(self.maze) - 1) * self.player.cell_size + self.player.displacement:
            return True

    def start_game(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        start = time.time()
        self.difference = 0
        #print(self.generate_JSON_string())
        while True:
            keys = pygame.key.get_pressed()
            #this is to be moved in another module
            if self.check_if_player_wins():
                return True
            end = time.time()
            self.difference = end - start
            if self.difference >= self.time:
                return False
            if keys[pygame.K_LEFT]:
                self.player.move("left")
                time.sleep(0.1)
            if keys[pygame.K_RIGHT]:
                self.player.move("right")
                time.sleep(0.1)
            if keys[pygame.K_DOWN]:
                self.player.move("down")
                time.sleep(0.1)
            if keys[pygame.K_UP]:
                self.player.move("up")
                time.sleep(0.1)
            #draw_everything(screen, self.generate_coordinates())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            with open("test_frame.json", "w") as json_file:
                json_file.write(self.generate_JSON_string())

            pygame.display.update()
        return True

    def set_difficulty(self):
        if self.difficulty <= 6:
            self.maze = [[Cell() for i in range(10)] for j in range(10)]
        else:
            self.maze = [[Cell() for i in range(int(self.difficulty * 2.3))] for j in range(int(self.difficulty * 2.3))]
        self.time = 60 + 400 // self.difficulty

    def print(self):
        #for testing purposes
        for i in range(len(self.maze)):
            for j in range(2):
                for m in range(len(self.maze)):
                    if j == 0:
                        if self.maze[i][m].top_wall:
                            print("+---", end="")
                        else:
                            print("+   ", end="")
                        if m == len(self.maze) - 1:
                            print("+")
                    else:
                        if self.maze[i][m].left_wall:
                            print("|   ", end="")
                        else:
                            print("    ", end="")
                        if m == len(self.maze) - 1:
                            print("|")
        for i in range(len(self.maze)):
            print("+---", end="")
        print("+")
import random
import json
import time
import pygame
import sys
import time
from renderer import draw_everything
from event_handler import unparse
from time import sleep, localtime
from weakref import WeakKeyDictionary
from PodSixNet.Server import Server
from PodSixNet.Channel import Channel


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
            if self.y > 0 and not maze[
                    self.x //
                    self.cell_size][
                    self.y //
                    self.cell_size].top_wall:
                self.y -= self.cell_size
        if direction == "down":
            if self.y // self.cell_size + 1 < len(maze) and self.y < len(maze) * self.cell_size and not maze[
                    self.x // self.cell_size][self.y // self.cell_size + 1].top_wall:
                self.y += self.cell_size
        if direction == "left":
            if self.x > 0 and not maze[
                    self.x //
                    self.cell_size][
                    self.y //
                    self.cell_size].left_wall:
                self.x -= self.cell_size
        if direction == "right":
            if self.x // self.cell_size + 1 < len(maze) and self.x < len(maze) * self.cell_size and not maze[
                    self.x // self.cell_size + 1][self.y // self.cell_size].left_wall:
                self.x += self.cell_size


class ClientChannel(Channel):

    def __init__(self, *args, **kwargs):
        self.nickname = "anonymous"
        Channel.__init__(self, *args, **kwargs)

    def Close(self):
        self._server.DelPlayer(self)

    def Network_print_game_state(self, data):
        objects = self._server.generate_coordinates()
        self._server.end = time.time()
        self._server.difference = self._server.end - self._server.start
        self._server.SendToAll({'action': 'render_game_state',
                                'objects': objects,
                                'player_wins': self._server.check_if_player_wins(),
                                'time_is_up': self._server.time_is_up()})

    def Network_player_move(self, data):
        if self._server.player_can_write(self):
            self._server.player.move(data['move'])


class MazeGame(Server):

    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        pygame.init()
        Server.__init__(self, *args, **kwargs)
        self.width = 800
        self.height = 600
        self.start = time.time()
        self.end = 0
        self.difference = 0
        self.clock = pygame.time.Clock()
        self.players = WeakKeyDictionary()
        self.players_order = WeakKeyDictionary()
        self.current_index = 0
        print('Server launched')

    def player_can_write(self, channel):
        return self.players_order[channel] == 0

    def no_continuation_test(self, cell_x, cell_y):
        should_pop = True
        if cell_y + \
                1 < len(self.maze) and not self.maze[cell_x][cell_y + 1].was_visited:
            should_pop = False
        if cell_x + \
                1 < len(self.maze) and not self.maze[cell_x + 1][cell_y].was_visited:
            should_pop = False
        if cell_y - 1 >= 0 and not self.maze[cell_x][cell_y - 1].was_visited:
            should_pop = False
        if cell_x - 1 >= 0 and not self.maze[cell_x - 1][cell_y].was_visited:
            should_pop = False
        return should_pop

    def list_all_available_neighbours(self, cell_x, cell_y):
        neighbours = []
        if cell_y + \
                1 < len(self.maze) and not self.maze[cell_x][cell_y + 1].was_visited:
            neighbours.append(1)
        if cell_x + \
                1 < len(self.maze) and not self.maze[cell_x + 1][cell_y].was_visited:
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
            # this might be a problem
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
                    coordinates.append(
                        ("top_left_wall",
                         self.displacement_x +
                         i *
                         self.player.cell_size,
                         self.displacement_y +
                         j *
                         self.player.cell_size))
                elif maze[i][j].top_wall:
                    coordinates.append(
                        ("top_wall",
                         self.displacement_x +
                         i *
                         self.player.cell_size,
                         self.displacement_y +
                         j *
                         self.player.cell_size))
                elif maze[i][j].left_wall:
                    coordinates.append(
                        ("left_wall",
                         self.displacement_x +
                         i *
                         self.player.cell_size,
                         self.displacement_y +
                         j *
                         self.player.cell_size))

        for i in range(len(maze)):
            coordinates.append(
                ("left_wall",
                 self.displacement_x +
                 len(maze) *
                    self.player.cell_size,
                    self.displacement_y +
                    i *
                    self.player.cell_size))
            coordinates.append(
                ("top_wall",
                 self.displacement_x +
                 i *
                 self.player.cell_size,
                 self.displacement_y +
                 len(maze) *
                    self.player.cell_size))
        coordinates.append(
            ("maze_player",
             self.displacement_x +
             self.player.x,
             self.displacement_y +
             self.player.y))
        coordinates.append(("maze_win", self.displacement_x +
                            (len(maze) -
                             1) *
                            self.player.cell_size +
                            self.player.displacement, self.displacement_y +
                            (len(maze) -
                             1) *
                            self.player.cell_size +
                            self.player.displacement))
        coordinates.append(
            ("clock", str(self.time - int(self.difference)), 0, 0))
        return coordinates

    def check_if_player_wins(self):
        if self.player.x == (len(self.maze) - 1) * self.player.cell_size + self.player.displacement and \
                self.player.y == (len(self.maze) - 1) * self.player.cell_size + self.player.displacement:
            return True

    def time_is_up(self):
        return self.difference >= self.time

    def set_difficulty(self):
        if self.difficulty <= 6:
            self.maze = [[Cell() for i in range(10)] for j in range(10)]
        else:
            self.maze = [[Cell() for i in range(int(self.difficulty * 2.3))]
                         for j in range(int(self.difficulty * 2.3))]
        self.time = 60 + 400 // self.difficulty

    def Connected(self, channel, addr):
        if self.current_index < 2:
            self.AddPlayer(channel)

    def AddPlayer(self, player):
        self.players[player] = True
        self.players_order[player] = self.current_index
        self.current_index += 1

    def SendToAll(self, data):
        [p.Send(data) for p in self.players]

    def Launch(self, difficulty):
        self.difficulty = difficulty
        self.set_difficulty()
        self.generate_maze()
        self.player = Player(self.maze)
        self.displacement_x = self.width // 2 - \
            len(self.maze) * self.player.cell_size + (len(self.maze) // 2) * self.player.cell_size
        self.displacement_y = self.height // 2 - \
            len(self.maze) * self.player.cell_size + (len(self.maze) // 2) * self.player.cell_size
        while True:
            self.Pump()
            sleep(0.0001)

    def DelPlayer(self, player):
        self.players[player] = False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: {0} host:port".format(sys.argv[0]))
        print("e.g. {0} localhost:31425".format(sys.argv[0]))
    else:
        host, port = sys.argv[1].split(":")
        s = MazeGame(localaddr=(host, int(port)))
        difficulty = 3
        s.Launch(difficulty)

import random

class Cell:
    def __init__(self):
        self.top_wall = True
        self.left_wall = True
        self.was_visited = False


class MazeGame:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.maze = [[Cell() for i in range(4)] for j in range(4)]

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
            print(neighbours, cell)
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
                cell = visited[len(visited) - 1]

                if visited[len(visited) - 1] is None:
                    visited.pop()

            no_continuation = self.no_continuation_test(cell[0], cell[1])

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
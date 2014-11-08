from maze_game import MazeGame

x = MazeGame(1)
m = list(zip(*x.maze))
print(m[0][1].left_wall, m[0][1].top_wall)
print(m[1][0].left_wall, m[1][0].top_wall)


x.print()
x.start_game()

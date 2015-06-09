import random
import sys

#Please note: all coordinates are stored as [x, y]
#one can obtain the data at the corresponding coordinate in a maze using maze[y][x]
def generate_maze(w, h, global_density = 0.4, local_density = 2):
    level = [['.' for x in range(w)] for y in range(h)]
    for i in range(int(global_density*w*h)):
        while True:
            x = random.randint(1,w)-1
            y = random.randint(1,h)-1
            if level[y][x] != '.':
                continue
            c = 0
            for dx in range(-1,2):
                for dy in range(-1,2):
                    if level[(y+dy+h)%h][(x+dx+w)%w] != '.':
                        c+=1
            if c > local_density:
                continue
            level[y][x] = '#'
            break
    return level

def generate_maze2(w, h):
    maze = [[".#"[(x%2)*(y%2)] for x in range(w)] for y in range(h)]
    return maze

def get_empty_cell(maze, w, h, c='None'):
    for i in range(100):
        x = random.randint(1,w)-1
        y = random.randint(1,h)-1
        if maze[y][x] == '.':
            if c != 'None':
                maze[y][x]=c
            return [x,y]
    return 0

def show_maze(maze, fout=sys.stdout):
    for line in maze:
        fout.write("".join(line)+"\n")
